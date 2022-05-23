import smbus
import time
import Settings
from PyQt5 import QtGui

i2c_cmd = 0x5E


def init():

    global ex1_enabled
    ex1_enabled = True

    global ex2_enabled
    ex2_enabled = True

    global LINKED
    LINKED = True

    global i2cbusy
    i2cbusy = False

    global ex1_dir
    ex1_dir = False

    global ex2_dir
    ex2_dir = False

    global ex1_GeneralMicrostep
    ex1_GeneralMicrostep = 256

    global ex2_GeneralMicrostep
    ex2_GeneralMicrostep = 256

    global ex1_currentLimit
    ex1_currentLimit = 400

    global ex2_currentLimit
    ex2_currentLimit = 400

    global ex1_GeneralInterval
    ex1_GeneralInterval = 400

    global ex2_GeneralInterval
    ex2_GeneralInterval = 400

    global ex1_GradientInterval
    ex1_GradientInterval = 60000
    global ex2_GradientInterval
    ex2_GradientInterval = 60000

    global ex1_FinalInterval
    ex1_FinalInterval = 20
    global ex2_FinalInterval
    ex2_FinalInterval = 20

    global ex1_CurrentInterval
    ex1_CurrentInterval = 200
    global ex2_CurrentInterval
    ex2_CurrentInterval = 400

    global ex1_Increasing
    ex1_Increasing = True
    global ex2_Increasing
    ex2_GradientDelta = False

    global gradient_running
    gradient_running = False

    global interval_time
    interval_time = 5

    global on_time
    on_time = 60

    global off_time
    off_time = 60

    global time_elipsed
    time_elipsed = 0

    global log_start_time
    log_start_time = 0

    global sample_time
    sample_time = 0

    global forward
    forward = QtGui.QIcon()
    forward.addPixmap(QtGui.QPixmap("../_images/Forward.png"),
                      QtGui.QIcon.Normal, QtGui.QIcon.Off)

    global reverse
    reverse = QtGui.QIcon()
    reverse.addPixmap(QtGui.QPixmap("../_images/Reverse.png"),
                      QtGui.QIcon.Normal, QtGui.QIcon.Off)

    global linked
    linked = QtGui.QIcon()
    linked.addPixmap(QtGui.QPixmap("../_images/Link.png"),
                     QtGui.QIcon.Normal, QtGui.QIcon.Off)

    global broken
    broken = QtGui.QIcon()
    broken.addPixmap(QtGui.QPixmap("../_images/Broken_Link.png"),
                     QtGui.QIcon.Normal, QtGui.QIcon.Off)


def sendCMD(cont):
    print("sending command...\n" + cont)
    temp = cont + "\n"
    try:
        if Settings.i2cbusy:
            time.sleep(0.02)

        Settings.i2cbusy = True
        bus = smbus.SMBus(1)
        converted = []
        for b in temp:
            converted.append(ord(b))
        bus.write_i2c_block_data(0x08, i2c_cmd, converted)
        Settings.i2cbusy = False
    except Exception as e:
        print(e, "command send failure,contact Jerry for support")
