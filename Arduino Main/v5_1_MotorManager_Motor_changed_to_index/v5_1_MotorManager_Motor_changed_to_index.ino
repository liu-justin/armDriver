#include <Motor.h>
#include <MotorManager.h>
Motor R0(2,3,4,42,103);
Motor RA(5,6,7,34,81);

MotorManager mm(&R0, &RA);

int stepsPerRev = 800; // written on the motor driver
int minorSteps = stepsPerRev/200; // how many minor steps are in between the 200 major steps of a standard stepper motor

void setup() {
  Serial.begin(9600);
  byte startR0Mark = 0x69;     // g,105
  byte startRAMark = 0x6A;     // h,106
  R0.setStartReceivingByte(startR0Mark);
  RA.setStartReceivingByte(startRAMark);
  // setting state to homing intialization
  mm.setAllStates(5);

}

void loop() {
  unsigned long currentTime = millis();
  
  for (int i = 0; i < MOTOR_COUNT; i++) {
    //Motor* motor = &mm.getMotor(i); was when i replaced all the mm.getMotor(i) with motor, but pointers are poop
    Serial.print("ml, motor "); Serial.print(i); Serial.print(" state: "); Serial.print(mm.getMotor(index)->getState()); Serial.print("~ ");

    
    switch(mm.getMotor(index)->getState()){
      case 0: // error
        Serial.print(i);
        Serial.println(" errored, limit switch was pressed");
        break;
      case 1: // ready
        // might have a UI control, in which it sends data to motors and case 1 reads it
        // if all motors are ready, go to driving at 25
        if (mm.checkStates(1)) {
//          mm.getMotor(index)->showTimePy();
//          mm.getMotor(index)->showDirPy();
          mm.setAllStates(25);
        }
        break;

      case 5: // receiving from Python intialization
          mm.getMotor(index)->setState(6);
          Serial.print("s6");
        break;

      case 6: // waiting for the start byte from Arduino
        waitingForStartByte(mm.getMotor(i));
        break;

      case 7: // reading in data
        Serial.print("s7");
        Serial.print("~ ");
        readingDataFromPy(mm.getMotor(i));
        break;

      case 15: // homing initialization
        mm.getMotor(index)->directionForward(); // i think backwards is CCW from drive side
        mm.getMotor(index)->setState(16);
        break;
        
      case 16: // homing
        if (currentTime - mm.getMotor(index)->previousTime > 50) { // 50 is a slow homing speed for 1600, for 800 its pretty fast
          mm.getMotor(index)->pulse();
          mm.getMotor(index)->previousTime = currentTime;
        } 

        // limit switch has been hit
        if (digitalRead(mm.getMotor(index)->getLimitPin()) == 1){
          mm.getMotor(index)->directionChange();
          
          mm.getMotor(index)->setStep(mm.getMotor(index)->getCCWFlag()*minorSteps); // need to add this to the initialization as a parameter
          mm.getMotor(index)->setState(17);
        }
        break;
        
      case 17: // homing ending, just getting off the limit switch so it isnt tripped while moving
        if (currentTime - mm.getMotor(index)->previousTime > 50) { // 50 is a slow homing speed
          mm.getMotor(index)->pulse();
          mm.getMotor(index)->previousTime = currentTime;
        } 
        
        // return to a known position, in this case im down 135deg from mark on each so i dont need a seperate home flag in the initialization
        if (mm.getMotor(index)->getStep()/minorSteps == 75){
          mm.getMotor(index)->setState(1);
        }
        break;
        
      case 25: // initialization of linear movement from timePy
        mm.getMotor(index)->previousTime = millis();
        mm.getMotor(index)->previousMajorStep = mm.getMotor(index)->getStep();
        mm.getMotor(index)->setState(26);
        break;
        
      case 26: // linear moving from delayTime array
        if (currentTime - mm.getMotor(index)->previousTime > mm.getMotor(index)->timePy[mm.getMotor(index)->getTimePyCounter()]) {
          if (mm.getMotor(index)->dirPy[mm.getMotor(index)->getTimePyCounter()] != 0){
            // this could be backwards
            mm.getMotor(index)->setDirection(mm.getMotor(index)->dirPy[mm.getMotor(index)->getTimePyCounter()]);
            mm.getMotor(index)->pulse();
            // only for when Python sends major steps only
//            for (int j = 0; j < minorSteps; j++) {
//              mm.getMotor(index)->pulse();
//            }
          }
          mm.getMotor(index)->previousTime = currentTime;
          mm.getMotor(index)->incrementTimePyCounter();
        }

        // if it hits a limit switch, go to 99(error), it went out of bounds
        if (digitalRead(mm.getMotor(index)->getLimitPin()) == 1){
          mm.getMotor(index)->setState(99);
        }

        // should be if the proper number read (last number mark of timePy)
        if (mm.getMotor(index)->getTimePyCounter() > NUM_BYTES) {
          mm.getMotor(index)->setState(1);
        }
        break;

      case 35: // initialization of relative movement
        break;
    }
  }
}

int timeIndex = 0;
int directionIndex = 0;
int *timePointer;
int *directionPointer;

void waitingForStartByte(int index) {
    if (Serial.available() > 0) {
        byte rb = Serial.read();
        Serial.print("Motor ");
        Serial.print(mm.getMotor(index)->getStartReceivingByte());
        Serial.print(" got the following byte: ");
        Serial.print(rb);
        Serial.print("~ ");

        if (rb == mm.getMotor(index)->getStartReceivingByte()) {
            
            memset(mm.getMotor(index)->timePy, 0, NUM_BYTES); // memset is populates the array with zeros
            memset(mm.getMotor(index)->dirPy, 0, NUM_BYTES);
            timeIndex = 0; // reset both indices
            directionIndex = 0;
            timePointer = mm.getMotor(index)->timePy; // point the pointers to the head of the array
            directionPointer = mm.getMotor(index)->dirPy;
            mm.getMotor(index)->setState(7);
            mm.setAllStatesBut(1, index); 
            Serial.println("yay Arduino received a start receiving byte ");
            Serial.println("second time for catching Arduino received a start receiving byte");
        }
        else {
          Serial.println("nope Arduino received a start receiving byte ");
        }
    }
    else {
      Serial.println("waiting for serial for the start byte");
    }

}

void readingDataFromPy(int index) {
    byte stepUpMark = 0x78;   // x,120
    byte stepEvenMark = 0x79; // y,121
    byte stepDownMark = 0x7A; // z,122
    byte topTimeMark = 0x64;  //   100
    byte endMark = 0x66;      // f,102

    byte rb;
    while (Serial.available() > 0) {
      rb = Serial.read();
      Serial.print("Motor ");
      Serial.print(mm.getMotor(index)->getStartReceivingByte());
      Serial.print(" got the following byte: ");
      Serial.print(rb);
      Serial.print("~ ");
      
      // the byte is a direction byte
      if (rb == stepUpMark || rb == stepEvenMark || rb == stepDownMark) {
//          Serial.print("Arduino received a direction byte; ");
          *(directionPointer + directionIndex) = rb - 'y'; // I think this in Python is just motor.dirPy[directionIndex] = rb + '|'
          directionIndex++;
          if (directionIndex >= NUM_BYTES) {
              directionIndex = NUM_BYTES - 1;
          }
      }
    
      else if (rb <= topTimeMark) {
          *(timePointer + timeIndex) = rb;
          timeIndex++;
          if (timeIndex >= NUM_BYTES) {
              timeIndex = NUM_BYTES - 1;
          }
          Serial.print("Arduino received a time byte;");
//          Serial.print(", this is the timeIndex: ");
//          Serial.print(timeIndex);
//          Serial.print("| ");
//          
//          Serial.print("~ ");
      }

      else if (rb == endMark) {
        
        Serial.print("Arduino received an endMark;");
        mm.getMotor(index)->setState(15);
        mm.revertAllStatesBut(index);
      }
    }
}
