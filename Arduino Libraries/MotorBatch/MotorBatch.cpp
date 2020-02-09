#include "Arduino.h"
#include "MotorBatch.h"

MotorBatch::MotorBatch(int pulse, int direct, int limit, int CW, int CCW) {
	_pulsePin = pulse;
	_directionPin = direct;
	_limitPin = limit;
	pinMode(_pulsePin, OUTPUT);
	pinMode(_directionPin, OUTPUT);
	pinMode(_limitPin, INPUT);

	_ccwFlag = CCW;
	_cwFlag = CW;

	_state = 1;
	_statePrevious = 1;
	_timePyCounter = 0;


}

// forward is positive angle, so CCW
void MotorBatch::directionForward() {
	_direction = true;
	digitalWrite(_directionPin, _direction);
}

// this is clockwise
void MotorBatch::directionBackward() {
	_direction = false;
	digitalWrite(_directionPin, _direction);
}

void MotorBatch::directionChange(){
	_direction = !_direction;
	digitalWrite(_directionPin, _direction);
}

// should be a -1 or 1 coming in
void MotorBatch::setDirection(int incomingDir) {
	_direction = incomingDir*0.5 + 0.5;
}

void MotorBatch::setStep(int incomingStep) {
	_step = incomingStep;
}

int MotorBatch::getStep() {
	return _step;
}

void MotorBatch::pulse(){
	digitalWrite(_pulsePin, HIGH);
	digitalWrite(_pulsePin, LOW);
	_step += (2*_direction)-1;
}

void MotorBatch::setState(int incomingState) {
	_statePrevious = _state;
	_state = incomingState;
	// Serial.print("Setting state to ");
	// Serial.println(incomingState);
}

int MotorBatch::getState() {
	return _state;
}

int MotorBatch::getStatePrevious() {
	return _statePrevious;
}

void MotorBatch::revertState() {
	_state = _statePrevious;
}

int MotorBatch::getTimePyCounter() {
	return _timePyCounter;
}

void MotorBatch::incrementTimePyCounter() {
	_timePyCounter++;
}

int MotorBatch::getCCWFlag() {
	return _ccwFlag;
}

int MotorBatch::getCWFlag() {
	return _cwFlag;
}

int MotorBatch::getLimitPin(){
	return _limitPin;
}

void MotorBatch::setStartReceivingByte(byte incomingStartByte) {
	_startReceivingByte = incomingStartByte;
}

byte MotorBatch::getStartReceivingByte() {
	return _startReceivingByte;
}

void MotorBatch::showTimePy() {
	Serial.println("Showing the time array in the object");
	for (int i = 0; i < NUM_BYTES; i++) {
		Serial.print(timePy[i]);
		Serial.print(" ");
	}
}

void MotorBatch::showDirPy() {
	Serial.println("Showing the direction array in the object");
	for (int i = 0; i < NUM_BYTES; i++) {
		Serial.print(dirPy[i]);
		Serial.print(" ");
	}
}

void MotorBatch::setReceivedTime(int incomingTime) {
	_receivedTime = incomingTime;
}
void MotorBatch::setReceivedDir(int incomingDir) {
	_receivedDir = incomingDir;
}
int MotorBatch::getReceivedTime() {
	return _receivedTime;
}
int MotorBatch::getReceivedDir() {
	return _receivedDir;
}

int MotorBatch::getRelativeMoveCounter() {
	return _relativeMoveCounter;
}

void MotorBatch::setRelativeMoveCounter(int incomingCounter) {
	_relativeMoveCounter = incomingCounter;
}

void MotorBatch::decrementRelativeMoveCounter() {
	_relativeMoveCounter -= 1;
}