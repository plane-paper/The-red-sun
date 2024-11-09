from particle import KunaiHitParticle
from primitives import GameObject, Pose
import pygame
from projectile import Kunai
import constants as c
from sprite import Sprite, SpriteSheet

class Player(GameObject):

    def __init__(self, game):
        #Initialization
        self.position = Pose((0, 0))
        self.velocity = Pose((0, 0))
        self.recoil_velocity = Pose((0, 0))
        self.game = game
        self.jumps = 2
        self.grounded = False
        self.projectiles = []
        self.ammo = 3
        self.beaming = False
        self.beam_target = Pose((c.GAME_WIDTH//2, c.GAME_HEIGHT//2 - 150))
        self.charge = 0

        self.sprite = Sprite(16)
        idle_right = SpriteSheet("images/player_idle_1.png", (8, 1), 8, repeat=True) #Idle_left is deleted for convenience purposes
        run_right = SpriteSheet("images/player_run_1.png", (4, 1), 4, repeat=True)
        run_left = SpriteSheet("images/player_run_1.png", (4, 1), 4, repeat=True, xflip=True)
        falling = SpriteSheet("images/player_falling_1.png", (3, 1), 3, repeat=False)
        jumping = SpriteSheet("images/player_jumping_1.png", (1, 1), 1)
        self.sprite.add_animation(
            {"idle_right": idle_right,
             "run_right": run_right,
             "run_left": run_left,
             "falling": falling,
             "jumping": jumping}
        ) #I hate dictionaries
        self.sprite.start_animation("idle_right")
        self.falling = False

        self.move_direction = 0  #right 1, left -1

    def update(self, dt, events):
        self.sprite.update(dt)

        for projectile in self.projectiles[:]:
            projectile.update(dt, events)
            if (projectile.position - Pose((c.WINDOW_WIDTH//2, c.WINDOW_HEIGHT//2))).magnitude() > c.WINDOW_WIDTH*3:
                self.projectiles.remove(projectile)
            if (projectile.pickup or projectile.gravity) and (projectile.position - self.position).magnitude() < 30:
                self.projectiles.remove(projectile)
                self.ammo += 1
                self.game.pickup_kunai.play()

        if self.beaming: #Move player to the top of the screen
            self.velocity = (self.beam_target - self.position)*1.5
            self.position += self.velocity * dt
            return

        gravity = 3000
        speed = 800

        self.recoil_velocity *= 0.0001**dt #Change for recoil

        pressed = pygame.key.get_pressed()
        left = pressed[pygame.K_a] and not self.game.lost
        right = pressed[pygame.K_d] and not self.game.lost
        up = (pressed[pygame.K_w] or pressed[pygame.K_SPACE]) and not self.game.lost
        down = pressed[pygame.K_s] and not self.game.lost
        control_velocity = Pose((speed * (right - left), 1200 * down))
        self.velocity += Pose((0, 1000*-up)) * dt #This is faster than event loop, also much easier to structure

        if not self.grounded: #In air
            if self.velocity.y + control_velocity.y < 0:
                self.sprite.start_animation("jumping")
            elif not self.falling:
                self.falling = True #Don't delete
                self.sprite.start_animation("falling")

        if left and not right and self.grounded and self.move_direction != -1: #At ground
            self.sprite.start_animation("run_left")
            self.move_direction = -1
        elif right and not left and self.grounded and self.move_direction != 1:
            self.sprite.start_animation("run_right")
            self.move_direction = 1
        elif ((not left and not right) or (left and right)) and self.grounded and self.move_direction != 0:
            self.sprite.start_animation("idle_right")
            self.move_direction = 0

        mpos = pygame.mouse.get_pos()
        relmpos = Pose(mpos) * (c.GAME_WIDTH/c.WINDOW_WIDTH) - self.position

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_SPACE:
                    self.try_jump()
                if event.key == pygame.K_e:
                    if not self.game.rewinding and self.charge >= 125:
                        self.game.start_rewind()
                    elif not self.game.rewinding:
                        self.game.nope_sound.play()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.shoot(relmpos)


        self.velocity += Pose((0, gravity)) * dt

        if self.position.y > self.game.floor - 20:
            if self.velocity.y + control_velocity.y + self.recoil_velocity.y > 0:
                self.land()

        if self.grounded:
            self.velocity -= self.velocity
            control_velocity.y = 0
            self.position.y = self.game.floor - 20

        self.position += self.velocity * dt + control_velocity * dt + self.recoil_velocity * dt

        if self.position.x < 0 or self.position.x > c.WINDOW_WIDTH:
            self.position.x = max(0, min(c.WINDOW_WIDTH, self.position.x))
            self.recoil_velocity.x = 0

        for enemy in self.game.enemies[:]:
            if enemy.destroyed:
                continue
            if (enemy.position - self.position).magnitude() < 50:
                self.get_hit_by_enemy(enemy)

    def land(self):
        self.jumps = 2 #Reset
        if not self.grounded: #Reset grounded
            self.grounded = True
            self.sprite.start_animation("idle_right")
            self.move_direction = 0

    def try_jump(self):
        if self.jumps > 0:
            self.grounded = False
            self.falling = False
            self.jumps -= 1
            jump = 1000
            self.velocity = Pose((0, -jump))
            self.sprite.start_animation("falling")
            self.game.jump_sound.play()

    def get_hit_by_enemy(self, enemy):
        self.game.player_hurt.play()
        self.game.destroy_all_enemies()
        self.velocity = Pose((0, 0))
        self.recoil_velocity += (self.position - enemy.position) * (5000/(self.position - enemy.position).magnitude()) #Bounce back
        self.charge = 0 #Clear charges
        for i in range(50):
            self.game.particles.append(KunaiHitParticle(self.position.get_position(), color=(255, 50, 50)))#Blood particles
            self.game.shake(direction = (enemy.position - self.position).get_position(), amt=70)

    def draw(self, surf, offset=(0, 0)):
        position = self.position + Pose(offset)
        self.sprite.set_position((self.position + Pose(offset)).get_position())
        self.sprite.draw(surf)
        for projectile in self.projectiles:
            projectile.draw(surf, offset)

    def start_tractor_beam(self):
        self.beaming = True
        self.grounded = False 
        self.recoil_velocity *= 0
        self.move_direction = -1 #Always face left if moving when rewind
        self.sprite.start_animation("run_left")

    def end_tractor_beam(self):
        self.beaming = False
        self.recoil_velocity*= 0 #Change
        self.jumps = 1
        self.grounded = False
        self.velocity = Pose((0, -500))
        self.falling = False

    def shoot(self, velocity):
        if not self.ammo: #Check for ammo
            return
        self.move_direction = 0
        self.sprite.start_animation("idle_right")
        self.game.shoot_kunai_sound.play()
        self.ammo -= 1
        velocity = velocity * (1/velocity.magnitude()) * 4000 #Change for slower kunai + lower rec
        self.recoil_velocity -= velocity * 0.3 #Rec is 70% of velocity of kunai
        self.projectiles.append(Kunai(self.game, velocity=velocity.get_position(), position=self.position.get_position())) #Shoot Kunai