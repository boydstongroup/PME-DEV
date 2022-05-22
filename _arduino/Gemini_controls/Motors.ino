void motorStatus() {
  digitalWrite(EN_PIN_1, commands[2]);
  digitalWrite(EN_PIN_2, commands[3]);
}

void dirUpdate() {
  digitalWrite(DIR_PIN_1, commands[2]);
  digitalWrite(DIR_PIN_2, commands[3]);
}

void setInterval() {
  interval_1 = commands[2];
  interval_2 = commands[3];
  
}

void setMicrosteps() {
  Motor_1.microsteps(commands[2]);
  Motor_2.microsteps(commands[3]);
  
}

void setCurrentLimit() {
  Motor_1.rms_current(commands[2]);
  Motor_2.rms_current(commands[3]);
  
}
