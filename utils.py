import os
import cv2
from datetime import datetime
import time

class Utils:
    @staticmethod    
    def append_date_text(img):

        #text to display
        text = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

        # font 
        font = cv2.FONT_HERSHEY_COMPLEX
        
        # org 
        org = (50, 50) 
        
        # fontScale 
        fontScale = 1
        
        # Blue color in BGR 
        color = (210, 210, 210) 
        
        # Line thickness of 2 px 
        thickness = 2
        cv2.putText(img, text, org, font, fontScale, color, thickness)

        return img

    @staticmethod
    def increase_brightness(img, value=50):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)

        lim = 255 - value
        v[v > lim] = 255
        v[v <= lim] += value

        final_hsv = cv2.merge((h, s, v))
        img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        return img

    @staticmethod
    def put_FPS_Text(frame, start_time):
        fps = 1.0 / (time.time() - start_time)
        
        #text to display
        fps_text="FPS: %.2f" % fps

        # font 
        font = cv2.FONT_HERSHEY_COMPLEX
        
        # org 
        org = (50, 100) 
        
        # fontScale 
        fontScale = 1
        
        # Blue color in BGR 
        color = (210, 210, 210) 
        
        # Line thickness of 2 px 
        thickness = 2

        cv2.putText(frame, fps_text, org, font, fontScale, color, thickness)
        
    @staticmethod
    def isVideoFile(inputString):
        return True if inputString.lower().endswith(('.mp4', '.mov', '.avi', '.webm', '.mkv', '.flx')) else False

    @staticmethod
    def isIPCam(inputString):
        return True if inputString.lower().startswith(('rtsp://', 'http://', 'https://')) else False

    @staticmethod
    def isImageFile(inputString):
        return True if inputString.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.bmp')) else False

    @staticmethod
    def makeDirectoryIfNotExist(dirname):
        if not os.path.exists(dirname):
            os.makedirs(dirname)