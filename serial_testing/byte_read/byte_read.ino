
// Example 6 - Receiving binary data

const byte numBytes = 64;
byte delayTime[numBytes];
byte stepDirection[numBytes];
byte numReceived = 0;

boolean newData = false;

void setup() {
    Serial.begin(9600);
    Serial.println("<Arduino is ready>");
}

void loop() {
    recvBytesWithEndMarkers();
    showNewData();
}

void recvBytesWithEndMarkers() {
    static byte delayIndex = 0;
    static byte directionIndex = 0;
    byte stepUpMark = 0x65;
    byte stepEvenMark = 0x66;
    byte stepDownMark = 0x67;
    byte endMark = 0x68;
    byte rb;
   

    while (Serial.available() > 0 && newData == false) {
        rb = Serial.read();
        Serial.println(rb, HEX);
        Serial.println(rb, BIN);

        if (rb == stepUpMark || rb == stepEvenMark || rb == stepDownMark) {
            stepDirection[directionIndex] = rb - 'e';
            directionIndex++;
            if (directionIndex >= numBytes) {
                directionIndex = numBytes - 1;
            }
        }
        else if (rb == endMark) {
            delayTime[delayIndex] = '\0';
            stepDirection[directionIndex] = '\0';
            numReceived = directionIndex;
            delayIndex = 0;
            directionIndex = 0;
            newData = true;
        }

        else {        
            delayTime[delayIndex] = rb;
            delayIndex++;
            if (delayIndex >= numBytes) {
                delayIndex = numBytes - 1;
            }
        }
    }
}

void showNewData() {
    if (newData == true) {
        Serial.print("This just in (delay time)... ");
        for (byte n = 0; n < numReceived; n++) {
            Serial.print(delayTime[n], DEC);
            Serial.print(' ');
        }
        Serial.println();
        
        Serial.print("This just in (step direction)... ");
        for (byte n = 0; n < numReceived; n++) {
            Serial.print(stepDirection[n], HEX);
            Serial.print(' ');
        }
        Serial.println();
        newData = false;
    }
}
