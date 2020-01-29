#include <DM542_driver.h>
DM542_driver R0(2,3,4,42,103);
DM542_driver RA(5,6,7,34,81);

# define MOTOR_COUNT 2
DM542_driver motorList[MOTOR_COUNT] = {R0, RA};

int stepsPerRev = 1600; // written on the motor driver
int minorSteps = stepsPerRev/200; // how many minor steps are in between the 200 major steps of a standard stepper motor

void setup() {
  Serial.begin(9600);
  byte startR0Mark = 0x69;     // g,105
  byte startRAMark = 0x6A;     // h,106
  motorList[0].setStartReceivingByte(startR0Mark);
  motorList[1].setStartReceivingByte(startRAMark);
  // setting state to homing intialization
  for (int i = 0; i < MOTOR_COUNT; i++) {
    motorList[i].setState(5);
  }

}

void loop() {
  unsigned long currentTime = millis();
  
  for (int i = 0; i < MOTOR_COUNT; i++) {
    //DM542_driver* motor = &motorList[i]; was when i replaced all the motorList[i] with motor, but pointers are poop
    
    switch(motorList[i].getState()){
      case 0: // error
        Serial.print(i);
        Serial.println(" errored, limit switch was pressed");
        break;
        break;
      case 1: // ready
        break;

      case 5: // receiving from Python intialization
          // send a reserved char ~ 0x7e to tell Python that Arduino is ready
          Serial.write(0x7E);
          motorList[i].setState(6);
        break;

      case 6: // receiving from Python
        recvBytesWithEndMarkers(motorList[i]);
        break;

      case 15: // homing initialization
        motorList[i].directionForward(); // i think backwards is CCW from drive side
        motorList[i].setState(16);
        break;
        
      case 16: // homing
        if (currentTime - motorList[i].previousTime > 50) { // 50 is a slow homing speed
          motorList[i].pulse();
          motorList[i].previousTime = currentTime;
        } 

        // limit switch has been hit
        if (digitalRead(motorList[i].getLimitPin()) == 1){
          motorList[i].directionChange();
          motorList[i].setStep(motorList[i].getCCWFlag()*minorSteps); // need to add this to the initialization as a parameter
          motorList[i].setState(17);
        }
        break;
        
      case 17: // homing ending, just getting off the limit switch so it isnt tripped while moving
        if (currentTime - motorList[i].previousTime > 50) { // 50 is a slow homing speed
          motorList[i].pulse();
          motorList[i].previousTime = currentTime;
        } 

        // after a couple(arbitrary) of steps, stop
        if (abs(motorList[i].getStep()/minorSteps - motorList[i].getCCWFlag()) > 10){
          motorList[i].setState(1);
        }
        break;
        
      case 25: // initialization of linear movement from timePy
        motorList[i].previousTime = millis();
        motorList[i].setState(26);
        break;
        
      case 26: // linear moving from delayTime array
        if (currentTime - motorList[i].previousTime > motorList[i].timePy[motorList[i].getTimePyCounter()]) {
          motorList[i].pulse();
          motorList[i].previousTime = currentTime;
          motorList[i].incrementTimePyCounter();
        }

        // if it hits a limit switch, go to 99(error), it went out of bounds
        if (digitalRead(motorList[i].getLimitPin()) == 1){
          motorList[i].setState(99);
        }

        // should be if the proper number read (last number mark of timePy)
        if (motorList[i].getTimePyCounter() > NUM_BYTES) {
          motorList[i].setState(1);
        }
        break;
    }
  }
}

int timeIndex = 0;
int directionIndex = 0;
int *timePointer;
int *directionPointer;

void recvBytesWithEndMarkers(DM542_driver motor) {
    
    byte stepUpMark = 0x78;   // {,120
    byte stepEvenMark = 0x79; // |,121
    byte stepDownMark = 0x7A; // },122
    byte startReceivingMark = 0x65;    // e,101
    byte endMark = 0x66;      // f,102

    byte rb;
    Serial.println("Before the loop does this happen again");
    while (Serial.available() > 0) {
        rb = Serial.read();
        Serial.print("Arduino got the following byte: ");
        Serial.print(rb);
        Serial.print("| ");
        
        // the byte is a direction byte
        if (rb == stepUpMark || rb == stepEvenMark || rb == stepDownMark) {
            Serial.print("Arduino received a direction byte; ");
            *(directionPointer + directionIndex) = rb - '|'; // I think this in Python is just motor.dirPy[directionIndex] = rb + '|'
            directionIndex++;
            if (directionIndex >= NUM_BYTES) {
                directionIndex = NUM_BYTES - 1;
            }
        }

        else if (rb == startR0Mark || rb == startRAMark) {
          if (rb == motor.getStartReceivingByte()) {
            Serial.print("Arduino received a start receiving byte and it has a match; ");
            memset(motor.timePy, 0, NUM_BYTES); // memset is populates the array with zeros
            memset(motor.dirPy, 0, NUM_BYTES);
            timeIndex = 0; // reset both indices
            directionIndex = 0;
            timePointer = motor.timePy; // point the pointers to the head of the array
            directionPointer = motor.dirPy;
          }
          
        }

        // the byte is the endMark
        else if (rb == endMark) {
            Serial.println("{endMark}");
            
        }

        else {
            Serial.print("Arduino received a time byte, this is the timeIndex: ");
            Serial.print(timeIndex);
            Serial.print("| ");
            *(timePointer + timeIndex) = rb;
            timeIndex++;
            if (timeIndex >= NUM_BYTES) {
                timeIndex = NUM_BYTES - 1;
            }
            motor.showTimePy();
            Serial.write(0x7E);
        }
    }
}
