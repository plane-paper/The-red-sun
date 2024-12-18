# The Red Sun

## Installation & User Manual

**Before use: Download (git clone or through downloading a zip file) all files in this repository, <ins>and</ins> install python and requirements.txt**

Please go to your command prompt, and enter:

>python3

Install Python as necessary. Then:

>pip3 install -r SomeDisk:/someUser/somedirectory/requirements.txt

**Then run the game**, either through command prompt:

>python3 SomeDisk:/someUser/somedirectory/game.py

**Or** by directly clicking on game.py in the downloaded files

*Yes this game has a plot. Try and look for it yourself, I'm not gonna say anything.

[Warning]: The game requires 2GB of RAM.

[Warning]: When on low FPS (<20), the game might have issues running. For example, projectiles
		might miss enemies when a hit should register, the player might glitch through the
		floor, etc. Please refer to the instruction of your hardware provider to increase
		the FPS in order to have a better experience.

[Warning]: Some violence could be seen in the game.

## Troubleshooting
Ensure you are running the game through:
>python3 Disk:/User/directory/game.py

Then, assess the error message. There could be countless, here are a few common ones:

### Function/File missing/not found
You are missing a file that contains a vital function from the game. Ensure that **all files from the repository** is downloaded in the same directory and **unzipped**.

### PyGame/Other library is not defined (in line 1-10)
Pygame or the library in question is not installed properly. Several issues could cause this:
- Improper pip installation. Run:
>pip install libraryName

In your command prompt, then try again
- PATH issues. Ensure the path that pip is installed in is included in your computer's environment variables. Access your environment variables in the control panel.

### Specific line issues
This may be an issue specific to your runtime environment. Email r38su@uwaterloo.ca with your issue.

## Game Preview

### **Title Screen**

![Title Screen](./readme-assets/pic07.jpg "Title Screen")

### Sample Gameplay

![Sample Gameplay 1](./readme-assets/pic08.jpg "Sample Gameplay 1")

![Sample Gameplay 2](./readme-assets/pic09.jpg "Sample Gameplay 2")

![Sample Gameplay 3](./readme-assets/pic10.jpg "Sample Gameplay 3")
