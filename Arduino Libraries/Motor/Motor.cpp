#include "Arduino.h"
#include "Motor.h"

Motor::Motor(int pulse, int direct, int limit, int CW, int CCW) {
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
void Motor::directionForward() {
	_direction = true;
	digitalWrite(_directionPin, _direction);
}

// this is clockwise
void Motor::directionBackward() {
	_direction = false;
	digitalWrite(_directionPin, _direction);
}

void Motor::directionChange(){
	_direction = !_direction;
	digitalWrite(_directionPin, _direction);
}

// should be a -1 or 1 coming in
void Motor::setDirection(int incomingDir) {
	_direction = incomingDir*0.5 + 0.5;
}

void Motor::setStep(int incomingStep) {
	_step = incomingStep;
}

int Motor::getStep() {
	return _step;
}

void Motor::pulse(){
	digitalWrite(_pulsePin, HIGH);
	digitalWrite(_pulsePin, LOW);
	_step += (2*_direction)-1;
}

void Motor::setState(int incomingState) {
	_statePrevious = _state;
	_state = incomingState;
	// Serial.print("Setting state to ");
	// Serial.println(incomingState);
}

int Motor::getState() {
	return _state;
}

int Motor::getStatePrevious() {
	return _statePrevious;
}

void Motor::revertState() {
	_state = _statePrevious;
}

int Motor::getTimePyCounter() {
	return _timePyCounter;
}

void Motor::incrementTimePyCounter() {
	_timePyCounter++;
}

int Motor::getCCWFlag() {
	return _ccwFlag;
}

int Motor::getCWFlag() {
	return _cwFlag;
}

int Motor::getLimitPin(){
	return _limitPin;
}

void Motor::setStartReceivingByte(byte incomingStartByte) {
	_startReceivingByte = incomingStartByte;
}

byte Motor::getStartReceivingByte() {
	return _startReceivingByte;
}

void Motor::showTimePy() {
	Serial.println("Showing the time array in the object");
	for (int i = 0; i < NUM_BYTES; i++) {
		Serial.print(timePy[i]);
		Serial.print(" ");
	}
}

void Motor::showDirPy() {
	Serial.println("Showing the direction array in the object");
	for (int i = 0; i < NUM_BYTES; i++) {
		Serial.print(dirPy[i]);
		Serial.print(" ");
	}
}

int Motor::getRelativeMoveCounter() {
	return _relativeMoveCounter;
}

void Motor::setRelativeMoveCounter(int incomingCounter) {
	_relativeMoveCounter = incomingCounter;
}

void Motor::decrementRelativeMoveCounter() {
	_relativeMoveCounter -= 1;
}