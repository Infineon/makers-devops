#include <Arduino.h>

void readSerialAndRespond() {
   String s("");

    do {
        s = Serial.readString();
    } while( s.indexOf("[@START_TEST@]") == -1 );

    Serial.println(s);
}