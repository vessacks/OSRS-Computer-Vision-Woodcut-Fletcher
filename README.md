# OSRS-Computer-Vision-Woodcut-Fletcher
Run Computer_Vision_Woodcutter_Fletcher_0_0_0.py and follow the prompts to set run duration, cycle duration, etc
vision.py looks for and identifies objects of interest (logs, trees, etc)
wincap.py creates screenshots for vision.py to look through
action.py generates randomized clicks on those objects of interest. Each session it generates a click profile to follow for that session only to prevent comparison across sessions
windmouse.py generates randomized mouse movements between clickpoints. I'm using windmouse under GNU licence, and have modified it to allow for different speeds of travel


