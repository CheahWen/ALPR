import configparser

"""
    DB: server, port, user, password, db
    Input: source
    LP_Detect: weights-path, input-size, iou, score_threshold
    OCR: weights-path, config-path, class-path

"""

# our config file name
configFile='config.cfg'



class ConfigParserManager:
    
    
    @staticmethod
    def getAppConfig(configFile=configFile):
        config = configparser.ConfigParser()
        config.read(configFile)

        app_title=config.get("App", "title")
        app_icon=config.get("App", "icon")
       

        return app_title, app_icon

    @staticmethod
    def getDBConfig(configFile=configFile):
        config = configparser.ConfigParser()
        config.read(configFile)

        server=config.get("DB", "server")
        user=config.get("DB", "user")
        password=config.get("DB", "password")
        port=int(config.get("DB", "port"))
        db=config.get("DB", "db")

        return server, user, password, port, db

    @staticmethod
    def getInputSourceConfig(configFile=configFile):
        config = configparser.ConfigParser()
        config.read(configFile)
        inputSource=config.get("Input", "source")

        return inputSource

    @staticmethod
    def getVideoPlaceholderConfig(configFile=configFile):
        config = configparser.ConfigParser()
        config.read(configFile)
        videoPlaceholder=config.get("VideoPlaceholder", "source")

        return videoPlaceholder
    
    @staticmethod
    def getLPDetectionConfig(configFile=configFile):
        config = configparser.ConfigParser()
        config.read(configFile)
        lp_det_weights_path=config.get("LP_Detect", "weights-path")
        lp_det_input_size_x=int(config.get("LP_Detect", "input-size-x"))
        lp_det_input_size_y=int(config.get("LP_Detect", "input-size-y"))
        lp_det_iou_threshold=float(config.get("LP_Detect", "iou-threshold"))
        lp_det_score_threshold=float(config.get("LP_Detect", "score-threshold"))

        return lp_det_weights_path, lp_det_input_size_x, lp_det_input_size_y, lp_det_iou_threshold, lp_det_score_threshold

    @staticmethod
    def getOCRConfig(configFile=configFile):
        config = configparser.ConfigParser()
        config.read(configFile)
        ocr_weights_path=config.get("OCR", "weights-path")
        ocr_config_path=config.get("OCR", "config-path")
        ocr_class_path=config.get("OCR", "class-path")
        ocr_input_size_x=int(config.get("OCR", "input-size-x"))
        ocr_input_size_y=int(config.get("OCR", "input-size-y"))
        
        ocr_nms_threshold=float(config.get("OCR", "nms-threshold"))
        ocr_score_threshold=float(config.get("OCR", "score-threshold"))

        return ocr_weights_path, ocr_config_path, ocr_class_path, ocr_input_size_x, ocr_input_size_y, ocr_nms_threshold, ocr_score_threshold
