#include <Motor.h>
#include <MotorManager.h>
Motor R0(2,3,4,42,103);
Motor RA(5,6,7,34,81);

// if you want to add motors, need to add the adjust the MOTORLISTLENGTH in MotorManager
MotorManager mm(&R0, &RA);

void setup() {
  
  Serial.begin(9600);
  
  R0.setState(10);
  Serial.println(R0.getState());
  Serial.println(mm.getMotor(0)->getState());
  mm.setAllStates(15);
  Serial.println(mm.getMotor(0)->getState());
  Serial.println(mm.getMotor(1)->getState());

}

void loop() {
  // put your main code here, to run repeatedly:

}
