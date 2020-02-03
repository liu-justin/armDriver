#include "Arduino.h"
#include "motorManager.h"

motorManager::motorManager(DM542_driver* R0, DM542_driver* RA) {
	_motorList


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

// should be a -1 or 1 coming in
void DM542_driver::setDirection(int incomingDir) {
	_direction = incomingDir*0.5 + 0.5;
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

void DM542_driver::showDirPy() {
	Serial.println("Showing the direction array in the object");
	for (int i = 0; i < NUM_BYTES; i++) {
		Serial.print(dirPy[i]);
		Serial.print(" ");
	}
}

int DM542_driver::getRelativeMoveCounter() {
	return _relativeMoveCounter;
}

void DM542_driver::setRelativeMoveCounter(int incomingCounter) {
	_relativeMoveCounter = incomingCounter;
}

void DM542_driver::decrementRelativeMoveCounter() {
	_relativeMoveCounter -= 1;
}