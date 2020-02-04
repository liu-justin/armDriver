#include <Motor.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdarg.h>

Motor R0(2,3,4,42,103);
Motor RA(5,6,7,34,81);

void setup() {
  Serial.begin(9600);
  motorVariadic(2, &R0, &RA);
}

void loop() {
  // put your main code here, to run repeatedly:

}

// first param is how many params you want to average, the rest are the params
// this works

Motor* motorList[2];

void motorVariadic(int count, ...)
{
    va_list ap;
    int j;

    va_start(ap, count); /* Requires the last fixed parameter (to get the address) */
    for (j = 0; j < count; j++) {
        motorList[j] = va_arg(ap, Motor*);
        Serial.println(motorList[j]->getCCWFlag());
    }
    va_end(ap);
}
