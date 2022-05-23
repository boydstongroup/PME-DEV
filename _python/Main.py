import Settings
import Commands
import UI_Update
import Functions
import Threads
import Call_Thread
# import os
# import time

import sys

from PyQt5.QtWidgets import QMainWindow, QApplication

import PME_UI


class MainWindow(QMainWindow, PME_UI.Ui_MainWindow):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        Settings.init()
        Commands.init()

        self.ex1Enable_pushButton.clicked.connect(
            lambda: Commands.motor_toggle(0, self))
        self.ex2Enable_pushButton.clicked.connect(
            lambda: Commands.motor_toggle(1, self))

        self.ex1Reverse_pushButton.clicked.connect(
            lambda: Commands.reverse_motor(0, self))
        self.ex2Reverse_pushButton.clicked.connect(
            lambda: Commands.reverse_motor(1, self))

        self.link_pushButton.clicked.connect(lambda: UI_Update.link(self))

        self.ex1General_spinBox.valueChanged.connect(
            lambda: Functions.spin_change(0, self))
        self.ex2General_spinBox.valueChanged.connect(
            lambda: Functions.spin_change(1, self))

        self.ex1_verticalSlider.valueChanged.connect(
            lambda: Functions.slider_change(0, self))
        self.ex2_verticalSlider.valueChanged.connect(
            lambda: Functions.slider_change(1, self))

        self.ex1_verticalSlider.sliderReleased.connect(
            lambda: Commands.slider_Released())
        self.ex2_verticalSlider.sliderReleased.connect(
            lambda: Commands.slider_Released())

        self.ex1Current_spinBox.valueChanged.connect(
            lambda: Functions.settings_change(0, self))
        self.ex2Current_spinBox.valueChanged.connect(
            lambda: Functions.settings_change(1, self))

        self.ex1General_comboBox.currentIndexChanged.connect(
            lambda: Functions.settings_change(0, self))
        self.ex2General_comboBox.currentIndexChanged.connect(
            lambda: Functions.settings_change(1, self))

        self.ex1Initial_spinBox.valueChanged.connect(
            lambda: UI_Update.gradient_validate(self))
        self.ex1Final_spinBox.valueChanged.connect(
            lambda: UI_Update.gradient_validate(self))
        self.ex2Initial_spinBox.valueChanged.connect(
            lambda: UI_Update.gradient_validate(self))
        self.ex2Final_spinBox.valueChanged.connect(
            lambda: UI_Update.gradient_validate(self))

        self.startGradient_pushButton.clicked.connect(
            lambda: Call_Thread.start_Gradient(self))
        # self.startImaging_pushButton.clicked.connect(
        #     lambda: Call_Thread.start_timelapse(self))
        # self.preview_pushButton.clicked.connect(
        #     lambda: Call_Thread.start_preview(self))
        #
        # self.rotate_pushButton.clicked.connect(
        #     lambda: Functions.rotate_image(self))
        #
        # self.startInterval_pushButton.clicked.connect(
        #     lambda: Call_Thread.start_interval(self))
        # self.Interval_spinBox.valueChanged.connect(
        #     lambda: Functions.interval_Change(self))
        #
        # self.confirmCycle_pushButton.clicked.connect(
        #     lambda: Call_Thread.start_cycle(self))
        # self.onCycle_spinBox.valueChanged.connect(
        #     lambda: Functions.Cycle_Change(self))
        # self.offCycle_spinBox.valueChanged.connect(
        #     lambda: Functions.Cycle_Change(self))
        #
        # self.IR_pushButton.clicked.connect(lambda: Commands.IR_toggle(self))
        #
        # self.log_pushButton.clicked.connect(
        #     lambda: Functions.sensor_log(self))
        #
        # self.light_Confirm_pushButton.clicked.connect(
        #     lambda: Commands.light_confirm(self))
        # self.light_Reset_pushButton.clicked.connect(
        #     lambda: Commands.light_reset(self))
        #
        # self.title_lineEdit.textChanged.connect(
        #     lambda: Functions.IST_Edit(self))
        # self.addDate_pushButton.clicked.connect(
        #     lambda: Functions.add_date(self))
        #
        # self.ICI_spinBox.valueChanged.connect(
        #     lambda: Functions.ICI_Change(self))
        # self.ISD_spinBox.valueChanged.connect(
        #     lambda: Functions.ISD_Change(self))
        # self.directory_pushButton.clicked.connect(
        #     lambda: Functions.select_directory(self))
        #
        # self.x_resolution_spinBox.valueChanged.connect(
        #     lambda: Functions.camera_update(self))
        # self.y_resolution_spinBox.valueChanged.connect(
        #     lambda: Functions.camera_update(self))
        #
        # self.xAxis_horizontalSlider.valueChanged.connect(
        #     lambda: Functions.camera_update(self))
        # self.xAxis_horizontalSlider.sliderReleased.connect(
        #     lambda: Call_Thread.start_snapshot(self))
        #
        # self.yAxis_horizontalSlider.valueChanged.connect(
        #     lambda: Functions.camera_update(self))
        # self.yAxis_horizontalSlider.sliderReleased.connect(
        #     lambda: Call_Thread.start_snapshot(self))
        #
        # self.JPG_radioButton.toggled.connect(
        #     lambda: Functions.update_mode(self))
        # self.infraredImaging_checkBox.stateChanged.connect(
        #     lambda: Functions.IR_mode(self))
        #
        # self.fanSpeed_horizontalSlider.sliderReleased.connect(
        #     lambda: Functions.fanspeed_update(self))
        # self.fanSpeed_horizontalSlider.valueChanged.connect(
        #     lambda: UI_Update.fanlabel_update(self))


def main():
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
