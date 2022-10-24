import os
import Settings
import Commands
import statistics

import numpy as np
from PyQt5.QtGui import QImage, QPixmap
from pyqtgraph import mkPen
from PyQt5 import QtCore


def init(self):
    self.graphWidget.setBackground('#fbfbfb')
    self.graphWidget.showGrid(x=True, y=True)

    self.graphWidget_2.setBackground('#fbfbfb')
    self.graphWidget_2.showGrid(x=True, y=True)

    styles = {'color': 'r', 'font-size': '15px'}
    self.graphWidget.setLabel('left', 'Weight (g)', **styles)
    self.graphWidget.setLabel('bottom', 'Time (s)', **styles)

    self.graphWidget_2.setLabel('left', 'Concentration (Vol%)', **styles)
    self.graphWidget_2.setLabel('bottom', 'Time (s)', **styles)


def graph_update(self):
    Settings.current_time.append(Settings.sample_time - Settings.initial_time)
    Settings.graph_ref.setData(Settings.current_time, Settings.current_weight)
    self.reading_label.setText(
        "Live Reading: " + str(Settings.current_weight[-1]) + "g")
    if len(Settings.current_time) > 1:
        self.stdev_label.setText(
            "Stdev: " + str(round(statistics.stdev(Settings.current_weight), 2)))
        self.average_label.setText(
            "Avg: " + str(round(statistics.mean(Settings.current_weight), 2)) + "g")

        m, b = np.polyfit(Settings.current_time, Settings.current_weight, 1)
        self.linearFit_label.setText(
            "LR: " + str(round(m, 4)) + "x+" + str(round(b, 2)))
        correlation_matrix = np.corrcoef(
            Settings.current_time, Settings.current_weight)
        correlation_xy = correlation_matrix[0, 1]
        r_squared = correlation_xy**2
        self.r2_label.setText("R sq: " + str(round(r_squared,2)))

        Settings.trend_time=[0,Settings.current_time[-1]]
        Settings.trend_weight=[b,(m*Settings.current_time[-1]+b)]

        Settings.trend_ref.setData(Settings.trend_time, Settings.trend_weight)

def oxygen_update(self):
    Settings.oxygen_current_time.append(Settings.oxygen_sample_time - Settings.oxygen_initial_time)
    Settings.oxygen_graph_ref.setData(Settings.oxygen_current_time, Settings.oxygen_concentration)
    self.Oxygen_label.setText(str(Settings.oxygen_concentration[-1]) + " Vol%")


def collection_start(self):
    pen = mkPen(color=(197, 5, 12), width=2)
    Settings.graph_ref = self.graphWidget.plot(
        Settings.current_time, Settings.current_weight, pen=pen)
    pen2 = mkPen(color=(4, 121, 168), width=1, style=QtCore.Qt.DashLine)
    Settings.trend_ref = self.graphWidget.plot(
        Settings.trend_time, Settings.trend_weight, pen=pen2)

    self.startCollection_pushButton.setEnabled(False)
    self.startCollection_pushButton.setText("Initializing...")

def oxygen_start(self):
    pen = mkPen(color=(197, 5, 12), width=2)
    Settings.oxygen_graph_ref = self.graphWidget_2.plot(
        Settings.oxygen_current_time, Settings.oxygen_concentration, pen=pen)

    self.startOxygenCollection_pushButton.setEnabled(False)
    self.startOxygenCollection_pushButton.setText("Initializing...")


def zero(self):
    Settings.zero = True


def collection_initialized(self):
    self.startCollection_pushButton.setEnabled(True)
    self.startCollection_pushButton.setText("Reset Collection")
    self.reset_pushButton.setEnabled(True)

def oxygen_initialized(self):
    self.startOxygenCollection_pushButton.setEnabled(True)
    self.startOxygenCollection_pushButton.setText("Reset Collection")
    self.Calibration1_pushButton.setEnabled(True)
    self.Calibration2_pushButton.setEnabled(True)

def collection_complete(self):
    self.startCollection_pushButton.setEnabled(True)
    self.startCollection_pushButton.setText("Collect Data")
    self.reset_pushButton.setEnabled(False)
    Settings.current_time = []
    Settings.current_weight = []

def oxygen_complete(self):
    self.startOxygenCollection_pushButton.setEnabled(True)
    self.startOxygenCollection_pushButton.setText("Collect Data")
    Settings.oxygen_current_time = []
    Settings.oxygen_concentration = []
    self.Calibration1_pushButton.setEnabled(False)
    self.Calibration2_pushButton.setEnabled(False)

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


def gradient_start(self):
    if self.ex1Final_spinBox.value() > self.ex1Initial_spinBox.value():
        Settings.ex1_Increasing = True
    else:
        Settings.ex1_Increasing = False

    if self.ex2Final_spinBox.value() > self.ex2Initial_spinBox.value():
        Settings.ex2_Increasing = True
    else:
        Settings.ex2_Increasing = False

    Settings.ex1_CurrentInterval = self.ex1Initial_spinBox.value()
    Settings.ex2_CurrentInterval = self.ex2Initial_spinBox.value()

    Settings.ex1_FinalInterval = self.ex1Final_spinBox.value()
    Settings.ex2_FinalInterval = self.ex2Final_spinBox.value()

    Settings.ex1_GradientInterval = (
        self.ex1Duration_spinBox.value() * 60000) / (abs(self.ex1Final_spinBox.value() - self.ex1Initial_spinBox.value()))
    Settings.ex2_GradientInterval = (
        self.ex2Duration_spinBox.value() * 60000) / (abs(self.ex2Final_spinBox.value() - self.ex2Initial_spinBox.value()))
    self.startGradient_pushButton.setText("END EXTRUSION GRADIENT")
    gradient_update(self)


def gradient_complete(self):
    self.startGradient_pushButton.setText("START EXTRUSION GRADIENT")


def gradient_update(self):
    self.ex1_lcdNumber.display(Settings.ex1_CurrentInterval)
    self.ex2_lcdNumber.display(Settings.ex2_CurrentInterval)


def gradient_validate(self):
    if(self.ex1Final_spinBox.value() != self.ex1Initial_spinBox.value() and self.ex2Final_spinBox.value() != self.ex2Initial_spinBox.value()):
        self.startGradient_pushButton.setEnabled(True)
    else:
        self.startGradient_pushButton.setEnabled(False)


def Agitation_start(self, mot):
    if mot == 0:
        Settings.ex1_AgitationDuration = self.ex1AgitateDuration_spinBox.value()
        self.ex1Agitate_pushButton.setEnabled(False)
    if mot == 1:
        Settings.ex2_AgitationDuration = self.ex2AgitateDuration_spinBox.value()
        self.ex2Agitate_pushButton.setEnabled(False)
    if mot == 2:
        Settings.ex1_AgitationInterval = self.ex1AgitateInterval_spinBox.value()
        Settings.ex2_AgitationInterval = self.ex2AgitateInterval_spinBox.value()
        Settings.ex1_AgitationDuration = self.ex1AgitateDuration_spinBox.value()
        Settings.ex2_AgitationDuration = self.ex2AgitateDuration_spinBox.value()
        self.startAgitation_pushButton.setText("END PROGRAMMED AGITATION")


def Agitation_complete(self, mot):
    if mot == 0:
        self.ex1Agitate_pushButton.setEnabled(True)
    if mot == 1:
        self.ex2Agitate_pushButton.setEnabled(True)
    if mot == 2:
        self.startAgitation_pushButton.setText("START PROGRAMMED AGITATION")
