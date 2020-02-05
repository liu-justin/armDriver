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

boolean homedM = false;
boolean homedA = false;

int pulsePerRev = 1600;
int minorPulses = pulsePerRev/200; // how many minipulses are between the major ones

void loop() {
  // put your main code here, to run repeatedly:
  unsigned long currentTime = millis();

  if (!homedM || !homedA) {
    //0.5rev/sec
    if (currentTime - previousTimeM > mainM.delayTimeTest) {
      mainM.pulse();
      previousTimeM = currentTime;
    }
  
    if (digitalRead(mainM.getLimitPin()) == 1) {
      homedM = true;
      mainM.delayTimeTest = 100000000;
      mainM._stepCounter = 42*minorPulses; // 42 from the markings on the main arm
      mainM.directionChange();
    }
  
    if (currentTime - previousTimeA > mainA.delayTimeTest) {
      mainA.pulse();
      previousTimeA = currentTime;
    }
  
    if (digitalRead(mainA.getLimitPin()) == 1) {
      homedA = true;
      mainA.delayTimeTest = 100000000;
      mainA._stepCounter = 80*minorPulses;
      mainA.directionChange();
    }

    if (homedA && homedM){
      mainM.delayTimeTest = 50;
      mainA.delayTimeTest = 50;
      delay(500);
    }
  }

  else {
    
    
    if (currentTime - previousTimeM > mainM.delayTimeTest) {
      mainM.pulse();
      Serial.println(mainM._stepCounter);
      Serial.println(mainM._stepCounter/minorPulses);
      previousTimeM = currentTime;
    }
    
    if (mainM._stepCounter == 75*minorPulses){
      mainM.delayTimeTest = 10000000;
    }

    if (currentTime - previousTimeA > mainA.delayTimeTest) {
      mainA.pulse();
      previousTimeA = currentTime;
    }

    if (mainA._stepCounter == 50*minorPulses){
      mainA.delayTimeTest = 10000000;
    }
  }
  
}
