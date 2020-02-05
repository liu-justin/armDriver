#include <DM542_driver.h>
DM542_driver mainM(2,3,4,5);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.print("hello");
  delay(2000);

}
unsigned long previousTime = millis();

void loop() {

  // put your main code here, to run repeatedly:
  unsigned long currentTime = millis();

  if (currentTime - previousTime > 1) {
    mainM.pulse();
    previousTime = currentTime;
    Serial.println(mainM._stepCounter);

  }
  if (digitalRead(mainM.getLimitPin()) == 1){
    Serial.println(digitalRead(mainM.getLimitPin()));
        delay(9000000);
  }
//    Serial.print("This is the digitalRead: ");
//    Serial.println(digitalRead(mainM.getLimitPin()));
  
}
