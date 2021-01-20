# UCSI ALPR App

---

## Special thanks for the following Github repo
### Source code references:
> LP Detection: https://github.com/CheahWen/ConvALPR

> OCR: https://github.com/sergiomsilva/alpr-unconstrained

> Previously I use this: https://github.com/wechao18/Efficient-alpr-unconstrained, too slow and abandoned already.

---

## Step of installation:
1. Make sure Anaconda or Pip is installed
2. Create venv, choose yours:
    - Anaconda: conda create -n alpr python=3.7
    - Pip: virtualenv venv
3. Activate venv, choose yours:
    - Anaconda: conda activate alpr
    - Pip: [Linux cmd]: "source venv/bin/activate", [Window cmd]: ".\venv\Scripts\activate"
4. Then, install all dependency in requirements.txt.
    - Anaconda & Pip: type "pip install -r requirements.txt", this will work for Anaconda too because it will sync packages installed           from Pip
    
## Step of running app:
1. Open WAMP/XAMPP/etc, open Apache server and MySQL.
2. Specify source of input in "config.cfg", source can be webcam, video file, image file, IP cam (rstp://) or Mobile IP Webcam (https://).

![cfg](https://github.com/CheahWen/UCSI_ALPR/blob/main/img_log/cfg.PNG)

3. Activate venv.

![Conda Activate Env](https://github.com/CheahWen/UCSI_ALPR/blob/main/img_log/activate_conda_env.PNG)

4. Run "python main.py".

![Conda run script](https://github.com/CheahWen/UCSI_ALPR/blob/main/img_log/run_script.PNG)

5. If finished, just deactivate env.
   - Pip: simple type "deactivate"
   - Anaconda: simple type "conda deactivate"
     ![Conda deactivate](https://github.com/CheahWen/UCSI_ALPR/blob/main/img_log/deactivate_conda_env.PNG)
     
#### Mobile Camera as Input Source 
> IP Webcam Download: https://play.google.com/store/apps/details?id=com.pas.webcam&hl=en&gl=US

> Random Youtube video (How to use IP Webcam): https://youtu.be/2xcUzXataIk


## Step of making packaged exe file:
1. In the terminal, run "python compile.py"
2. Move to "**dist**" folder, you will see an exe file.
3. If the **icons** and **models** folder, **config.cfg** and **layout.kv** do not exist in "**dist**" folder, copy that 2 folders and 2 stuff from your main folder into it.
4. Run the exe file, you are good to go.

---

# Want theory? It is pretty boring.

> Originally, I refer to the this paper: https://openaccess.thecvf.com/content_ECCV_2018/papers/Sergio_Silva_License_Plate_Detection_ECCV_2018_paper.pdf

> Then I also found OCR paper in the above paper: https://www.researchgate.net/publication/320677458_Real-Time_Brazilian_License_Plate_Detection_and_Recognition_Using_Deep_Convolutional_Neural_Networks

> You can see how they implement their model (affine transform, data augmentation, YOLO stuff).

> FYI, You Only Look Once (YOLO), a pretrained model using CNN, now got v5 implemented using Pytorch: https://github.com/ultralytics/yolov5.

> But, I only take their OCR model, abandoned car detection and replace lp detection model from this repo: https://github.com/CheahWen/ConvALPR.


---

# Want to deploy on Atlas 200 DK?

> Atlas only take TF or caffe model to convert to OM format which is the only compatible model for Ascend chip.

> If want to deploy on Atlas 200 DK, change Darknet weight file to **frozen** TF .pb model.

> "saved_model.pb" is not the right model to convert, their ckpt are separated.

> If the TF graph is not **frozen**, you will get error of model conversion in Mind Studio. 

> All TF model need to be frozen, I don't know how: https://stackoverflow.com/questions/58119155/freezing-graph-to-pb-in-tensorflow2

> View your model architecture in Netron to check input layer name: https://netron.app/

> I actually have tried to convert frozen model to OM before, but get memory issue on Mind Studio.

---

# Get some idea of Kivy
> Kivy docs: https://kivy.org/

> Random Youtube video to get started: https://youtu.be/bMHK6NDVlCM

---

# Get some idea of PyInstaller
> Packaging Kivy App: https://kivy.org/doc/stable/guide/packaging-windows.html

> Stack Overflow: https://stackoverflow.com/questions/37696206/how-to-get-an-windows-executable-from-my-kivy-app-pyinstaller

---

# Files
## Script (Only 8 scripts)
1. ConfigParserManager.py: Read config file and pass the parsed data to respective script.
2. LogManager.py: Record any log.
3. CSVManager.py: Record csv file.
4. db.py: Manage database CRUD.
5. lp_det.py: Manage license plate detection stuff.
6. ocr_op.py: Manage any operation of OCR.
7. gui.py: Contain instance of DB object, PlateDetector object, OCR object. Updating UI based on data flow, control all event of GUI.
8. main.py: The starting point of the app. Contain ALPR class object inherit from Kivy App object, update the gui based on clock with fps 60 (```Clock.schedule_interval(self.gui.update, 1.0/60.0)```).

## Others
1. layout.kv: Declare the Kivy layout for the app.
2. config.cfg: Store all neccessary configurations.

---

##### End of Documentation...






