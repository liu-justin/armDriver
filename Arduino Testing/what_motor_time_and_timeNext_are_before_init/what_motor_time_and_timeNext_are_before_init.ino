#include <Motor.h>
#include <MotorManager.h>
Motor R0(2,3,4,42,103);
Motor RA(5,6,7,34,81);

// without initialization, they are 0; intializing with NULL is 0

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.print(R0.getTime());
  R0.enqueTime(6);
  Serial.print(R0.getTime());
  R0.enqueTime(9);
  Serial.print(R0.getTime());
  R0.consumeTime();
  Serial.print(R0.getTime());
  
}

void loop() {
  // put your main code here, to run repeatedly:

}
