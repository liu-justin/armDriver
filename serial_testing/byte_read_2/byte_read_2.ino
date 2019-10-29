
// Example 6 - Receiving binary data

const byte numBytes = 64;
int delayTimeR[numBytes];
int stepDirectionR[numBytes];
int delayTimeC[numBytes];
int stepDirectionC[numBytes];
byte numReceived = 0;

boolean newData = false;
boolean driving = false;

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
    byte stepUpMark = 0x7B;   // {
    byte stepEvenMark = 0x7C; // |
    byte stepDownMark = 0x7D; // }
    byte endMark = 0x65;      // e,101
    byte motorRMark = 0x66;   // f,102
    byte motorCMark = 0x67;   // g,103

    byte rb;
   

    while (Serial.available() > 0 && newData == false) {
        rb = Serial.read();
        Serial.println(rb, HEX);
        Serial.println(rb, BIN);

        if (rb == stepUpMark || rb == stepEvenMark || rb == stepDownMark) {
            stepDirectionR[directionIndex] = rb - 'e';
            directionIndex++;
            if (directionIndex >= numBytes) {
                directionIndex = numBytes - 1;
            }
        }

        else if (rb == endMark) {
            delayTimeR[delayIndex] = '\0';
            stepDirectionR[directionIndex] = '\0';
            numReceived = directionIndex;
            delayIndex = 0;
            directionIndex = 0;
            newData = true;
        }

        else {        
            delayTimeR[delayIndex] = rb;
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
