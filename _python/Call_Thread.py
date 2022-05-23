import Settings
import Functions
import UI_Update
import Threads
from PyQt5 import QtCore, QtGui, QtWidgets
import PyQt5

import os


def start_Gradient(self):
    self.Gradient_Thread = Threads.Gradient()
    self.Gradient_Thread.update.connect(
        lambda: UI_Update.gradient_update(self))
    self.Snap_Thread.started.connect(
        lambda: UI_Update.gradient_start(self))
    self.Snap_Thread.finished.connect(
        lambda: UI_Update.gradient_complete(self))

    self.Gradient_Thread.start()


# def start_preview(self):
#
#     self.Preview_Thread = Threads.Preview()
#     self.Preview_Thread.transmit.connect(
#         lambda: UI_Update.transmit_update(self))
#     self.Preview_Thread.started.connect(
#         lambda: UI_Update.snap_start(self))
#     self.Preview_Thread.finished.connect(
#         lambda: UI_Update.preview_complete(self))
#
#     self.Preview_Thread.start()
#
#
# def start_cycle(self):
#     if not Settings.cycle_running:
#         try:
#             self.Cycle_Thread = Threads.Cycle()
#             self.Cycle_Thread.started.connect(
#                 lambda: UI_Update.cycle_start(self))
#             self.Cycle_Thread.finished.connect(
#                 lambda: UI_Update.cycle_end(self))
#
#             self.Cycle_Thread.start()
#
#         except Exception as e:
#             print(e, "cycle failure, please contact Jerry for support")
#     else:
#         Settings.cycle_running = False
#
#
# def start_interval(self):
#     if not Settings.interval_running:
#         try:
#             self.Interval_Thread = Threads.Interval()
#             self.Interval_Thread.started.connect(
#                 lambda: UI_Update.interval_start(self))
#             self.Interval_Thread.finished.connect(
#                 lambda: UI_Update.interval_end(self))
#
#             self.Interval_Thread.start()
#
#         except Exception as e:
#             print(e, "interval failure, please contact Jerry for support")
#     else:
#         Settings.interval_running = False
#
# def start_timelapse(self):
#
#     if not Settings.timelapse_running:
#         self.Timelapse_Thread = Threads.Timelapse()
#         self.Timelapse_Thread.transmit.connect(
#             lambda: UI_Update.transmit_update(self))
#
#         self.Timelapse_Thread.started.connect(
#             lambda: UI_Update.timelapse_start(self))
#         self.Timelapse_Thread.captured.connect(
#             lambda: UI_Update.image_captured(self))
#         self.Timelapse_Thread.transmitstart.connect(
#             lambda: UI_Update.transmitst(self))
#         self.Timelapse_Thread.finished.connect(
#             lambda: UI_Update.timelapse_end(self))
#
#         self.Timelapse_Thread.start()
#
#     else:
#         Settings.timelapse_running = False
#         self.Progress_Bar.setValue(Settings.current + 1)
