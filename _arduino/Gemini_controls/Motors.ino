void motorStatus() {
  digitalWrite(EN_PIN_1, commands[2]);
  digitalWrite(EN_PIN_2, commands[3]);
}

void dirUpdate() {
  digitalWrite(DIR_PIN_1, commands[2]);
  digitalWrite(DIR_PIN_2, commands[3]);
}

void setDir(bool mot) {
  if (mot)
    digitalWrite(DIR_PIN_2, commands[2]);
  else
    digitalWrite(DIR_PIN_1, commands[2]);
}

void setMotor() {
  microstep_1 = commands[2];
  Serial.println(Motor_1.microsteps())
  Motor_1.rms_current(commands[3]);
  interval_1 = commands[4];

  microstep_2 = commands[5];
  Motor_2.rms_current(commands[6]);
  interval_2 = commands[7];

  ms_change = true;

}
