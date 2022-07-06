import os
import Settings
import Commands
from PyQt5.QtGui import QImage, QPixmap

def init(self):
    self.graphWidget.setBackground('#fbfbfb')
    self.graphWidget.showGrid(x=True, y=True)
    Settings.graph_ref=self.graphWidget.plot(Settings.current_time,Settings.current_weight)

def graph_update(self):
    Settings.graph_ref.setData(Settings.current_time++,Settings.current_weight)


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
