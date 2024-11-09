import pygame
import constants as c

import sys
import math
from player import Player
from primitives import Pose
from particle import RewindParticle, SunExplosion, SunTint, WarningParticle, SunExplosionLong
from enemy import Orb, Scuttle
from Button import Button
import random

black = (0, 0, 0)

class Game:

    def __init__(self): #Initializations (Game Window)
        pygame.init()
        self.fullscreen = True
        self.screen = pygame.display.set_mode((c.WINDOW_WIDTH, c.WINDOW_HEIGHT))
        pygame.display.set_icon(pygame.image.load("images/red_sun.jpg"))
        self.colorblind_mode = True #Default contrast on
        self.music_play = True
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("The Red Sun")

        self.config_menu()
        self.last_distance = None

        self.intro()
        self.directions()

        while True:

            self.init()
            self.main()

    def victory_screen(self, prev_surf):
        shade = pygame.Surface((c.WINDOW_WIDTH, c.WINDOW_HEIGHT))
        shade.fill((0, 0, 0))
        alpha = 0
        age = 0
        while alpha < 255:
            events, dt = self.get_events()
            age += dt
            self.screen.fill(black)
            self.screen.blit(prev_surf, (0, 0))

            alpha += 255 * dt
            shade.set_alpha(alpha)
            self.screen.blit(shade, (0, 0))

            self.update_display()

        back = pygame.image.load("images/win1.png")
        age = 0
        alpha = 255
        looper = True
        etc = pygame.image.load("images/etc_light.png")
        while looper:
            events, dt = self.get_events()
            age += dt
            self.screen.blit(back, (145, 0))
            if age > 3 and age%1 < 0.7:
                self.screen.blit(etc, (c.WINDOW_WIDTH//2 - etc.get_width()//2, c.WINDOW_HEIGHT - etc.get_height()))

            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN: looper = False

            shade.set_alpha(alpha)
            self.screen.blit(shade, (c.centerx, c.centery))
            alpha -= 255 * dt

            self.update_display()
        alpha = 0
        age = 0

        shade.fill(black)

        while alpha < 255:
            events, dt = self.get_events()
            age += dt
            self.screen.fill(black)
            self.screen.blit(back, (c.centerx, c.centery))

            alpha += 255 * dt
            shade.set_alpha(alpha)
            self.screen.blit(shade, (0, 0))

            self.update_display()
        pygame.quit()
        sys.exit()

    
#Do this later on

    def config_menu(self):
        self.started = False
        
        fullscreen_button = Button(
            pygame.image.load("images/fullscreen_enabled.png"),
            pos=(c.WINDOW_WIDTH//2 + 200, c.WINDOW_HEIGHT - 200),
            disabled_surf=pygame.image.load("images/fullscreen_disabled.png"),
            enabled=False,
            pulse=0, #GETS RID OF THAT ANNOYING MOVING THING, DO NOT DELETE
            on_click=self.toggle_fullscreen_mode,
        )
        colorblind_button = Button(
            pygame.image.load("images/contrast_enabled.png"),
            pos=(c.WINDOW_WIDTH//2 - 200, c.WINDOW_HEIGHT - 200),
            disabled_surf=pygame.image.load("images/contrast_disabled.png"),
            enabled=False,
            pulse=0,
            on_click=self.toggle_colorblind_mode,
        )
        start_button = Button(
            pygame.image.load("images/start_button.png"),
            pos=(c.WINDOW_WIDTH//2, c.WINDOW_HEIGHT - 600),
            on_click=self.start,
            pulse=0,
        )
        music_button = Button(
            pygame.image.load("images/music_enabled.png"),
            pos=(c.WINDOW_WIDTH//2, c.WINDOW_HEIGHT-400),
            disabled_surf=pygame.image.load("images/music_disabled.png"),
            enabled=False,
            on_click=self.toggle_music,
            pulse=0,
        )
        while not self.started:
            events, dt = self.get_events()
            self.screen.fill(black)
            colorblind_button.update(dt, events)
            fullscreen_button.update(dt, events)
            music_button.update(dt, events)
            start_button.update(dt, events)
            fullscreen_button.enabled = self.fullscreen
            colorblind_button.enabled = self.colorblind_mode
            music_button.enabled = self.music_play
            fullscreen_button.draw(self.screen)
            colorblind_button.draw(self.screen)
            music_button.draw(self.screen)
            start_button.draw(self.screen)
            self.update_display()

        if self.fullscreen: self.screen = pygame.display.set_mode((c.WINDOW_WIDTH, c.WINDOW_HEIGHT), flags=pygame.FULLSCREEN)
        else: self.screen = pygame.display.set_mode((c.WINDOW_WIDTH, c.WINDOW_HEIGHT))

    def intro(self):
        if self.music_play:
            pygame.mixer.music.load("sounds/intro.ogg")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        section = pygame.Surface((c.WINDOW_WIDTH, c.WINDOW_HEIGHT//3 + 15)) #Define section area
        sections = [
            section.copy() for _ in range(3)
        ] #Gives me 3 sections for my texts
        for section in sections:
            section.fill(black) #Fill black in all as bg
        age = 0 #Time
        alphas = [
            255 + 500,
            255 + 2000,
            255 + 3500,
        ] #Set alpha values, 0 = transparent, 255 = opaque
        sections[1] = pygame.transform.scale(sections[1], (c.WINDOW_WIDTH, c.WINDOW_HEIGHT//4))
        back = pygame.image.load("images/intro.png") #Intro
        while True:
            events, dt = self.get_events()
            age += dt #Update age of window with delta time
            self.screen.blit(back, (0, 0))
            for i, alpha in enumerate(alphas): #Enumerate is a neat little thing ngl, 2 loops
                alphas[i] -= 500 * dt
                sections[i].set_alpha(alpha)
            x = 0
            y = 0
            for section in sections:
                if age > 13: #Change to change the speed of reveal
                    section.set_alpha(255 * (age - 13))
            for section in sections:
                self.screen.blit(section, (x, y))
                y += c.WINDOW_HEIGHT//3
                if y > c.WINDOW_HEIGHT//2:
                    y -= 100
            self.update_display()
            if age > 14:
                break
        #Stack overflow thank you

    def directions(self):
            shade = pygame.Surface((c.WINDOW_WIDTH, c.WINDOW_HEIGHT))
            shade.fill(black)
            back = pygame.image.load("images/instructions.png")
            age = 0
            alpha = 255
            looper = True
            etc = pygame.image.load("images/enter_to_continue.png")
            while looper: #makes the enter to continue thingy blink
                events, dt = self.get_events()
                age += dt
                self.screen.blit(back, (0, 0))
                if age > 3 and age%1 < 0.7:
                    self.screen.blit(etc, (c.WINDOW_WIDTH//2 - etc.get_width()//2, c.WINDOW_HEIGHT - etc.get_height()))

                for event in events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN: looper = False #Escape Mechanism

                shade.set_alpha(alpha)
                self.screen.blit(shade, (0, 0))
                alpha -= 255 * dt

                self.update_display()
            alpha = 0
            age = 0 #Reset

            while alpha < 255: #This animates the screen smoothly using alpha
                events, dt = self.get_events()
                age += dt
                self.screen.fill(black)
                self.screen.blit(back, (0, 0))



                shade.set_alpha(alpha)
                self.screen.blit(shade, (0, 0))
                alpha += 500 * dt

                self.update_display()


#Button stuff

    def toggle_colorblind_mode(self):
        self.colorblind_mode = not self.colorblind_mode

    def start(self):
        self.started = True

    def toggle_fullscreen_mode(self):
        self.fullscreen = not self.fullscreen

    def update_display(self):
        pygame.display.flip()

    def toggle_music(self):
        self.music_play = not self.music_play


#End of button stuff

    def get_events(self): #Gives me the event and delta time
        events = pygame.event.get()
        for event in events:
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or (event.type == pygame.QUIT):
                pygame.quit()
                sys.exit()
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_r and self.started): #Delete when release
                self.init() #issue: if skipped intro, then when died in game, it returns back to intro instead of title screen.
                self.main()
        dt = self.clock.tick(90)/1000 #Every 90 frames return delta time, divided by 1000
        return events, dt

    def spawn_scuttle(self, left=True): #Land enemie
        y = c.WINDOW_HEIGHT * 0.73
        if not left: #Literally default left, because I'm leftist
            self.enemies.append(Scuttle(self, (c.WINDOW_WIDTH + 1000, y), (-1, 0)))
            self.particles.append(WarningParticle((c.WINDOW_WIDTH - 50, y)))
        else:
            self.enemies.append(Scuttle(self, (-1000, y), (1, 0)))
            self.particles.append(WarningParticle((50, y)))

    def spawn_orb(self, left=True): #Air enemie
        if left:
            self.enemies.append(Orb(self, (-50, -random.random() * 200 - 50), direction=(1, 0)))
        else:
            self.enemies.append(Orb(self, (c.WINDOW_WIDTH + 50, -random.random() * 200 - 50), direction=(-1, 0)))

    def game_start(self): #Running in the 90s sus version
        self.game_started = True
        self.start_pos = self.xpos
        pygame.mixer.music.fadeout(1)
        if self.music_play:
            #BGM Start
            self.music = pygame.mixer.music.load("sounds/music.ogg")
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play()

    def init(self): #Every single init
        #Variable Def
        self.day = 1
        self.xpos = 0
        self.speed = 500
        self.since_orb = 0

        self.ccs_surf = None

        self.start_pos = 0
        self.courier_new = pygame.font.Font("fonts/cour.ttf", 20)

        self.shade = pygame.Surface((c.GAME_WIDTH, c.GAME_HEIGHT)) #Cover the entire screen
        self.shade.fill(black)
        self.shade_alpha = 255 #Make transparent surface

        self.really_lost = False

        self.game_started = False

        #Load Title Screen
        self.title = pygame.image.load("images/title.png")
        self.title_pos = int(c.WINDOW_HEIGHT * 0.3)

        #All Sounds
        self.nope_sound = pygame.mixer.Sound("sounds/nope.wav")
        self.nope_sound.set_volume(0.2)
        self.restart_sound = pygame.mixer.Sound("sounds/restart.wav")
        self.restart_sound.set_volume(0.5)
        self.rewind_sound = pygame.mixer.Sound("sounds/rewind.wav")
        self.pickup_battery = pygame.mixer.Sound("sounds/pickup_battery.wav")
        self.pickup_battery.set_volume(0.1)
        self.pickup_kunai = pygame.mixer.Sound("sounds/pickup_kunai.wav")
        self.pickup_kunai.set_volume(0.1)
        self.laser_sound = pygame.mixer.Sound("sounds/laser.wav")
        self.laser_sound.set_volume(0.75)
        self.explosion_sound = pygame.mixer.Sound("sounds/explosion.wav")
        self.shoot_kunai_sound = pygame.mixer.Sound("sounds/throw_kunai.wav")
        self.shoot_kunai_sound.set_volume(0.2)
        self.laser_aim = pygame.mixer.Sound("sounds/laser_aim.wav")
        self.laser_aim.set_volume(0.2)
        self.kunai_hit = pygame.mixer.Sound("sounds/kunai_hit.wav")
        self.kunai_hit.set_volume(0.8)
        self.jump_sound = pygame.mixer.Sound("sounds/jump.wav")
        self.jump_sound.set_volume(0.3)
        self.player_hurt = pygame.mixer.Sound("sounds/hurt.wav")
        self.mrew = pygame.mixer.Sound("sounds/mrew.wav")
        self.mrew.set_volume(0.0)
        self.death = pygame.mixer.Sound("sounds/death.wav")
        self.death.set_volume(0.8)


        self.press_e= pygame.image.load("images/press_e.png")

        self.horizon = c.GAME_HEIGHT * 0.6
        self.floor = c.GAME_HEIGHT - 140
        self.game_time = 0

        self.player = Player(self)
        self.player.position = Pose((c.GAME_WIDTH//2, -100))

        #See my grade 9 Final Project, Dankamu function

        self.particles = []
        self.enemies = []

        #All Images

        self.background = pygame.image.load("images/bakground.png")
        self.background_reflection = pygame.transform.flip(self.background, 0, 1) #keep to avoid dragging sprites
        self.background_buildings = pygame.image.load("images/background_buildings.png")
        self.background_buildings.set_colorkey((255, 255, 255))
        self.foreground_buildings = pygame.image.load("images/foreground_buildings.png")
        self.foreground_buildings.set_colorkey((94, 84, 40))
        self.sun = pygame.image.load("images/sun.png")
        self.train = pygame.image.load("images/train.png")

        self.blue = pygame.image.load("images/red.png") #About the variable, let me explain
        self.blue = pygame.transform.scale(self.blue, (c.GAME_WIDTH, c.GAME_HEIGHT))
        self.blue_color = self.blue.get_at((0, 0)) #Returns a copy of the RGBA value
        #This is slower than PixelArray, but generates better quality and res

        self.clock = pygame.time.Clock()
        self.fps_font = pygame.font.Font("fonts/cour.ttf", 12)
        self.fpss = [0]
        
        #More variables

        self.lightener = pygame.Surface((c.GAME_WIDTH, c.GAME_HEIGHT))
        self.lightener.fill((255, 255, 255))#Lighter alpha shade, 遮罩
        self.lightener.set_alpha(30)#The original idea is to go from here to black but it kinda failed
        self.day_when_rewind = 1

        self.rewinding = False

        self.shake_amp = 0
        self.shake_direction = Pose((1, 0))
        self.since_shake = 0

        #Loadup stats bar

        self.kunai_ui = pygame.image.load("images/kunai_ui.png")
        self.pickups = [] #All collectible items
        self.quad_ui = pygame.image.load("images/charge_quadrant_one.png")
        self.quad_color_ui = pygame.image.load("images/charge_quad_color.png")
        self.center_ui = pygame.image.load("images/charge_center.png")
        self.center_color_ui = pygame.image.load("images/charge_center_color.png")
        self.charge_back_ui = pygame.image.load("images/charge_background.png")
        self.charge_glow = pygame.image.load("images/charge_glow.png")

        self.since_scuttle = 0 #Time since enemy, NOT stats bar


    def get_offset(self): #MC Shake offset calculation, this belongs in PRIMITIVES.PY but importing class-dep args is pain

        if self.shake_direction.magnitude() <1:
            return (0, 0)
        return (self.shake_direction * (1/self.shake_direction.magnitude()) * self.shake_amp * math.cos(self.since_shake*20)).get_position()

    def update_background(self, dt, events):
        self.since_shake += dt
        self.shake_amp *= 0.01**dt #This is barely contained by float as dt gets bigger
        self.shake_amp = max(0, self.shake_amp - 5*dt)

        self.xpos += self.speed * dt #Updates player position, irrelevant to bg
        self.game_time += dt - dt*0.8*self.rewinding
        if self.game_started:
            if not self.rewinding:
                self.day -= (1/36.5)*dt 
            else:
                pace = (1 - self.day_when_rewind)/3
                self.day += pace*dt 
            if self.rewinding and self.day >= 1:
                self.stop_rewinding() 
            if self.day < 0:
                self.day = 0 

        lightness = self.day #Gradually less light
        bc = tuple([max(0, int(item * lightness)) for item in self.blue_color])
        self.blue.fill(bc)

        if self.rewinding and self.speed > 100: #Rewinding train speed
            self.speed = max(self.speed - 2000 * dt, 50)
        if not self.rewinding:
            self.speed = min(self.speed + 2000 * dt, 500)

    def update_fps(self, dt, events):
        self.fpss.append(1/dt)
        self.fpss = self.fpss[-100:]

    def draw_fps(self, surface): #Test only, make empty when release
        fps = int(round(sum(self.fpss)/len(self.fpss), 0))

        color = black
        if self.day < 0.2:
            color = (255, 255, 255)

        label = self.fps_font.render("FPS: MIN   AVG   MAX", 0, color)

        maxfps = max(self.fpss)
        minfps = min(self.fpss)
        text = f"{int(minfps)} |  {fps} |  {int(maxfps)}"
        surf = self.fps_font.render(text, 0, color)
        surface.blit(label, (c.GAME_WIDTH - label.get_width() - 10, 10))
        surface.blit(surf, (c.GAME_WIDTH - surf.get_width() - 10, 10 + label.get_height()))

    def draw_background(self, surf, offset=(0, 0)):
        bgh = self.background.get_height() #Background Height
        margin = max(0, bgh - c.GAME_HEIGHT)
        bgy = -margin * self.day
        ba = pygame.Rect((0, -bgy, c.GAME_WIDTH, self.horizon))
        surf.blit(self.background, (0, 0), area=ba) #Stick BG
        bra = pygame.Rect((0, margin * (1 - self.day) + (c.GAME_HEIGHT - self.horizon)/2, c.GAME_WIDTH, c.GAME_HEIGHT - self.horizon))
        surf.blit(self.background_reflection, (0, self.horizon), area=bra)


        #Sun timer

        sun_peak_height = self.sun.get_height() * 1.5
        sx = c.GAME_WIDTH//2 - self.sun.get_width()//2 + offset[0]
        sy = int(self.horizon - sun_peak_height * self.day + offset[1])
        sa = (0, 0, self.sun.get_width(), int(sun_peak_height * self.day)) #Sun area
        surf.blit(self.sun, (sx, sy), area=sa)


        #Background Building track
        bbw = self.background_buildings.get_width()
        bbh = self.background_buildings.get_height()
        bbx = int((-self.xpos * 0.1) % bbw - bbw + offset[0])
        bby = int(self.horizon + offset[1])
        while bbx < c.GAME_WIDTH:
            surf.blit(self.background_buildings, (bbx, bby - bbh))
            bbx += bbw


        #Foreground building track
        fbw = self.foreground_buildings.get_width()
        fbx = int((-self.xpos * 0.7) % fbw - fbw + offset[0])
        while fbx < c.GAME_WIDTH:
            surf.blit(self.foreground_buildings, (fbx, 300))
            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(fbx, 570, c.WINDOW_WIDTH, c.WINDOW_HEIGHT))
            fbx += fbw

        surf.blit(self.blue, (0, 0), special_flags=pygame.BLEND_RGB_ADD)

        #Draw trains

        train_center_x = c.GAME_WIDTH//2
        train_spacing = 5
        train_width = self.train.get_width()
        train_start_x = train_center_x - self.train.get_width()//2 + offset[0] - train_spacing - train_width

        if self.colorblind_mode:
            surf.blit((self.lightener), (0, 0)) #Attempt at higher contrast, didn't work out

        for number in range(3):
            xo, yo = self.get_train_offset(number) #Gets offset for 3 different vars.
            train_x = int(train_start_x + number * train_spacing + number * train_width + xo)
            train_y = int(self.floor - 5 + yo + offset[1])
            surf.blit(self.train, (train_x, train_y), special_flags=pygame.BLEND_MULT) #Put train into canva

    def get_train_number(self, x):
        train_center_x = c.GAME_WIDTH // 2
        train_width = self.train.get_width()
        if x < train_center_x - train_width//2 - 38:
            return 0
        elif x < train_center_x + train_width//2 - 35:
            return 1
        else:
            return 2 #Maximum two trains present

    def get_train_offset(self, number): #Train shake
        xo = -math.sin(self.game_time * 10 + number * 10) * 1.5
        yo = math.cos(self.game_time * 10 + number * 10) * 1.5
        return xo, yo

    def start_rewind(self):
        if self.music_play:
            pygame.mixer.music.fadeout(250)
        self.rewind_sound.play()
        self.rewinding = True
        self.player.start_tractor_beam()
        self.day_when_rewind = self.day
        if self.day_when_rewind == 1:
            self.day_when_rewind = 0.999 #Can't rewind when =1
        for i in range(1000):
            self.particles.append(RewindParticle(self))
        self.particles.append(SunTint(duration=3, alpha=100))
        self.destroy_all_enemies(silent=True)

    def destroy_all_enemies(self, silent=False):
        for enemy in self.enemies:
            if not enemy.destroyed:
                enemy.reward = 0
                enemy.destroy(silent=silent)

    def stop_rewinding(self):
        if self.music_play:
            pygame.mixer.music.rewind() #Nice little thingy, should've known this last year
            pygame.mixer.music.play()

        self.mrew.play()
        self.restart_sound.play()
        self.rewinding = False
        self.day = 1
        self.player.end_tractor_beam()
        self.particles.append(SunExplosion(self))
        self.player.charge = 0

    def lose(self):
        self.death.play()
        if self.lost:
            return
        self.particles.append(SunExplosionLong(self, duration=6, color=(255, 0, 0), callback=self.really_lose))
        self.lost = True
        self.last_distance = self.xpos #Log for title screen

    def get_train_offset_from_x(self, x): #Additional offset for shaking
        return self.get_train_offset(self.get_train_number(x))

    def draw_hud(self, surf, offset=(0, 0)): #Kunai + Energy + Distance
        x = c.GAME_WIDTH//2 - (self.player.ammo - 1) * 10 - 18
        y = c.GAME_HEIGHT - 45
        for i in range(self.player.ammo):
            surf.blit(self.kunai_ui, (x, y))
            x += 20 #Change for distance between Kunai UIs

        charge_per_section = 25 #/100
        max_charge = charge_per_section * 5 #The other one is the center
        quads = self.player.charge//charge_per_section
        remainder = self.player.charge%charge_per_section

        x = c.WINDOW_WIDTH//2 - self.charge_back_ui.get_width()//2
        y = c.WINDOW_HEIGHT - 105 - self.charge_back_ui.get_height()//22

        quad = self.quad_ui.copy()
        quad_color = self.quad_color_ui.copy()
        quad_color.set_colorkey(black)
        center_color = self.center_color_ui.copy()
        center_color.set_colorkey(black)
        if quads >= 5:
            glow = self.charge_glow.copy() #Glowing stuff
            dark = pygame.Surface(glow.get_size())
            dark.fill(black)
            dark.set_alpha(50 + 128 * math.sin(self.game_time*6))
            glow.blit(dark, (0, 0))
            surf.blit(glow, (x - glow.get_width()//2 + quad.get_width()//2, y), special_flags=pygame.BLEND_ADD)
            if not self.rewinding and self.game_time%1 < 0.7: #Remind to press E
                pos = c.WINDOW_WIDTH//2 - self.press_e.get_width()//2, y - 28
                surf.blit(self.press_e, pos)
        surf.blit(self.charge_back_ui, (x, y))
        for i in range(4):
            if i >= quads:
                break
            surf.blit(quad, (x, y)) #Same surface
            quad = pygame.transform.rotate(quad, -90)
            quad_color = pygame.transform.rotate(quad_color, -90)
        if quads < 4: #Charge prev quad as gain charge
            quad_color.set_alpha(remainder/charge_per_section * 255)
            surf.blit(quad_color, (x, y))
        elif quads < 5: #Fake charge center as charge = 4
            center_color.set_alpha(remainder/charge_per_section*255)
            surf.blit(center_color, (x, y))
        elif quads >= 5: #Charge center
            surf.blit(self.center_ui, (x, y))

        pixels = self.xpos
        if not self.game_started and self.last_distance: #Post-death
            pixels = self.last_distance
        miles = round((100000 - pixels)/1000, 1) #Round remaining distance/1000 to 1 decimal place
        if not self.game_started and not self.last_distance: #First play
            miles = 100
        context_string = f"Last run:"
        ccs_string = self.courier_new.render(f"{miles}", 1, (255, 255, 255))
        if not self.ccs_surf: #Prevent double render
            self.ccs_surf = self.courier_new.render(" miles to city center", 1, (255, 255, 255))
        surf.blit(ccs_string, (c.WINDOW_WIDTH - ccs_string.get_width() - self.ccs_surf.get_width() - 5, c.WINDOW_HEIGHT - ccs_string.get_height() - 3))
        surf.blit(self.ccs_surf, (c.WINDOW_WIDTH - self.ccs_surf.get_width() - 5, c.WINDOW_HEIGHT - self.ccs_surf.get_height() - 3))

        if self.last_distance and not self.game_started: #Post-death display prev score, overwrite
            cx_string = self.courier_new.render(context_string, 1, (255, 255, 255))
            surf.blit(cx_string, (c.WINDOW_WIDTH - cx_string.get_width() - 5, c.WINDOW_HEIGHT - cx_string.get_height() - 19))




    def get_multiplier(self): #Increase difficulty of game as time increases
        return ((self.xpos - self.start_pos)/14000 + 3)/3

    def main(self): #THE NON IMPOSTOR
        self.lost = False
        self.clock.tick(120) #Change for cap FPS

        while True: #Game loop
            events, dt = self.get_events()
            if dt > 1/20: #FPS cap
                dt = 1/20
            self.update_background(dt, events)
            self.update_fps(dt, events)

            if not self.game_started: #Title screen bg speed
                self.speed = 100

            self.shade_alpha -= 1500 * dt #Screen transparency, decrease over time

            if self.game_started:
                keep_particles = [] #List of particles left
                for particle in self.particles:
                    particle.update(dt, events)
                    if not particle.destroyed:
                        keep_particles.append(particle)
                self.particles = keep_particles #Refresh
                if self.lost: #This gives about 0.01 miliseconds of grace because it comes before the update variable
                    dt *= 0.01
                    events = [event for event in events if event.type != pygame.KEYDOWN and event.type != pygame.MOUSEBUTTONDOWN]
                self.player.update(dt, events)
                for pickup in self.pickups[:]:
                    pickup.update(dt, events)
                for enemy in self.enemies[:]:
                    enemy.update(dt, events) #There's no point in taking events, delete if never used until release.
                    if (enemy.position - self.player.position).magnitude() > c.WINDOW_WIDTH * 3:
                        self.enemies.remove(enemy) #Delete enemy if too far away from player

                #Enemy spawning
                self.since_scuttle += dt
                self.since_orb += dt
                if self.since_scuttle > 3.5 / self.get_multiplier():
                    self.since_scuttle = 0
                    self.spawn_scuttle(random.choice([0, 1])) #Direction

                if self.get_multiplier() > 1.4: #Change to make orbs spawn earlier
                    if self.since_orb > 8 / self.get_multiplier():
                        has_left = False
                        has_right = False
                        for enemy in self.enemies:
                            if type(enemy) == Orb:
                                if enemy.direction.x < 0:
                                    has_right = True
                                else:
                                    has_left = True
                        if not has_left and not has_right:
                            self.spawn_orb(random.choice((1, 0))) #Random if none
                            self.since_orb = 0
                        elif not (has_left and has_right):
                            self.spawn_orb(has_right) #If only one side, then spawn on the empty side
                            self.since_orb = 0

            offset = self.get_offset()


            #Drawing stuff

            self.draw_background(self.screen, offset)
            self.draw_hud(self.screen)
            for pickup in self.pickups:
                pickup.draw(self.screen, offset)
            for enemy in self.enemies:
                enemy.draw(self.screen, offset)
            for particle in self.particles[:]:
                particle.draw(self.screen, offset)
            self.player.draw(self.screen, offset)
            self.draw_fps(self.screen) #Delete when release

            x = c.GAME_WIDTH//2 - self.title.get_width()//2
            y = int(c.GAME_HEIGHT * 0.3) - self.title.get_height()//2
            self.screen.blit(self.title, (x, y))

            if self.game_started:
                self.title_pos -= 1000 * dt
                self.title.set_alpha(self.title_pos * 255 / c.GAME_HEIGHT / 0.3) #Gradual fade

            if self.shade_alpha > 0: #Shadow, see projectile.py
                self.shade.set_alpha(self.shade_alpha)
                self.screen.blit(self.shade, (0, 0))

            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if not self.game_started: #Title screen
                            self.game_start()

            if self.day <= 0: #Lose condition
                self.lose()

            self.update_display()
            if self.really_lost:
                break

            if self.xpos >= 100000: #Win condition
                self.victory_screen(self.screen.copy())

    def really_lose(self):
        self.really_lost = True
        

    def shake(self, direction=None, amt=15): #Hurt animation
        if amt < self.shake_amp:
            return
        else:
            self.shake_amp = amt
        if direction and Pose(direction).magnitude() > 0:
            self.shake_direction = Pose(direction)
        else:
            self.shake_direction = Pose((1, 1))
        self.since_shake = 0


dir = True #Edit for not insta start
if dir:
    Game()