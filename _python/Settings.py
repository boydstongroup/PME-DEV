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

    global ex1_Interval
    ex1_Interval = 400

    global ex2_Interval
    ex2_Interval = 400

    global ex1_microstep
    ex1_microstep = 256

    global ex2_microstep
    ex2_microstep = 256

    global tag_index
    tag_index = 0

    global interval
    interval = 2

    global duration
    duration = 2

    global total
    total = 1

    global current
    current = 0

    global rotation
    rotation = 0



    global interval_running
    interval_running = False

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
        time.sleep(0.02)
        Settings.i2cbusy = False
    except Exception as e:
        print(e, "command send failure,contact Jerry for support")
