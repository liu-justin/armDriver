#include <Motor.h>

//const int numBytes = 64;
int delayTimeR[numBytes] = {0};
int stepDirectionR[numBytes];
int delayTimeC[numBytes] = {0};
int stepDirectionC[numBytes];
byte numReceived = 0;

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
        showNewData();
    }
    if (driving == true) {
        driveMotors();
    }
    
}

void recvBytesWithEndMarkers() {
    
    byte stepUpMark = 0x7B;   // {,123
    byte stepEvenMark = 0x7C; // |,124
    byte stepDownMark = 0x7D; // },125
    byte startMark = 0x65;    // e,101
    byte endMark = 0x66;      // f,102
    byte endRMark = 0x67;     // g,103
    byte endCMark = 0x68;     // h,104

    static byte timeIndex = 0;
    static byte directionIndex = 0;
    int time[numBytes];
    int direction[numBytes];

    byte rb;
   
    while (Serial.available() > 0) {
        rb = Serial.read();
        Serial.println(rb, HEX);
        Serial.println(rb, BIN);

        // the byte is a direction byte
        if (rb == stepUpMark || rb == stepEvenMark || rb == stepDownMark) {
            direction[directionIndex] = rb - '|';
            directionIndex++;
            if (directionIndex >= numBytes) {
                directionIndex = numBytes - 1;
            }
        }

        else if (rb == endRMark) {
            memcpy(delayTimeR, time, numBytes);
            memcpy(stepDirectionR, direction, numBytes);
            r.forward1();

            memset(time, 0, sizeof(time));
            memset(direction, 0, sizeof(direction));
            timeIndex = 0;
            directionIndex = 0;
        }

        else if (rb = endCMark) {
            memcpy(delayTimeC, time, numBytes);
            memcpy(stepDirectionC, direction, numBytes);

            memset(time, 0, sizeof(time));
            memset(direction, 0, sizeof(direction));
            timeIndex = 0;
            directionIndex = 0;
        }

        // the byte is the endMark
        else if (rb == endMark) {
            reading = false;
            driving = true;
            showNewData();
            previousTime = millis();
            
        }

        else {        
            time[timeIndex] = rb;
            timeIndex++;
            if (timeIndex >= numBytes) {
                timeIndex = numBytes - 1;
            }
        }
    }
}

void showNewData() {
        Serial.print("This just in (delay time)... ");
        for (byte n = 0; n < numReceived; n++) {
            Serial.print(delayTimeR[n]);
            Serial.print(' ');
        }
        Serial.println();
        
        Serial.print("This just in (step direction)... ");
        for (byte n = 0; n < numReceived; n++) {
            Serial.print(stepDirectionR[n]);
            Serial.print(' ');
        }
        Serial.println();
}

void driveMotors() {
    unsigned long currentTime = millis();
    if (currentTime - previousTime > delayTimeR[rIndex]){
        // step the motors in the direction of stepDirectionR[rIndex]
        r.step1(stepDirectionR[rIndex]);
        rIndex++;
    }
    
    if (currentTime - previousTime > delayTimeC[cIndex]){
        c.step1(stepDirectionC[cIndex]);
        cIndex++;
    }

    if (rIndex >= sizeof(delayTimeR) and cIndex >= sizeof(delayTimeC)) {
        driving = false;
        reading = true;
    }

}
