#!/usr/bin/env python

import cv2

class motion():
    '''
    motion detection
        1. Captrure images
        2. Analysis the sequence of the images
        3. Show images
        4. Alarm while motion detected
    '''
    def __init__(self):
        '''
        Initialize required objects
        '''
        # Construct the camera captddure object
        from camera import camera
        self.cam = camera()
        # Using container to store images
        from container import dataContainer
        self.imgContainer = dataContainer()
        # Contruct a alarm object
        from alarm import alarm
        self.eventAlarm = alarm()
        # Construct the image processing strategy
        from strategy import strategyConstructor
        self.strategyConstruction = strategyConstructor(self.eventAlarm)
        # check if X11 DISPLAY exist
        self._isgui = self._checkGUI()

    def detect(self):
        '''
        Detection motion from images
        '''
        # Store initial n images to image container
        for i in range(3):
            # Capture a image
            self.fetchImage()

        while True:
            # reset alarm
            self.eventAlarm.reset()
            # Runing the image process strategies
            for strategy in self.strategyConstruction.listStrategy():
                strategy.execute(self.imgContainer)
            # Display image
            self.showImage()
            # Check alarm
            if self.eventAlarm.isalarm():
                self.eventAlarm.alarm()
            # Get keyboard input
            input_ch = self.getKeyboard()
            # Check if 'ESC'
            if (input_ch == 27):
                break
            # Capture new image
            self.fetchImage()
        # Close window and exit the program
        self.closeWindow()

    def fetchImage(self):
        '''
        Capture an image from camera and save to the image container
        '''
        ret, image = self.cam.read()
        self.imgContainer.insert ({"Original": image })

    def showImage(self):
        '''
        Display the images
        '''
        if (self._isGUI()):
            import numpy as np
            # concatenate two images horizontally
            vis = np.concatenate( \
                    (self.imgContainer.pop("Original") , self.imgContainer.pop("Process") ), \
                    axis=1)
            cv2.namedWindow("Image", cv2.WND_PROP_FULLSCREEN) 
            # Set fullscreen window
            cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.cv.CV_WINDOW_FULLSCREEN)
            # Show image
            cv2.imshow ("Image", vis)
        else:
            self.imgContainer.pop("Original")
            self.imgContainer.pop("Process")

    def getKeyboard(self):
        '''
        Return keyboard input
        '''
        return 0xFF & cv2.waitKey(1)

    def closeWindow(self):
        '''
        Close all cv2 window
        '''
        if (self._isGUI()):
            cv2.destroyAllWindows()
        else:
            exit()

    def _checkGUI(self):
        '''
        check if X11 DISPLAY exist
        Retrun:
            [True|False]: X11 DISPLAY exist or not
        '''
        import os
        return os.environ.has_key('DISPLAY')

    def _isGUI(self):
        '''
        Return X11 DISPLAY exist
        Retrun:
            [True|False]: X11 DISPLAY exist or not
        '''
        return self._isgui

# Run the program
if __name__ == "__main__":
    Motion = motion()
    Motion.detect()
