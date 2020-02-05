#include <Motor.h>
#include <DM542_driver.h>

//#Motor R0(2,3,4,5,6);
DM542_driver mainM(2,3,4,5);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

}
unsigned long previousTime = millis();

void loop() {

  // put your main code here, to run repeatedly:
  unsigned long currentTime = millis();

  if (currentTime - previousTime > 10) {
    //R0.step1(motorDirection);
    //Serial.println(R0._stepCounter);
    mainM.pulse();
    previousTime = currentTime;
  }
  /*
  if (R0._stepCounter == 120) {
    delay(500);
    motorDirection = motorDirection * -1;
  }
  if (R0._stepCounter == -10) {
    //delay(1000*60*60*6);
    delay(2000);
    motorDirection = motorDirection * -1;
  }*/
}
