#include <TMC2208Stepper.h>
#include <Wire.h>
#include <avr/wdt.h>

#define DIR_PIN_1   10
#define STEP_PIN_1  11
#define EN_PIN_1    12

#define DIR_PIN_2   3
#define STEP_PIN_2  4
#define EN_PIN_2    5

#define BUZZER_PIN A8

#define SLAVE_ADDRESS 0x08
#define COMMANDSIZE 10

TMC2208Stepper Motor_1 = TMC2208Stepper(&Serial1);
TMC2208Stepper Motor_2 = TMC2208Stepper(&Serial2);

char data[50];
int commands[COMMANDSIZE];

//int MotorSpeed_1 = 10;
int interval_1 = 200;
int currentLimit_1 = 400;
int microstep_1 = 256;
boolean dir_1 = true;

//int MotorSpeed_2 = 10;
int interval_2 = 200;
int currentLimit_2 = 400;
int microstep_2 = 256;
boolean dir_2 = true;

boolean ms_change = false;

unsigned long NextTime_1 = 0;
unsigned long NextTime_2 = 0;

void setup() {
  Serial.begin(9600);

  Serial1.begin(115200);
  Motor_1.push();

  Serial2.begin(115200);
  Motor_2.push();

  pinMode(BUZZER_PIN, OUTPUT);

  pinMode(DIR_PIN_1, OUTPUT);
  pinMode(STEP_PIN_1, OUTPUT);
  pinMode(EN_PIN_1, OUTPUT);

  pinMode(DIR_PIN_2, OUTPUT);
  pinMode(STEP_PIN_2, OUTPUT);
  pinMode(EN_PIN_2, OUTPUT);

  digitalWrite(EN_PIN_1, HIGH);   // Disable driver in hardware
  digitalWrite(EN_PIN_2, HIGH);   // Disable driver in hardware

  Motor_1.pdn_disable(true);     // Use PDN/UART pin for communication
  Motor_1.I_scale_analog(false); // Use internal voltage reference
  Motor_1.rms_current(currentLimit_1);      // Set driver current 500mA
  Motor_1.toff(2);               // Enable driver in software
  Motor_1.mstep_reg_select(true);
  Motor_1.microsteps(microstep_1);
  //Motor_1.intpol(true);
  Motor_1.dedge(true);

  Motor_2.pdn_disable(true);     // Use PDN/UART pin for communication
  Motor_2.I_scale_analog(false); // Use internal voltage reference
  Motor_2.rms_current(currentLimit_2);      // Set driver current 500mA
  Motor_2.toff(2);               // Enable driver in software
  Motor_2.mstep_reg_select(true);
  Motor_2.microsteps(microstep_2);
  //Motor_2.intpol(true);
  Motor_2.dedge(true);

  //    digitalWrite(EN_PIN_1, LOW);   // Disable driver in hardware
  //    digitalWrite(EN_PIN_2, LOW);   // Disable driver in hardware

  uint32_t data = 0;
  Motor_1.DRV_STATUS(&data);
  Motor_2.DRV_STATUS(&data);

  Serial.begin(9600);
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);

  startup();
}

void loop() {
  if (ms_change)
  {
    Motor_1.microsteps(microstep_1);
    delay(10);
    Motor_2.microsteps(microstep_2);
    ms_change = false;
  }

  if (micros() < NextTime_1)
    NextTime_1 = micros();
  if (micros() < NextTime_2)
    NextTime_2 = micros();


  if (micros() - NextTime_1 > interval_1) {
    digitalWrite(STEP_PIN_1, !digitalRead(STEP_PIN_1));
    NextTime_1 = micros();         // reset for next pulse
  }

  if (micros() - NextTime_2 > interval_2) {
    digitalWrite(STEP_PIN_2, !digitalRead(STEP_PIN_2));
    NextTime_2 = micros();         // reset for next pulse
  }
}
