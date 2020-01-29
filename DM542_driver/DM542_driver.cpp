#include "Arduino.h"
#include "DM542_driver.h"

DM542_driver::DM542_driver(int pulse, int direct, int limit, int CCW, int CW) {
	_pulsePin = pulse;
	_directionPin = direct;
	_limitPin = limit;
	pinMode(_pulsePin, OUTPUT);
	pinMode(_directionPin, OUTPUT);
	pinMode(_limitPin, INPUT);

	_ccwFlag = CCW;
	_cwFlag = CW;

	_state = 1;
	_timePyCounter = 0;

}

// forward is positive angle, so CCW
void DM542_driver::directionForward() {
	_direction = true;
	digitalWrite(_directionPin, _direction);
}

// this is clockwise
void DM542_driver::directionBackward() {
	_direction = false;
	digitalWrite(_directionPin, _direction);
}

void DM542_driver::directionChange(){
	_direction = !_direction;
	digitalWrite(_directionPin, _direction);
}

void DM542_driver::setStep(int incomingStep) {
	_step = incomingStep;
}

int DM542_driver::getStep() {
	return _step;
}

void DM542_driver::pulse(){
	digitalWrite(_pulsePin, HIGH);
	digitalWrite(_pulsePin, LOW);
	_step += (2*_direction)-1;
}

void DM542_driver::setState(int incomingState) {
	_state = incomingState;
	// Serial.print("Setting state to ");
	// Serial.println(incomingState);
}

int DM542_driver::getState() {
	return _state;
}

int DM542_driver::getTimePyCounter() {
	return _timePyCounter;
}

void DM542_driver::incrementTimePyCounter() {
	_timePyCounter++;
}

int DM542_driver::getCCWFlag() {
	return _ccwFlag;
}

int DM542_driver::getCWFlag() {
	return _cwFlag;
}

int DM542_driver::getLimitPin(){
	return _limitPin;
}

void DM542_driver::setStartReceivingByte(byte incomingStartByte) {
	_startReceivingByte = incomingStartByte;
}

byte DM542_driver::getStartReceivingByte() {
	return _startReceivingByte;
}

void DM542_driver::showTimePy() {
	Serial.println("Showing the time array in the object");
	for (int i = 0; i < NUM_BYTES; i++) {
		Serial.print(timePy[i]);
		Serial.print(" ");
	}
}