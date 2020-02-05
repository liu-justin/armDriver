//#include <StandardCplusplus.h>
//#include <system_configuration.h>
//#include <unwind-cxx.h>
//#include <utility.h>

#include <Motor.h>
#include <MotorManager.h>
#include <stdio.h>
#include <stdarg.h>

Motor R0(2,3,4,42,103);
Motor RA(5,6,7,34,81);

MotorManager mm(2, &R0, &RA);
  
  // Serial.println(mm._motorList[0].getState());
void setup() {
  Serial.begin(9600);
  
  R0.setState(10);
  Serial.println(R0.getState());
  Serial.println(mm._motorList[0]->getState());
 

  //motorVariadic(2, &R0, &RA);
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
