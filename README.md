# UCSI ALPR App

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
    - Anaconda & Pip: "pip install -r requirements.txt"
    
## Step of running app:
1. Open WAMP/XAMPP/etc, open Apache server and MySQL.
2. Specify source of input in "config.cfg", source can be webcam, video file, image file, IP cam (rstp://) or Mobile IP Webcam (https://).
3. In the terminal, run "python main.py".

### Mobile Camera as Input Source 
**IP Webcam**: https://play.google.com/store/apps/details?id=com.pas.webcam&hl=en&gl=US
**IP Webcam (How to use)**: https://youtu.be/2xcUzXataIk


## Step of making packaged exe file:
1. In the terminal, run "python compile.py"
2. Move to "**dist**" folder, you will see an exe file.
3. If the **icons** and **models** folder, **config.cfg** and **layout.kv** do not exist in "**dist**" folder, add that 2 folders and 2 stuff into it.

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

### End of Documentation.






