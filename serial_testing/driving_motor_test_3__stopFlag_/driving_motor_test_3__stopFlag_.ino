#include <DM542_driver.h>
DM542_driver mainM(2,3,4);
DM542_driver mainA(5,6,7);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  delay(1000);
  mainM.directionBackward();
  mainA.directionForward();
}
unsigned long previousTimeM = millis();
unsigned long previousTimeA = millis();
boolean stopM = false;
boolean stopA = false;

void loop() {
  // put your main code here, to run repeatedly:
  unsigned long currentTime = millis();

  //0.5rev/sec
  if (currentTime - previousTimeM > 50 && stopM == false) {
    mainM.pulse();
    previousTimeM = currentTime;
  }

  if (digitalRead(mainM.getLimitPin()) == 1) {
    //mainM.delayTimeTest = 100000000;
    stopM = true;
  }

  if (currentTime - previousTimeA > 50 && stopA == false) {
    mainA.pulse();
    previousTimeA = currentTime;
  }

  if (digitalRead(mainA.getLimitPin()) == 1) {
    //mainA.delayTimeTest = 100000000;
    stopA = true;
  }
  
}
