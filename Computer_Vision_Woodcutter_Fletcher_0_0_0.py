
#main.py
import cv2 as cv
import numpy as np
import os
from windowcapture import WindowCapture
from vision import Vision
import pyautogui
from pyHM import Mouse
import time
from action import Action



# initialize the WindowCapture class
wincap = WindowCapture('Runelite - Vessacks')


# initialize the Vision class
log_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\Woodcutter Fletcher\\image library\\log.png')
stump_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\Woodcutter Fletcher\\image library\\stump.png')
tree_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\Woodcutter Fletcher\\image library\\tree.png')
knife_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\Woodcutter Fletcher\\image library\\knife.png')

#initialize the action class
log_action = Action('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\Woodcutter Fletcher\\image library\\log.png')
tree_action = Action('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\Woodcutter Fletcher\\image library\\tree.png')
knife_action = Action('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\Woodcutter Fletcher\\image library\\knife.png')

loop_time = time.time()
confidence_counter = 0 #every time it thinks we're out of combat, the counter goes up. when it hits a threshold, we find a new thing to fight
heelCooler = time.time() # used to wait a bit before reclicking an enemy

#I need these definitions up here to prevent reference before assignment
print('welcome to woodcutter/fletcher! I will find whatever tree you have fed me an image of, cut it, and fletch it.')

startTime = time.time()
STOP_AFTER = float(input('please type the number of seconds you would like to run the script, then press enter. '))
CUT_RECLICK_TIMER = 10
CUT_LOGOUT_TIMER = 60
SLEEP_TIMER = 10
MAX_LOGS = 20
FLETCH_RECLICK_TIMER = 20

def cutLoop():
    #take a screenshot
    screenshot = wincap.get_screenshot()

    # get an updated image of the game and look for object of interest
    treeWindow = tree_vision.find(screenshot, 0.90, 'rectangles')

    #this holds up the loop until tree != [], ie it's found a tree
    while treeWindow == []:
        print('looking for a tree')
        screenshot = wincap.get_screenshot()
        treeWindow = tree_vision.find(screenshot, 0.90, 'rectangles')

    #once it's found a tree,it translates to screen coords and clicks
    treeScreen = wincap.get_screen_position(treeWindow)
    treeClickpoint = tree_action.click(treeScreen)
    print('clicked a tree')
    #time.sleep(5) #need to wait a bit before seeing if I'm not woodcutting
    #print('sleeping 5s before checking whether it is woodcutting')

    
    log_time = time.time()
    loop_time = time.time() #need for the FPS calc
    numLogs = 0 #need it for the log sameness calc
    while True:
        screenshot = wincap.get_screenshot()
        logWindowAll = log_vision.find(screenshot, 0.90, debug_mode= 'rectangles', return_mode = 'allPoints')
        
        #log change timer
        if numLogs != len(logWindowAll): #if the number of logs has changed, reset the change timer
            log_time = time.time()

        #resets logs to len(logWindowAll)
        numLogs = len(logWindowAll)

        #looks at log change timer, determines if it should reclick
        if time.time() - log_time > CUT_RECLICK_TIMER: #if the number of logs hasn't changed in 10s, attempt reclick
            print('log count unchanged for %s s, attempting reclick' % CUT_RECLICK_TIMER)
            treeWindow = tree_vision.find(screenshot, 0.95, 'rectangles')
            if treeWindow != []:
                treeScreen = wincap.get_screen_position(treeWindow)
                treeClickpoint = tree_action.click(treeScreen)
                print('reclicked a tree, sleeping %s s, log timer not reset' %SLEEP_TIMER)
                time.sleep(SLEEP_TIMER)
                #log_time = time.time()

        #irrecoverable misclick identifier
        if time.time() - log_time > CUT_LOGOUT_TIMER:
            print('log timer %s, logged out for safety' % CUT_LOGOUT_TIMER)
            exit()

        #counts logs and breaks when it has enough      
        if numLogs > MAX_LOGS: #this loop waits until it sees at least X logs
            print('I see at least %s logs, going to fletching' % MAX_LOGS)
            break
     
        # debug the loop rate
        print('Logs = ' + str(len(logWindowAll)) + '| runTime = '+str(round(time.time() - startTime))+ ' | log_timer = '+ str(time.time() - log_time) + '| FPS {}'.format(1 / ((time.time() - loop_time))))
        loop_time = time.time()

        # press 'q' with the output window focused to exit.
        # waits 1 ms every loop to process key presses
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            exit()
    

def fletchLoop():
    #take a screenshot
    screenshot = wincap.get_screenshot()

    # get an updated image of the game and look for object of interest
    logWindow = log_vision.find(screenshot, 0.90)
    logWindowAll = log_vision.find(screenshot, 0.90, debug_mode= 'rectangles', return_mode = 'allPoints')
    knifeWindow = knife_vision.find(screenshot, 0.90, 'rectangles')

    if logWindow != [] and knifeWindow != []:
        knifeScreen = wincap.get_screen_position(knifeWindow)
        logScreen = wincap.get_screen_position(logWindow)
        logClick = log_action.click(logScreen,speed=.4)
        print('clicked a log at %s' %logClick)
        time.sleep(np.random.normal(.6,.1))
        knifeClick = knife_action.click(knifeScreen, speed=.2)
        print('clicked a knife at %s' % knifeClick)
        time.sleep(np.random.normal(1,.1))
        pyautogui.keyDown('space')
        time.sleep(np.random.normal(.15,.03))
        pyautogui.keyUp('space')
        print('fletching...')

    else: 
        print('error: missing log or knife, trying woodcutting')
        return
    
    numLogs= 0 #it's not really zero, but I need to give it a value to prevent referencing before assignment
    loop_time = time.time()
    while True:
        screenshot = wincap.get_screenshot()
        logWindowAll = log_vision.find(screenshot, 0.9, debug_mode = 'rectangles', return_mode = 'allPoints')
            
        #log change timer
        if numLogs != len(logWindowAll): #if the number of logs has changed, reset the change timer
            log_time = time.time()

        #resets logs to len(logWindowAll)
        numLogs = len(logWindowAll)

        if time.time() - log_time > FLETCH_RECLICK_TIMER: #if the number of logs hasn't changed in CUT_RECLICK_TIMER seconds, attempt reclick
            print('log_timer unchanged in %s, going back to cutting' %FLETCH_RECLICK_TIMER)
            break #i used to try a reclick, but that caught. now i just send it back to cutting
            '''
            # get an updated image of the game and look for object of interest
            logWindow = log_vision.find(screenshot, 0.90)
            logWindowAll = log_vision.find(screenshot, 0.90, debug_mode= 'rectangles', return_mode = 'allPoints')
            knifeWindow = knife_vision.find(screenshot, 0.90, 'rectangles')
            #if its found logs and knives, click'em
            if logWindow != [] and knifeWindow != []:
                knifeScreen = wincap.get_screen_position(knifeWindow)
                logScreen = wincap.get_screen_position(logWindow)
                logClick = log_action.click(logScreen,speed=.4)
                print('clicked a log at %s' %logClick)
                time.sleep(np.random.normal(.6,.1))
                knifeClick = knife_action.click(knifeScreen, speed=.2)
                print('clicked a knife at %s' % knifeClick)
                time.sleep(np.random.normal(1,.1))
                pyautogui.keyDown('space')
                time.sleep(np.random.normal(.15,.03))
                pyautogui.keyUp('space')
                print('fletching...')
            '''
        if numLogs == 0: #if you're out of logs, go back to fletching
            print('I see no logs, going back to cutting')
            break

        # debug the loop rate
        print('Logs = ' + str(len(logWindowAll)) + '| runTime = '+str(round(time.time() - startTime))+ '| FPS {}'.format(1 / ((time.time() - loop_time))))
        loop_time = time.time()
        

        # press 'q' with the output window focused to exit.
        # waits 1 ms every loop to process key presses
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            exit()
    



while True:
    runTime = time.time() - startTime
    if runTime > STOP_AFTER:
        print('completed run. final runtime was %s' % runTime)
        exit()
    cutLoop()
    fletchLoop()

