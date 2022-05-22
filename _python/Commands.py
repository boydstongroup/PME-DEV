import Settings
import UI_Update
import Functions
import decimal
from time import sleep


def init():
    Settings.sendCMD("0~")


def motor_toggle(mot, self):
    if not mot:
        if Settings.LINKED and not Settings.ex1_enabled:
            Settings.ex1_enabled = True
            Settings.ex2_enabled = True
        elif Settings.LINKED and Settings.ex1_enabled:
            Settings.ex1_enabled = False
            Settings.ex2_enabled = False
        elif not Settings.LINKED and not Settings.ex1_enabled:
            Settings.ex1_enabled = True
        else:
            Settings.ex1_enabled = False
    else:
        if Settings.LINKED and not Settings.ex2_enabled:
            Settings.ex1_enabled = True
            Settings.ex2_enabled = True
        elif Settings.LINKED and Settings.ex2_enabled:
            Settings.ex1_enabled = False
            Settings.ex2_enabled = False
        elif not Settings.LINKED and not Settings.ex2_enabled:
            Settings.ex2_enabled = True
        else:
            Settings.ex2_enabled = False
    CMD = ("1~0~" + str(int(Settings.ex1_enabled)) +
           "~" + str(int(Settings.ex2_enabled)))
    Settings.sendCMD(CMD)
    UI_Update.motor_update(self)


def reverse_motor(mot, self):
    if Settings.LINKED:
        Settings.ex1_dir = not Settings.ex1_dir
        Settings.ex2_dir = not Settings.ex2_dir
    else:
        if not mot:
            Settings.ex1_dir = not Settings.ex1_dir

        else:
            Settings.ex2_dir = not Settings.ex2_dir
    CMD = ("1~1~" + str(int(Settings.ex1_dir)) +
           "~" + str(int(Settings.ex2_dir)))
    Settings.sendCMD(CMD)
    UI_Update.dir(self)


def interval_Released():
    CMD = "1~2~" + str(Settings.ex1_GInterval) + \
        "~" + str(Settings.ex2_GInterval)
    Settings.sendCMD(CMD)


def microstep_Released():
    CMD = "1~3~" + str(Settings.ex1_Gmicrostep) + \
        "~" + str(Settings.ex2_Gmicrostep)
    Settings.sendCMD(CMD)


def current_Released():
    CMD = "1~4~" + str(Settings.ex1_currentLimit) + \
        "~" + str(Settings.ex2_currentLimit)
    Settings.sendCMD(CMD)
