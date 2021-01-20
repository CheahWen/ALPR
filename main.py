import os
import os
import csv
from datetime import date, datetime

from utils import Utils
from LogManager import LogManager
from ConfigParserManager import ConfigParserManager

Utils.makeDirectoryIfNotExist("LogFiles")
Utils.makeDirectoryIfNotExist("csv")
LogManager.makeConfig()

# declare before any kivy module (IMPORTANT)
from kivy.config import Config
#prevent auto exit program when pressing "ESC" key
# Config.set('kivy', 'exit_on_escape', '0')
app_title, app_icon = ConfigParserManager.getAppConfig()

Config.set('kivy','window_icon',app_icon)

Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'height',  800)

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock

import sys
import warnings
warnings.filterwarnings("ignore")
# import torch
from gui import GUI
from CSVManager import CSVManager

Window.clearcolor=(1,1,1,1)
Builder.load_file('layout.kv')

class ALPRApp(App):
    gui=GUI()
    myClock=Clock
    def build(self):
        self.title = app_title
        Clock.schedule_interval(self.gui.update, 1.0/4.0)
        return self.gui
    def on_stop(self, *args):
        Clock.unschedule(self.gui.update)

if __name__ == '__main__':

    CSVManager.writeRow(filename=f"csv/result_{date.today()}.csv", data=["**************Starting App, Break Point**************"])

    ALPRApp().run()