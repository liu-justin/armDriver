// errors in this stuff
//#include <StandardCplusplus.h>
//#include <system_configuration.h>
//#include <unwind-cxx.h>
//#include <utility.h>

#include <Motor.h>
#include <MotorManager.h>
Motor R0(2,3,4,42,103);
Motor RA(5,6,7,34,81);

// if you want to add motors, need to add the adjust the MOTORLISTLENGTH in MotorManager
MotorManager mm(&R0, &RA);

// importing this stuff from StandardC++ library didnt work
//std::vector<int> v;

void setup() {
  
  Serial.begin(9600);
  
  R0.setState(10);
  Serial.println(R0.getState());
  Serial.println(mm.getMotor(0)->getState());
  mm.setAllStates(15);
  Serial.println(mm.getMotor(0)->getState());
  Serial.println(mm.getMotor(1)->getState());
 
 //motorVariadic(2, &R0, &RA);

// have to do work on this, set this up for Motors instead of string
//  vector v;
//  vector_init(&v);
//  vector_add(&v, &R0);
//  vector_add(&v, &RA);
//  for (int i = 0; i < vector_total(&v); i++)
//    Serial.println(vector_get(&v, i).getState());
}

void loop() {
  // put your main code here, to run repeatedly:

}

//Motor* motorList[2];
//
//// first param is how many params you want to average, the rest are the params
//// this works
//void motorVariadic(int count, ...)
//{
//    va_list ap;
//    int j;
//
//    va_start(ap, count); /* Requires the last fixed parameter (to get the address) */
//    for (j = 0; j < count; j++) {
//        motorList[j] = va_arg(ap, Motor*);
//        Serial.println(motorList[j]->getCCWFlag());
//    }
//    va_end(ap);
//}
