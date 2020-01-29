#include <DM542_driver.h>
DM542_driver mainM(2,3,4,5);

Motor R0(2,3,4,5,6);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
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

  int switchState = digitalRead(R0.getLimitPin());
  motorDirection = 1 - switchState;
  Serial.print("switchState: ");
  Serial.println(switchState);

  char rb;
  while (Serial.available() > 0) {
    rb = Serial.read();
    Serial.println(rb);
    if (rb == '0' || rb == '1' || rb == '2') {
      Serial.print("Change in motor direction: ");
      Serial.println(int(rb)-49); 
      motorDirection = int(rb)-49;
    }
  }
}
