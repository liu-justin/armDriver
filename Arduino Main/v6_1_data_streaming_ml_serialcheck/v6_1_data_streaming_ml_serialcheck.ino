#include <Motor.h>
#include <MotorManager.h>
Motor R0(2,3,4,42,103);
Motor RA(5,6,7,34,81);

MotorManager mm(&R0, &RA);

int stepsPerRev = 800; // written on the motor driver
int minorSteps = stepsPerRev/200; // how many minor steps are in between the 200 major steps of a standard stepper motor

void setup() {
  Serial.begin(57600);
  
  // setting state to homing intialization
  mm.setAllStates(15);
  Serial.print("Arduino is ready for first Times/Dirs!");
  // keep looping until all time/dir timeNext/dirNext is filled
  waitAndReadInit();
  Serial.print("Ready to receive real data");

}

void loop() {
  unsigned long currentTime = millis();
  waitAndRead();
  
  for (int i = 0; i < MOTOR_COUNT; i++) {
    //Motor* motor = &mm.getMotor(i); was when i replaced all the mm.getMotor(i) with motor, but pointers are poop
    Serial.print("ml, motor "); Serial.print(i); Serial.print(" state: "); Serial.print(mm.getMotor(i)->getState()); Serial.print(", statePrev: "); Serial.print(mm.getMotor(i)->getStatePrevious()); Serial.print("; ");
 
    switch(mm.getMotor(i)->getState()){
      case 0: // error
        Serial.print(i);
        Serial.println(" errored, limit switch was pressed");
        break;
      case 1: // ready
        // might have a UI control, in which it sends data to motors and case 1 reads it
        // if all motors are ready, go to driving at 25
        if (mm.checkStates(1)) {

          mm.setAllStates(25);
        }
        break;

      case 2: // ready buffer, only to reset the statePrev
      case 5: // receiving from Python intialization
      case 6: // waiting for the start byte from Arduino
      case 7: // reading in data    
      case 8: // receiving from Python ending buffer, to reset statePrev
        break;

      case 15: // homing initialization
        mm.getMotor(i)->directionForward(); // i think backwards is CCW from drive side
        mm.getMotor(i)->setState(16);
        break;
        
      case 16: // homing
        if (currentTime - mm.getMotor(i)->previousTime > 50) { // 50 is a slow homing speed for 1600, for 800 its pretty fast
          mm.getMotor(i)->pulse();
          mm.getMotor(i)->previousTime = currentTime;
        } 

        // limit switch has been hit
        if (digitalRead(mm.getMotor(i)->getLimitPin()) == 1){
          mm.getMotor(i)->directionChange();
          
          mm.getMotor(i)->setStep(mm.getMotor(i)->getCCWFlag()*minorSteps); // need to add this to the initialization as a parameter
          mm.getMotor(i)->setState(17);
        }
        break;
        
      case 17: // homing ending, just getting off the limit switch so it isnt tripped while moving
        if (currentTime - mm.getMotor(i)->previousTime > 50) { // 50 is a slow homing speed
          mm.getMotor(i)->pulse();
          mm.getMotor(i)->previousTime = currentTime;
        } 
        
        // return to a known position, in this case im down 135deg from mark on each so i dont need a seperate home flag in the initialization
        if (mm.getMotor(i)->getStep()/minorSteps == 75){
          mm.getMotor(i)->setState(1);
        }
        break;
        
      case 25: // initialization of linear movement from timePy   
      case 26: // linear moving from delayTime array
        break;
      case 35: // initialization of relative movement
        break;
      case 45: // waiting for data from Python
        
        if (currentTime - mm.getMotor(i)->previousTime > mm.getMotor(i)->getTime()) {
          
            if (mm.getMotor(i)->getDir() != 0){
              // this could be backwards
              mm.getMotor(i)->setDirection(mm.getMotor(i)->getDir());
              mm.getMotor(i)->pulse();
              // only for when Python sends major steps only
  //            for (int j = 0; j < minorSteps; j++) {
  //              mm.getMotor(index)->pulse();
  //            }
            }
            mm.getMotor(i)->previousTime = currentTime;
            mm.getMotor(i)->consumeTime();
            mm.getMotor(i)->consumeDir();
            Serial.println("requesting more data");
        }
        if (digitalRead(mm.getMotor(i)->getLimitPin()) == 1){
          mm.getMotor(i)->setState(99);
        }
        break;
          
      }
      Serial.print("~ ");
    }
  }


void waitAndRead() {
    Serial.print("while waiting for a byte, ");
    while (Serial.available() >= 3) { // need the start byte, time byte, and dir byte; safeguard for when Arduino clears the buffer faster than Python can fill it
        byte rb = Serial.peek(); // peek instead of read, so I don't have to send two from Python
        Serial.print("got the following byte: "); Serial.print(rb); Serial.print(", ");
        if (rb >= 105 && rb < 105 + MOTOR_COUNT) {
          rb = Serial.read(); // clears the start byte
          int index = rb - 105;
          mm.getMotor(index)->receiveTime(Serial.read()); // grabs the time byte
          mm.getMotor(index)->receiveDir(Serial.read());  // grabs the dir byte
          Serial.println("got a byte, set the time/dir, and now requesting next byte ");
        }
        else {
          Serial.println("Serial did not start with a start byte");
        }
    }
}

void waitAndReadInit() {
    Serial.print("while waiting for a byte, ");
    while (Serial.available() >= 3) { // need the start byte, time byte, and dir byte; safeguard for when Arduino clears the buffer faster than Python can fill it
        byte rb = Serial.peek(); // peek instead of read, so I don't have to send two from Python
        Serial.print("got the following byte: "); Serial.print(rb); Serial.print(", ");
        if (rb >= 105 && rb < 105 + MOTOR_COUNT) {
          rb = Serial.read(); // clears the start byte
          int index = rb - 105;
          mm.getMotor(index)->enqueTime(Serial.read()); // grabs the time byte
          mm.getMotor(index)->enqueDir(Serial.read());  // grabs the dir byte
          Serial.println("got a byte, set the time/dir, and now requesting next byte ");
        }
        else {
          Serial.println("Serial did not start with a start byte");
        }
    }
}
