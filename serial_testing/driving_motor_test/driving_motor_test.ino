#include <DM542_driver.h>
DM542_driver mainM(2,3,4,5);

Motor R0(0,1,2,3,4);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  delay(2000);
}
unsigned long previousTime = millis();

void loop() {
  // put your main code here, to run repeatedly:
  unsigned long currentTime = millis();

  //0.5rev/sec
  if (currentTime - previousTime > 50) {
    mainM.pulse();
    previousTime = currentTime;
  }

  switchState = digitalRead(R0._limit);
  if (switchState == 1) {
    motorDirection = 0;
  }

  while (Serial.available() > 0) {
    rb = Serial.read();
    if (rb == '0' || rb == '1' || rb == '2') {
      motorDirection = int(rb)-1;
    }
  }
}
