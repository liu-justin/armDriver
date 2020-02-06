#include <Motor.h>
//#include <MotorManager.h>
Motor R0(2,3,4,42,103);
Motor RA(5,6,7,34,81);

# define MOTOR_COUNT 2
Motor* motorList[MOTOR_COUNT] = {&R0, &RA};

int stepsPerRev = 800; // written on the motor driver
int minorSteps = stepsPerRev/200; // how many minor steps are in between the 200 major steps of a standard stepper motor

void setup() {
  Serial.begin(9600);
  byte startR0Mark = 0x69;     // g,105
  byte startRAMark = 0x6A;     // h,106
  R0.setStartReceivingByte(startR0Mark);
  RA.setStartReceivingByte(startRAMark);
  // setting state to homing intialization
  for (int i = 0; i < MOTOR_COUNT; i++) {
    motorList[i]->setState(5);
  }

}

void loop() {
  unsigned long currentTime = millis();
  
  for (int i = 0; i < MOTOR_COUNT; i++) {
    //Motor* motor = &motorList[i]; was when i replaced all the motorList[i] with motor, but pointers are poop
    Serial.print("ml, motor "); Serial.print(i); Serial.print(" state: "); Serial.print(motorList[i]->getState()); Serial.print("~ ");

    
    switch(motorList[i]->getState()){
      case 0: // error
        Serial.print(i);
        Serial.println(" errored, limit switch was pressed");
        break;
      case 1: // ready

        // if all motors are ready, go to driving at 25
        if (motorList[1-i]->getState() == 1) {
//          motorList[i]->showTimePy();
//          motorList[i]->showDirPy();
          motorList[i]->setState(25);
          motorList[1-i]->setState(25);
        }
        break;

      case 5: // receiving from Python intialization
          // send a reserved char ~ 0x7e to tell Python that Arduino is ready
          //Serial.print("Arduino is ready, going to state 6; ");
          
          motorList[i]->setState(6);
          Serial.print("s6");
        break;

      case 6: // waiting for the start byte from Arduino
        waitingForStartByte(motorList[i]);
        break;

      case 7: // reading in data
        Serial.print("s7");
        Serial.print("~ ");
        readingDataFromPy(motorList[i]);
        break;

      case 15: // homing initialization
        motorList[i]->directionForward(); // i think backwards is CCW from drive side
        motorList[i]->setState(16);
        break;
        
      case 16: // homing
        if (currentTime - motorList[i]->previousTime > 50) { // 50 is a slow homing speed
          motorList[i]->pulse();
          motorList[i]->previousTime = currentTime;
        } 

        // limit switch has been hit
        if (digitalRead(motorList[i]->getLimitPin()) == 1){
          motorList[i]->directionChange();
          
          motorList[i]->setStep(motorList[i]->getCCWFlag()*minorSteps); // need to add this to the initialization as a parameter
          motorList[i]->setState(17);
        }
        break;
        
      case 17: // homing ending, just getting off the limit switch so it isnt tripped while moving
        if (currentTime - motorList[i]->previousTime > 50) { // 50 is a slow homing speed
          motorList[i]->pulse();
          motorList[i]->previousTime = currentTime;
        } 
        
        // return to a known position, in this case im down 135deg from mark on each so i dont need a seperate home flag in the initialization
        if (motorList[i]->getStep()/minorSteps == 75){
          motorList[i]->setState(1);
        }
        break;
        
      case 25: // initialization of linear movement from timePy
        motorList[i]->previousTime = millis();
        motorList[i]->previousMajorStep = motorList[i]->getStep();
        motorList[i]->setState(26);
        break;
        
      case 26: // linear moving from delayTime array
        if (currentTime - motorList[i]->previousTime > motorList[i]->timePy[motorList[i]->getTimePyCounter()]) {
          if (motorList[i]->dirPy[motorList[i]->getTimePyCounter()] != 0){
            // this could be backwards
            motorList[i]->setDirection(motorList[i]->dirPy[motorList[i]->getTimePyCounter()]);
            motorList[i]->pulse();
            // only for when Python sends major steps only
//            for (int j = 0; j < minorSteps; j++) {
//              motorList[i]->pulse();
//            }
          }
          motorList[i]->previousTime = currentTime;
          motorList[i]->incrementTimePyCounter();
        }

        // if it hits a limit switch, go to 99(error), it went out of bounds
        if (digitalRead(motorList[i]->getLimitPin()) == 1){
          motorList[i]->setState(99);
        }

        // should be if the proper number read (last number mark of timePy)
        if (motorList[i]->getTimePyCounter() > NUM_BYTES) {
          motorList[i]->setState(1);
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

void waitingForStartByte(Motor* motor) {
    if (Serial.available() > 0) {
        byte rb = Serial.read();
        Serial.print("Motor ");
        Serial.print(motor->getStartReceivingByte());
        Serial.print(" got the following byte: ");
        Serial.print(rb);
        Serial.print("~ ");

        if (rb == motor->getStartReceivingByte()) {
            
            memset(motor->timePy, 0, NUM_BYTES); // memset is populates the array with zeros
            memset(motor->dirPy, 0, NUM_BYTES);
            timeIndex = 0; // reset both indices
            directionIndex = 0;
            timePointer = motor->timePy; // point the pointers to the head of the array
            directionPointer = motor->dirPy;
            motor->setState(7);
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

void readingDataFromPy(Motor* motor) {
    byte stepUpMark = 0x78;   // x,120
    byte stepEvenMark = 0x79; // y,121
    byte stepDownMark = 0x7A; // z,122
    byte topTimeMark = 0x64;  //   100
    byte endMark = 0x66;      // f,102

    byte rb;
    while (Serial.available() > 0) {
      rb = Serial.read();
      Serial.print("Motor ");
      Serial.print(motor->getStartReceivingByte());
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
        motor->setState(15);
      }
    }
}
