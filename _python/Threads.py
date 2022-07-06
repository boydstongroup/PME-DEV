import Settings
import Commands
import time
import sys
import RPi.GPIO as GPIO
from hx711 import HX711
# import Functions
# import socket
# import board
# import busio
# import os
# import timeit


# import adafruit_mma8451
# import adafruit_bme280

from time import sleep
from PyQt5.QtCore import QThread, pyqtSignal
from picamera import PiCamera


class Gradient(QThread):
    update = pyqtSignal()

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self._running = False

    def run(self):
        Settings.gradient_running = True
        Commands.Gradient_Update()
        ex1_last_time = round(time.time() * 1000)
        ex2_last_time = ex1_last_time
        while Settings.ex1_FinalInterval != Settings.ex1_CurrentInterval and Settings.ex2_FinalInterval != Settings.ex2_CurrentInterval and Settings.gradient_running:
            current_time = round(time.time() * 1000)
            ex1_eclipsed_time = current_time - ex1_last_time
            ex2_eclipsed_time = current_time - ex2_last_time
            updated = False
            if ex1_eclipsed_time >= Settings.ex1_GradientInterval:
                if Settings.ex1_Increasing:
                    Settings.ex1_CurrentInterval += 1
                else:
                    Settings.ex1_CurrentInterval -= 1
                ex1_last_time = current_time
                updated = True
            if ex2_eclipsed_time >= Settings.ex2_GradientInterval:
                if Settings.ex2_Increasing:
                    Settings.ex2_CurrentInterval += 1
                else:
                    Settings.ex2_CurrentInterval -= 1
                ex2_last_time = current_time
                updated = True
            if updated:
                Commands.Gradient_Update()
                self.update.emit()
        Settings.gradient_running = False

class Agitation(QThread):

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self._running = False

    def run(self):
        Settings.agitation_running = True
        ex1_last_time = round(time.time())
        while Settings.agitation_running:
            current_time = round(time.time())
            ex1_eclipsed_time = current_time - ex1_last_time
            if ex1_eclipsed_time >= Settings.ex1_AgitationInterval:
                Commands.Agitation(2)
                ex1_last_time = current_time
                Settings.agitating = True
                sleep(Settings.ex1_AgitationDuration)
                Settings.agitating = False
                Commands.Power_Update()
                if Settings.gradient_running:
                    Commands.Gradient_Update()
                else:
                    Commands.slider_Released()


class ex1Agitation(QThread):

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self._running = False

    def run(self):
        Commands.Agitation(0)
        sleep(Settings.ex1_AgitationDuration)
        Commands.Power_Update()
        if Settings.gradient_running:
            Commands.Gradient_Update()
        else:
            Commands.slider_Released()


class ex2Agitation(QThread):

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self._running = False

    def run(self):
        Commands.Agitation(1)
        sleep(Settings.ex2_AgitationDuration)
        Commands.Power_Update()
        if Settings.gradient_running:
            Commands.Gradient_Update()
        else:
            Commands.slider_Released()

class Collect(QThread):
    update = pyqtSignal()

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self._running = False

    def run(self):
        Settings.collection_running = True
        hx = HX711(15, 14)
        hx.set_reading_format("MSB", "MSB")
        hx.set_reference_unit(Settings.scale_referenceUnit)
        hx.reset()
        hx.tare()

        while Settings.collection_running:
            val = round(max(0.00, hx.get_weight(5)),2)
            print(val)

            # To get weight from both channels (if you have load cells hooked up
            # to both channel A and B), do something like this
            #val_A = hx.get_weight_A(5)
            #val_B = hx.get_weight_B(5)
            #print "A: %s  B: %s" % ( val_A, val_B )

            hx.power_down()
            hx.power_up()
            time.sleep(1)
            Settings.current_weight.append(val)
            self.update.emit()
        Settings.gradient_running = False

# class Interval(QThread):
#
#     def __init__(self):
#         QThread.__init__(self)
#
#     def __del__(self):
#         self._running = False
#
#     def run(self):
#         while True:
#             for x in range(Settings.interval_time):
#                 sleep(1)
#                 if not Settings.interval_running:
#                     break
#             Settings.frame_dir = not Settings.frame_dir
#             Settings.core_dir = not Settings.core_dir
#
#             CMD = ("1~1~" + str(int(Settings.frame_dir)) +
#                    "~" + str(int(Settings.core_dir)))
#             Settings.sendCMD(CMD)
#
#             if not Settings.interval_running:
#                 break
#
#
# class Snap(QThread):
#
#     transmit = pyqtSignal()
#
#     def __init__(self):
#         QThread.__init__(self)
#
#     def __del__(self):
#         self._running = False
#
#     def run(self):
#         if Settings.IR_imaging:
#             Commands.extract_lights()
#             Settings.sendCMD("4~1")
#         try:
#             sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             ip_address = "10.0.5.1"
#             server_address = (ip_address, 23456)
#             sock.connect(server_address)
#             cmd = "A~" + str(350) + "~" + str(350) + "~" + \
#                 str(Settings.rotation) + "~" + str(int(Settings.AOI_X * 100)) + "~" + \
#                 str(int(Settings.AOI_Y * 100)) + "~" + str(int(Settings.AOI_W * 100)) + \
#                 "~" + str(int(Settings.AOI_H * 100)) + "~1"
#             sock.sendall(cmd.encode())
#
#             with open('../_temp/snapshot.jpg', 'wb') as f:
#                 while True:
#                     try:
#                         data = sock.recv(5)
#                     except Exception as e:
#                         print(e, 'timeout after 20 seconds... retaking image')
#                     if not data:
#                         break
#                     f.write(data)
#                     self.transmit.emit()
#             sock.close()
#
#         except Exception as e:
#             print(e, "snapshot failure,contact Jerry for support")
#         if Settings.IR_imaging:
#             Settings.sendCMD("4~0")
#             Commands.deploy_lights()
#
#
# class Preview(QThread):
#     transmit = pyqtSignal()
#
#     def __init__(self):
#         QThread.__init__(self)
#
#     def __del__(self):
#         self._running = False
#
#     def run(self):
#         if Settings.IR_imaging:
#             Commands.extract_lights()
#             Settings.sendCMD("4~1")
#         try:
#             sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             ip_address = "10.0.5.1"
#             server_address = (ip_address, 23456)
#             sock.connect(server_address)
#             cmd = "A~" + str(Settings.x_resolution) + "~" + str(Settings.y_resolution) + "~" + \
#                 str(Settings.rotation) + "~" + str(int(Settings.AOI_X * 100)) + "~" + \
#                 str(int(Settings.AOI_Y * 100)) + "~" + str(int(Settings.AOI_W * 100)) + \
#                 "~" + str(int(Settings.AOI_H * 100)) + \
#                 "~" + str(int(Settings.imaging_mode))
#
#             start_time = timeit.default_timer()
#             sock.sendall(cmd.encode())
#
#             if Settings.imaging_mode == 1:
#                 with open('../_temp/preview.jpg', 'wb') as f:
#                     while True:
#                         try:
#                             data = sock.recv(5)
#                         except Exception as e:
#                             print(
#                                 e, ': no connection for 20 seconds... retaking image')
#                         if not data:
#                             break
#                         f.write(data)
#                         self.transmit.emit()
#                 sock.close()
#
#             else:
#                 with open('../_temp/preview.png', 'wb') as f:
#                     while True:
#                         data = sock.recv(5)
#                         if not data:
#                             break
#                         f.write(data)
#                         self.transmit.emit()
#                 sock.close()
#         except Exception as e:
#             print(e, "preview failure,contact Jerry for support")
#         Settings.time_elipsed = int(timeit.default_timer() - start_time)
#         if Settings.IR_imaging:
#             Settings.sendCMD("4~0")
#             Commands.deploy_lights()
#
#
# class Sensor(QThread):
#     update = pyqtSignal()
#     logstart = pyqtSignal()
#     logdone = pyqtSignal()
#
#     def __init__(self):
#         QThread.__init__(self)
#
#     def __del__(self):
#         self._running = False
#
#     def run(self):
#         i2c = busio.I2C(board.SCL, board.SDA)
#         time.sleep(1)
#         if Settings.acc_attached:
#             sensor = adafruit_mma8451.MMA8451(i2c)
#         if Settings.temp_attached:
#             bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, 0x76)
#
#         while True:
#             try:
#                 if Settings.tag_index == 0 and Settings.acc_attached:
#                     accel_x, accel_y, accel_z = sensor.acceleration
#                     Settings.ACC_X_text = "{0:.2f}".format(accel_x)
#                     Settings.ACC_Y_text = "{0:.2f}".format(accel_y)
#                     Settings.ACC_Z_text = "{0:.2f}".format(accel_z)
#                 elif Settings.temp_attached:
#                     Settings.TEMP_text = "{0:.2f}".format(bme280.temperature)
#                     Settings.HUD_text = "{0:.2f}".format(bme280.humidity)
#                     Settings.PR_text = "{0:.2f}".format(bme280.pressure)
#
#                 self.update.emit()
#                 sleep(Settings.sample_time)
#
#                 if Settings.log_sensor:
#                     if not Settings.sensor_flag:
#                         self.logstart.emit()
#                         if not os.path.isdir(Settings.prelog_dir):
#                             os.umask(0)
#                             os.mkdir(Settings.prelog_dir)
#                         if not os.path.isdir(Settings.log_dir):
#                             os.umask(0)
#                             os.mkdir(Settings.log_dir)
#                         log_file = open(Settings.log_dir + "/log.txt", "w")
#                         Settings.sensor_flag = True
#                         os.chmod(Settings.log_dir + "/log.txt", 0o777)
#
#                     if Settings.tag_index == 0:
#
#                         log_file.write(Settings.ACC_X_text + "\t" +
#                                        Settings.ACC_Y_text + "\t" + Settings.ACC_Z_text + "\r\n")
#                     else:
#
#                         log_file.write(Settings.TEMP_text + "\t" +
#                                        Settings.HUD_text + "\t" + Settings.PR_text + "\r\n")
#
#                     if int(timeit.default_timer() - Settings.log_start_time > Settings.log_duration):
#                         Settings.log_sensor = False
#                         Settings.sensor_flag = False
#                         log_file.close()
#                         self.logdone.emit()
#             except Exception as e:
#                 pass
#
#
# class Timelapse(QThread):
#     captured = pyqtSignal()
#     transmit = pyqtSignal()
#     transmitstart = pyqtSignal()
#
#     def __init__(self):
#         QThread.__init__(self)
#
#     def __del__(self):
#         self._running = False
#
#     def run(self):
#         if not os.path.isdir(Settings.full_dir):
#             os.umask(0)
#             os.mkdir(Settings.full_dir)
#
#         Settings.current = 0
#         while Settings.current < Settings.total:
#
#             start_time = timeit.default_timer()
#             if Settings.imaging_mode == 1:
#                 Settings.current_image = Settings.full_dir + \
#                     "/" + Settings.sequence_name + "_%04d.jpg" % Settings.current
#             else:
#                 Settings.current_image = Settings.full_dir + \
#                     "/" + Settings.sequence_name + "_%04d.png" % Settings.current
#
#             sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             sock.settimeout(20)
#             ip_address = "10.0.5.1"
#             skip = False
#             server_address = (ip_address, 23456)
#             if Functions.check_connection():
#                 try:
#                     sock.connect(server_address)
#                 except Exception as e:
#                     print(e, ': socket connection failed, please reboot device')
#                     skip = True
#                 if Settings.IR_imaging:
#                     Commands.extract_lights()
#                     Settings.sendCMD("4~1")
#
#                 cmd = "A~" + str(Settings.x_resolution) + "~" + str(Settings.y_resolution) + "~" + \
#                     str(Settings.rotation) + "~" + str(int(Settings.AOI_X * 100)) + "~" + \
#                     str(int(Settings.AOI_Y * 100)) + "~" + str(int(Settings.AOI_W * 100)) + \
#                     "~" + str(int(Settings.AOI_H * 100)) + \
#                     "~" + str(int(Settings.imaging_mode))
#                 if not skip:
#                     sock.sendall(cmd.encode())
#
#                     with open(Settings.current_image, 'wb') as f:
#                         self.transmitstart.emit()
#                         while True:
#                             try:
#                                 data = sock.recv(5)
#                             except Exception as e:
#                                 print(
#                                     e, ': no connection for 20 seconds... retaking image')
#                                 if Settings.IR_imaging:
#                                     Settings.sendCMD("4~0")
#                                     Commands.deploy_lights()
#                                 break
#                             if not data:
#                                 Settings.current += 1
#                                 print("image capture and transmission succesful")
#                                 if Settings.IR_imaging:
#                                     Settings.sendCMD("4~0")
#                                     Commands.deploy_lights()
#                                 break
#                             f.write(data)
#                             self.transmit.emit()
#                         sock.close()
#                         self.captured.emit()
#                 elapsed = int(timeit.default_timer() - start_time)
#
#             if elapsed < Settings.interval * 60:
#                 for x in range(Settings.interval * 60 - elapsed):
#                     sleep(1)
#                     if not Settings.timelapse_running:
#                         break
#             if not Settings.timelapse_running:
#                 break
