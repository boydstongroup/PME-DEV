import os
import Settings
import Commands
from PyQt5.QtGui import QImage, QPixmap

def link(self):
    if Settings.LINKED:
        Settings.LINKED = False
        self.link_pushButton.setIcon(Settings.broken)
    else:
        Settings.LINKED = True
        self.link_pushButton.setIcon(Settings.linked)


def dir(self):
    if Settings.ex1_dir:
        self.ex1Reverse_pushButton.setIcon(Settings.reverse)
    else:
        self.ex1Reverse_pushButton.setIcon(Settings.forward)

    if Settings.ex2_dir:
        self.ex2Reverse_pushButton.setIcon(Settings.reverse)
    else:
        self.ex2Reverse_pushButton.setIcon(Settings.forward)

def motor_update(self):
    if not Settings.ex1_enabled:
        self.ex1Enable_pushButton.setText("DISABLE MOTOR")
    else:
        self.ex1Enable_pushButton.setText("ENABLE MOTOR")

    if not Settings.ex2_enabled:
        self.ex2Enable_pushButton.setText("DISABLE MOTOR")
    else:
        self.ex2Enable_pushButton.setText("ENABLE MOTOR")
