import Settings
import UI_Update
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

#
# def reverse_motor(mot, self):
#     if Settings.LINKED:
#         Settings.frame_dir = not Settings.frame_dir
#         Settings.core_dir = not Settings.core_dir
#     else:
#         if not mot:
#             Settings.frame_dir = not Settings.frame_dir
#
#         else:
#             Settings.core_dir = not Settings.core_dir
#     CMD = ("1~1~" + str(int(Settings.frame_dir)) +
#            "~" + str(int(Settings.core_dir)))
#     Settings.sendCMD(CMD)
#     UI_Update.dir(self)
#
#
# def spin_change(mot, self):
#     self.core_spinBox.blockSignals(True)
#     self.frame_spinBox.blockSignals(True)
#     self.core_verticalSlider.blockSignals(True)
#     self.frame_verticalSlider.blockSignals(True)
#
#     if Settings.LINKED:
#         if not mot:
#             if int(decimal.Decimal(str(self.frame_spinBox.value())) * 100) in Settings.speed_dict:
#                 Settings.frame_RPM = self.frame_spinBox.value()
#                 Settings.core_RPM = Settings.frame_RPM
#
#                 self.frame_verticalSlider.setValue(Settings.frame_RPM * 20)
#                 self.core_verticalSlider.setValue(Settings.core_RPM * 20)
#
#                 self.core_spinBox.setValue(Settings.core_RPM)
#             else:
#                 Settings.frame_RPM = self.frame_verticalSlider.sliderPosition() / 20
#
#         else:
#             if int(decimal.Decimal(str(self.core_spinBox.value())) * 100) in Settings.speed_dict:
#                 Settings.core_RPM = self.core_spinBox.value()
#                 Settings.frame_RPM = Settings.core_RPM
#
#                 self.frame_verticalSlider.setValue(Settings.frame_RPM * 20)
#                 self.core_verticalSlider.setValue(Settings.core_RPM * 20)
#
#                 self.frame_spinBox.setValue(Settings.frame_RPM)
#             else:
#                 Settings.core_RPM = self.core_verticalSlider.sliderPosition() / 20
#     else:
#         if not mot:
#             if int(decimal.Decimal(str(self.frame_spinBox.value())) * 100) in Settings.speed_dict:
#                 Settings.frame_RPM = self.frame_spinBox.value()
#                 self.frame_verticalSlider.setValue(Settings.frame_RPM * 20)
#             else:
#                 Settings.frame_RPM = self.frame_verticalSlider.sliderPosition() / 20
#         else:
#             if int(decimal.Decimal(str(self.core_spinBox.value())) * 100) in Settings.speed_dict:
#                 Settings.core_RPM = self.core_spinBox.value()
#                 self.core_verticalSlider.setValue(Settings.core_RPM * 20)
#             else:
#                 Settings.core_RPM = self.core_verticalSlider.sliderPosition() / 20
#     self.core_spinBox.blockSignals(False)
#     self.frame_spinBox.blockSignals(False)
#     self.core_verticalSlider.blockSignals(False)
#     self.frame_verticalSlider.blockSignals(False)
#
#     CMD = "1~2~" + getMicrostep(Settings.frame_RPM * 100) + "~" + str(Settings.speed_dict[int(decimal.Decimal(str(
#         Settings.frame_RPM)) * 100)]) + "~" + str(getMicrostep(Settings.core_RPM * 100)) + "~" + str(Settings.speed_dict[int(decimal.Decimal(str(
#             Settings.core_RPM)) * 100)])
#     Settings.sendCMD(CMD)
#
#
# def slider_change(mot, self):
#     self.core_spinBox.blockSignals(True)
#     self.frame_spinBox.blockSignals(True)
#     self.core_verticalSlider.blockSignals(True)
#     self.frame_verticalSlider.blockSignals(True)
#
#     if Settings.LINKED:
#         if not mot:
#             Settings.frame_RPM = self.frame_verticalSlider.sliderPosition() / 20
#             Settings.core_RPM = Settings.frame_RPM
#             self.core_verticalSlider.setValue(Settings.core_RPM * 20)
#
#         else:
#             Settings.core_RPM = self.core_verticalSlider.sliderPosition() / 20
#             Settings.frame_RPM = Settings.core_RPM
#             self.frame_verticalSlider.setValue(Settings.frame_RPM * 20)
#         self.frame_spinBox.setValue(Settings.frame_RPM)
#         self.core_spinBox.setValue(Settings.core_RPM)
#     else:
#         if not mot:
#             Settings.frame_RPM = self.frame_verticalSlider.sliderPosition() / 20
#             self.frame_spinBox.setValue(Settings.frame_RPM)
#         else:
#             Settings.core_RPM = self.core_verticalSlider.sliderPosition() / 20
#             self.core_spinBox.setValue(Settings.core_RPM)
#
#     self.core_spinBox.blockSignals(False)
#     self.frame_spinBox.blockSignals(False)
#     self.core_verticalSlider.blockSignals(False)
#     self.frame_verticalSlider.blockSignals(False)
#
#
# def slider_Released():
#     CMD = "1~2~" + getMicrostep(Settings.frame_RPM * 100) + "~" + str(Settings.speed_dict[int(decimal.Decimal(str(Settings.frame_RPM)) * 100)]) + "~" + getMicrostep(
#         Settings.core_RPM * 100) + "~" + str(Settings.speed_dict[int(decimal.Decimal(str(Settings.core_RPM)) * 100)])
#     Settings.sendCMD(CMD)
