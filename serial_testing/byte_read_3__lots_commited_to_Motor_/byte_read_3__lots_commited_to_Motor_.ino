#include <Motor.h>

boolean reading = true;
boolean driving = false;

unsigned long previousTime = 0;
int rIndex = 0;
int cIndex = 0;

Motor r(0,1,2,3);
Motor c(4,5,6,7);

void setup() {
    Serial.begin(9600);
    Serial.println("<Arduino is ready>");
}

void loop() {
    if (reading == true) {
        recvBytesWithEndMarkers();
    }
    if (driving == true) {
        //driveMotors();
    }
    
}

void recvBytesWithEndMarkers() {
    
    byte stepUpMark = 0x7B;   // {,123
    byte stepEvenMark = 0x7C; // |,124
    byte stepDownMark = 0x7D; // },125
    byte startMark = 0x65;    // e,101
    byte endMark = 0x66;      // f,102
    byte startRMark = 0x67;     // g,103
    byte startCMark = 0x68;     // h,104

    int timeIndex = 0;
    int directionIndex = 0;
    int *timePointer;
    int *directionPointer;

    byte rb;
   
    while (Serial.available() > 0) {
        rb = Serial.read();
        showData();
        Serial.print("start of loop, Serial.available: ");
        Serial.print(Serial.available());
        Serial.print(" data read: ");
        Serial.println(rb);
        

        // the byte is a direction byte
        if (rb == stepUpMark || rb == stepEvenMark || rb == stepDownMark) {
            *(directionPointer + directionIndex) = rb - '|';
            directionIndex++;
            if (directionIndex >= numBytes) {
                directionIndex = numBytes - 1;
            }
        }

        else if (rb == startRMark) {
            // want the time and direction arrays to point to the correct array(in this case R)
            memset(r.delayTime, 0, numBytes);
            memset(r.stepDirection, 0, numBytes);
            timeIndex = 0;
            directionIndex = 0;
            timePointer = r.delayTime;
            directionPointer = r.stepDirection;
        }

        else if (rb == startCMark) {
            Serial.println("start C");
            memset(c.delayTime, 0, numBytes);
            memset(c.stepDirection, 0, numBytes);
            timeIndex = 0;
            directionIndex = 0;
            timePointer = c.delayTime;
            directionPointer = c.stepDirection;
        }

        // the byte is the endMark
        else if (rb == endMark) {
            reading = false;
            driving = true;
            Serial.println("endMark");
            showData();
            previousTime = millis();
            
        }

        else {        
            Serial.println(timeIndex);
            *(timePointer + timeIndex) = rb;
            timeIndex++;
            if (timeIndex >= numBytes) {
                timeIndex = numBytes - 1;
            }
        }
    }
}

void showData() {
        Serial.print("This just in (R delay time)... ");
        for (byte n = 0; n < 64; n++) {
            Serial.print(r.delayTime[n]);
            Serial.print(' ');
        }
        Serial.println();
        
        Serial.print("This just in (C delay time)... ");
        for (byte n = 0; n < 64; n++) {
            Serial.print(c.delayTime[n]);
            Serial.print(' ');
        }
        Serial.println();
}

void driveMotors() {
    unsigned long currentTime = millis();
    if (currentTime - previousTime > r.delayTime[rIndex]){
        // step the motors in the direction of stepDirectionR[rIndex]
        r.step1(r.stepDirection[rIndex]);
        rIndex++;
    }
    
    if (currentTime - previousTime > c.delayTime[cIndex]){
        c.step1(c.stepDirection[cIndex]);
        cIndex++;
    }

    if (rIndex >= 64 and cIndex >= 64) {
        driving = false;
        reading = true;
    }

}
