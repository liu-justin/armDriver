
// Example 6 - Receiving binary data

const byte numBytes = 64;
int delayTimeR[numBytes];
int stepDirectionR[numBytes];
int delayTimeC[numBytes];
int stepDirectionC[numBytes];
byte numReceived = 0;

boolean reading = false;
boolean driving = false;

unsigned long previousTime = 0;
rIndex = 0;
cIndex = 0;

void setup() {
    Serial.begin(9600);
    Serial.println("<Arduino is ready>");
}

void loop() {
    if (reading == True) {
        recvBytesWithEndMarkers();
        showNewData();
    }
    if (driving == True) {
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
   
    while (Serial.available() > 0 && newData == false) {
        rb = Serial.read();
        Serial.println(rb, HEX);
        Serial.println(rb, BIN);

        // the byte is a direction byte
        if (rb == stepUpMark || rb == stepEvenMark || rb == stepDownMark) {
            direction[directionIndex] = rb - 'e';
            directionIndex++;
            if (directionIndex >= numBytes) {
                directionIndex = numBytes - 1;
            }
        }

        else if (rb == endRMark) {

            // do in need to do this now that it isnt a byte array, but an int array
            time[delayIndex] = '\0';
            direction[directionIndex] = '\0';
            delayTimeR = time;
            stepDirectionR = direction;

            time.cleararray
            direction.cleararray
            timeIndex = 0
            directionIndex = 0
        }

        else if (rb = endCMark) {

            time[delayIndex] = '\0';
            direction[directionIndex] = '\0';
            delayTimeC = time;
            stepDirectionC = direction;

            time.cleararray
            direction.cleararray
            timeIndex = 0
            directionIndex = 0
        }

        // the byte is the endMark
        else if (rb == endMark) {
            reading = False;
            driving = True;
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
    if (newData == true) {
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
        newData = false;
    }
}

void driveMotors() {
    cuurentTime = millis();
    if (currentTime - previousTime > delayTimeR[rIndex]){
        // step the motors in the direction of stepDirectionR[rIndex]
        rIndex++;
    }

}
