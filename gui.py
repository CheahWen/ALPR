import os,sys,inspect
import traceback

import concurrent.futures
from datetime import datetime
import time

import logging
logging.basicConfig(filename=f"LogFiles/Log.{datetime.today().strftime('%Y-%m-%d')}.log",
                        filemode='a',
                        format='%(asctime)s %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)

import cv2
# import torch
import numpy as np
import base64

# from lpr_op import LPR_OP
from db import DB
from lp_det import PlateDetector
from ocr_op import OCR_OP
from videocaptureasync import VideoCaptureAsync
from utils import Utils

from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image 


from kivy.graphics.texture import Texture
from kivy.app import App

from kivy.core.window import Window
import tensorflow as tf

from ConfigParserManager import ConfigParserManager
from LogManager import LogManager

physical_devices = tf.config.experimental.list_physical_devices('GPU')
use_gpu = True if len(physical_devices) > 0 else False

inputSource = ConfigParserManager.getInputSourceConfig()
VideoPlaceHolderSource = ConfigParserManager.getVideoPlaceholderConfig()

class GUI(GridLayout):


    def __init__(self, **kwargs):
        super(GridLayout, self).__init__(**kwargs)
        # check video or image file
        try:
            LogManager.makeLog(message="Opening source file...", type=0)
            if inputSource=="0":
                self.cap=VideoCaptureAsync(src=0)
                self.cap.start()
                if not self.cap.cap.isOpened():
                    raise Exception("Cannot open the webcam!")

            elif Utils.isVideoFile(inputSource) or Utils.isIPCam(inputSource):
                self.cap=VideoCaptureAsync(src=inputSource)
                self.cap.start()
                if not self.cap.cap.isOpened():
                    raise Exception("Cannot open the source! Please double check the source: {}".format(inputSource))

            elif Utils.isImageFile(inputSource):
                self.cap=cv2.imread(inputSource)

            else:
                raise Exception("Invalid input source! Please double check the source: {}".format(inputSource))
            
            LogManager.makeLog(message="Successfully opening source file...", type=0)

        except:
            LogManager.makeLog(message=f"LOAD_SOURCE_FAILED: File {inspect.stack()[1][1]}, Line {inspect.stack()[1][2]}:Invalid input source! Please double check the source: {inputSource}", type=1)
            LogManager.makeLog(message=f'{traceback.format_exc()}', type=1)
            os._exit(1)


        self.lp_det=PlateDetector()
        self.ocr_op=OCR_OP()
        self.db=DB()
        self.display_list = []
        self.is_full_screen = False
        self.draw_boxes=True
        self.shouldDisplay=True
        try:
            self.db.loop.run_until_complete(self.db.createPool())
        except:
            LogManager.makeLog(message=f"CONNECT_MYSQL_FAILED: File {inspect.stack()[1][1]}, Line {inspect.stack()[1][2]}:Could not connect to MySQL!", type=1)
            LogManager.makeLog(message=f'{traceback.format_exc()}', type=1)

            os._exit(1)

    def on_drawboxes_active(self, checkbox, value):
        self.draw_boxes=value

    def on_camdisplay_active(self, checkbox, value):
        self.shouldDisplay=value

   

    def toggle_full_screen(self):

        self.is_full_screen = not self.is_full_screen
        setattr(Window, 'fullscreen' , self.is_full_screen)
        self.full_screen_btn.text="Exit Full Screen" if self.is_full_screen else "Full Screen"


    def exit_program(self):
        LogManager.makeLog(message=f"INFO: Quit Program...", type=0)
        self.db.close_pool()
        App.get_running_app().stop()
        os._exit(1)
        # Window.close()
        

    def update_placeholder(self, transformed_data, index):

        texture2, lp_text, timestamp_text, owner_text, student_text=transformed_data

        if index==0:
            # Update cropped lp
            self.lp_placeholder_img_1.texture=texture2
            #Update license plate label
            self.lp_placeholder_label_1.text=lp_text
            #Update timestamp
            self.lp_placeholder_timestamp_1.text=timestamp_text
            self.lp_owner_label_1.text= owner_text
            self.lp_student_label_1.text= student_text

        if index==1:
            # Update cropped lp
            self.lp_placeholder_img_2.texture=texture2
            #Update license plate label
            self.lp_placeholder_label_2.text=lp_text
            #Update timestamp
            self.lp_placeholder_timestamp_2.text=timestamp_text
            self.lp_owner_label_2.text= owner_text
            self.lp_student_label_2.text= student_text

        if index==2:
            # Update cropped lp
            self.lp_placeholder_img_3.texture=texture2
            #Update license plate label
            self.lp_placeholder_label_3.text=lp_text
            #Update timestamp
            self.lp_placeholder_timestamp_3.text=timestamp_text
            self.lp_owner_label_3.text= owner_text
            self.lp_student_label_3.text= student_text

        if index==3:
            # Update cropped lp
            self.lp_placeholder_img_4.texture=texture2
            #Update license plate label
            self.lp_placeholder_label_4.text=lp_text
            #Update timestamp
            self.lp_placeholder_timestamp_4.text=timestamp_text
            self.lp_owner_label_4.text= owner_text
            self.lp_student_label_4.text= student_text

        if index==4:
            # Update cropped lp
            self.lp_placeholder_img_5.texture=texture2
            #Update license plate label
            self.lp_placeholder_label_5.text=lp_text
            #Update timestamp
            self.lp_placeholder_timestamp_5.text=timestamp_text
            self.lp_owner_label_5.text= owner_text
            self.lp_student_label_5.text= student_text

    def process_placeholder_data(self, data):
        placeholder=data
        
        # LP img
        # convert it to texture
        buf2 = cv2.flip(placeholder["lp_data"]["cropped_LP"], 0)
        buf2 = buf2.tostring()
        texture2 = Texture.create(size=(placeholder["lp_data"]["cropped_LP"].shape[1], placeholder["lp_data"]["cropped_LP"].shape[0]), colorfmt='bgr') 
        #if working on RASPBERRY PI, use colorfmt='rgba' here instead, but stick with "bgr" in blit_buffer. 
        texture2.blit_buffer(buf2, colorfmt='bgr', bufferfmt='ubyte')

        return texture2, placeholder["lp_data"]["lp"], placeholder["lp_data"]["timestamp"], placeholder["student"], placeholder["guardion"]

    def update(self, dt):
        try:
            self.cudaAvailableLabel.text= "On: GPU" if use_gpu else "On: CPU"
            

            start_time = time.time()

            if Utils.isImageFile(inputSource):
                frame=self.cap
                ret = True
            else:
                ret, frame=self.cap.read()

            if not ret:
                if Utils.isVideoFile(inputSource):
                    self.cap.stop()
                self.exit_program()
            else:
                frame=cv2.resize(frame, (1280, 720))                
                clean_frame=frame.copy()
                drawn_frame=frame.copy()

                input_img = self.lp_det.preprocess(frame)

                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(self.lp_det.predict, input_img)
                    yolo_out = future.result()
                
                
                bboxes = self.lp_det.procesar_salida_yolo(yolo_out)
                
                
                lp_rec=self.lp_det.get_cropped_lp(clean_frame, bboxes)

                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future2 = executor.submit(self.ocr_op.ocr_scan, clean_frame, drawn_frame, lp_rec, self.draw_boxes)
                    ocr_data = future2.result()
                
                if self.draw_boxes:
                    self.lp_det.draw_bboxes(clean_frame, drawn_frame, bboxes, self.display_list, mostrar_score=True)
                    self.ocr_op.draw_bboxes_with_text(drawn_frame, ocr_data)                

            
                for data in ocr_data:
                    # record to db
                    check_lp_sql = """SELECT lp.id, lp.plate_number, p.name, g.name FROM license_plate lp
                                    JOIN guardian g ON g.lp_id=lp.id
                                    JOIN profile p ON p.id=g.profile_id
                                     WHERE lp.plate_number='{}'
                    """.format(data["lp"])

                    check_lp_sql_res=self.db.loop.run_until_complete(self.db.selectOne(check_lp_sql))
                    
                    if check_lp_sql_res!=None:
                        
                        lp_id, plateNumber, student, guardion = check_lp_sql_res
                        trx_sql = "INSERT INTO license_plate_trx (lp_id, timestamp) VALUES ('{}', '{}')".format(lp_id, data["datetime"])

                        # insert record into db
                        self.db.loop.run_until_complete(self.db.insertOne(trx_sql))    
                        if len(self.display_list)>=5:
                            self.display_list.pop()
                        self.display_list.insert(0, {"lp_data": data, "student": student, "guardion": guardion})


                display_list=self.display_list

                if len(display_list)>0 and display_list[0]!=None:
                    transformed_data=self.process_placeholder_data(display_list[0])
                    self.update_placeholder(transformed_data, 0)
                if len(display_list)>1 and display_list[1]!=None:
                    transformed_data=self.process_placeholder_data(display_list[1])
                    self.update_placeholder(transformed_data, 1)
                if len(display_list)>2 and display_list[2]!=None:
                    transformed_data=self.process_placeholder_data(display_list[2])
                    self.update_placeholder(transformed_data, 2)
                if len(display_list)>3 and display_list[3]!=None:
                    transformed_data=self.process_placeholder_data(display_list[3])
                    self.update_placeholder(transformed_data, 3)
                if len(display_list)>4 and display_list[4]!=None:
                    transformed_data=self.process_placeholder_data(display_list[4])
                    self.update_placeholder(transformed_data, 4)
                

                frame=drawn_frame if self.draw_boxes else clean_frame

                if self.shouldDisplay:
                    if self.videoPlaceholder.source!='':
                        self.videoPlaceholder.source=''
                    #put fps
                    Utils.put_FPS_Text(frame, start_time)

                    # convert it to texture
                    buf1 = cv2.flip(frame, 0)
                    buf = buf1.tostring()

                    texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr') 
                    #if working on RASPBERRY PI, use colorfmt='rgba' here instead, but stick with "bgr" in blit_buffer. 
                    texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                    self.videoPlaceholder.texture=texture1

                else:
                    # display image from the texture
                    self.videoPlaceholder.source = VideoPlaceHolderSource

                print("FPS: ", 1/(time.time()-start_time))


        except Exception as e:

            self.videoPlaceholder.source = VideoPlaceHolderSource
            
            LogManager.makeLog(message=f"LOAD_FRAME_FAIL: File {inspect.stack()[1][1]}, Line {inspect.stack()[1][2]}:Could not load frame! Check whether the video is finished or it is the camera issue.", type=1)
            LogManager.makeLog(message=f'{traceback.format_exc()}', type=1)

            self.exit_program()
        
