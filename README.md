## UCSI ALPR App

Step of installation:
1. Make sure Anaconda or Pip is installed
2. Create venv, choose yours:
    - Anaconda: conda create -n alpr python=3.7
    - Pip: virtualenv venv
3. Activate venv, choose yours:
    - Anaconda: conda activate alpr
    - Pip: [Linux cmd]: "source venv/bin/activate", [Window cmd]: ".\venv\Scripts\activate"
4. Then, install all dependency in requirements.txt.
    - Anaconda & Pip: "pip install -r requirements.txt"
    
Step of running app:
1. Open WAMP/XAMPP/etc, open Apache server and MySQL.
2. Specify source of input in "config.cfg", source can be webcam, video file, image file or IP cam.
3. In the terminal, run "python main.py".

Step of making packaged exe file:
1. In the terminal, run "python compile_gpu.py"
