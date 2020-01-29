#include "Arduino.h"
#include "DM542_driver.h"

DM542_driver::DM542_driver(int pulse, int direct, int limit) {
	pulse_pin = pulse;
	direction_pin = direct;
	limit_pin = limit;
	limit_tripped = false;
	pinMode(pulse_pin, OUTPUT);
	pinMode(direction_pin, OUTPUT);
	pinMode(limit_pin, INPUT);
	
	direction = false;
	digitalWrite(direction_pin, direction);

	delayTimeTest = 50; // milliseconds                             

}

// forward is positive angle, so CCW
void DM542_driver::directionForward() {
	direction = true;
	digitalWrite(direction_pin, direction);
}

// this is clockwise
void DM542_driver::directionBackward() {
	direction = false;
	digitalWrite(direction_pin, direction);
}

void DM542_driver::directionChange(){
	direction = !direction;
	digitalWrite(direction_pin, direction);
}

void DM542_driver::pulse(){
	digitalWrite(pulse_pin, HIGH);
	digitalWrite(pulse_pin, LOW);
	_stepCounter += (2*direction)-1; // direction is true/false (1,0)
}

int DM542_driver::pulseInt(int steps) {
	for (int i = 0; i < steps; i++) {
		this->pulse();
		delay(1);
	}
}

int DM542_driver::getLimitPin(){
	return limit_pin;
}

