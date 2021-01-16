import os
import cv2
import traceback, inspect
import numpy as np
from datetime import datetime, date
import asyncio

import configparser

from ConfigParserManager import ConfigParserManager
from LogManager import LogManager
from CSVManager import CSVManager

(ocr_weights_path,
ocr_config_path,
ocr_class_path,
input_size_x,
input_size_y,
ocr_nms_threshold,
ocr_score_threshold) = ConfigParserManager.getOCRConfig()

class OCR_OP:
    def __init__(self,
                weights_path=ocr_weights_path,
                config_path=ocr_config_path,
                class_path=ocr_class_path,
                input_size_x=input_size_x,
                input_size_y=input_size_y,
                nms_threshold=ocr_nms_threshold,
                score_threshold=ocr_score_threshold):
        self.ocr_weights = weights_path
        self.ocr_netcfg = config_path
        self.ocr_dataset = class_path
        self.input_size_x=input_size_x
        self.input_size_y=input_size_y
        self.nms_threshold=nms_threshold
        self.score_threshold=score_threshold

        self.load_model()
        self.load_classes()


    def load_classes(self):
        try:
            LogManager.makeLog(message=f"INFO: Loading OCR Classes...", type=0)
            self.classes = []
            with open(self.ocr_dataset, 'r') as f:
                self.classes = f.read().splitlines()
            LogManager.makeLog(message="OCR Classes: {}".format(self.classes), type=0)
            LogManager.makeLog(message=f"OCR Classes successfully loaded.", type=0)

        except:

            LogManager.makeLog(message=f"LOAD_CLASSES_FAIL: File {inspect.stack()[1][1]}, Line {inspect.stack()[1][2]}: Error loading OCR Classes!", type=1)
            LogManager.makeLog(message=traceback.format_exc(), type=1)
            
            os._exit(1) # exiing with a non zero value is better for returning from an error


    def load_model(self):
        try:
            LogManager.makeLog(message=f"INFO: Loading OCR Model...", type=0)
            self.ocr_net = cv2.dnn.readNetFromDarknet(self.ocr_netcfg, self.ocr_weights)

            self.ln = self.ocr_net.getLayerNames()   
            self.ln = [self.ln[i[0] - 1] for i in self.ocr_net.getUnconnectedOutLayers()]
   
            print("OCR Layer: ", self.ocr_net.getLayerNames())
            LogManager.makeLog(message=f"Successfully loaded OCR Model...", type=0)
        except:
            
            LogManager.makeLog(message=f"LOAD_MODEL_FAIL: File {inspect.stack()[1][1]}, Line {inspect.stack()[1][2]}: Error loading OCR Classes!", type=1)
            LogManager.makeLog(message=traceback.format_exc(), type=1)
            os._exit(0) # exiing with a non zero value is better for returning from an error


    def ocr_scan(self, clean_frame, drawn_frame, lp_rec, shouldDraw=True):

        ocr_rec=[]
        for rec in lp_rec:
            
            x1=int(rec[0])
            y1=int(rec[1])
            x2=int(rec[2])
            y2=int(rec[3])
            score=int(rec[4])

            lp_loc=clean_frame[y1:y2, x1:x2]
            
            (H, W) = lp_loc.shape[:2]

            blob = cv2.dnn.blobFromImage(lp_loc, 1 / 255.0, (self.input_size_x, self.input_size_y),
            swapRB=True, crop=False)

            self.ocr_net.setInput(blob)

            layerOutputs = self.ocr_net.forward()
            
            boxes = []
            confidences = []
            classIDs = []

            # loop over each of the detections
            for detection in layerOutputs:
                # extract the class ID and confidence (i.e., probability) of
                # the current object detection
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]
                # filter out weak predictions by ensuring the detected
                # probability is greater than the minimum probability
                if confidence > self.score_threshold:
                    # scale the bounding box coordinates back relative to the
                    # size of the image, keeping in mind that YOLO actually
                    # returns the center (x, y)-coordinates of the bounding
                    # box followed by the boxes' width and height
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")
                    # use the center (x, y)-coordinates to derive the top and
                    # and left corner of the bounding box
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))
                    # update our list of bounding box coordinates, confidences,
                    # and class IDs
                    boxes.append([x, y, int(width), int(height), classID, confidence])
                    confidences.append(float(confidence))
                    classIDs.append(classID)

            lp_str=''
            # bounding boxes
            idxs = cv2.dnn.NMSBoxes(boxes, confidences, self.score_threshold, self.nms_threshold)
            new_boxes=[]
            # ensure at least one detection exists
            if len(idxs) > 0:
                # loop over the indexes we are keeping
                for i in idxs.flatten():
                    # extract the bounding box coordinates
                    (x, y) = (boxes[i][0], boxes[i][1])
                    (w, h) = (boxes[i][2], boxes[i][3])
                    
                    text = "{}".format(self.classes[classIDs[i]])
                    new_boxes.append([int(x), int(y), int(w), int(h), classIDs[i], confidences[i]])

                    if shouldDraw:
                        cv2.rectangle(lp_loc, (x, y), (x + w, y + h), (0,255,0), 1)
                        cv2.putText(lp_loc, text, (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                    
                    
            new_boxes=np.array(new_boxes)
            if (len(new_boxes)>0):
                new_boxes=new_boxes[new_boxes[:,0].argsort()]    

            for box in new_boxes:
                lp_str+=self.classes[int(box[4])]

            if lp_str != '':
                
                LogManager.makeLog(message='Detected license plate number: {}'.format(lp_str), type=0)
                time=datetime.now().strftime("%I:%M:%S %p")
                data={"lp": lp_str, "timestamp": time, "datetime": datetime.now(), "cropped_LP": lp_loc, "lp_bboxes": [x1, y1, W, H, score], "ocr_bboxes": new_boxes}
                
                ocr_rec.append(data)

                
                CSVManager.writeRow(filename=f"csv/result_{date.today()}.csv", data=[data["lp"], data["timestamp"]])


        return ocr_rec

    def draw_bboxes_with_text(self, drawn_frame, ocr_data):
        for data in ocr_data:
            lp_bboxes=data["lp_bboxes"]
            for box in data["ocr_bboxes"]:
                x=int(box[0])+int(lp_bboxes[0])
                y=int(box[1])+int(lp_bboxes[1])
                w=int(box[2])
                h=int(box[3])
                character=self.classes[int(box[4])]
                cv2.rectangle(drawn_frame, (x, y), (x + w, y + h), (0,255,0), 1)
                cv2.putText(drawn_frame, character, (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)