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

int Motor::getCCWFlag() {
	return _ccwFlag;
}

int Motor::getCWFlag() {
	return _cwFlag;
}

int Motor::getLimitPin(){
	return _limitPin;
}



void Motor::receiveTime(int incomingTime) {
	_timeNext = incomingTime;
}
void Motor::receiveDir(int incomingDir) {
	_dirNext = incomingDir;
}
void Motor::enqueTime(int incomingTime) {
	_time = _timeNext;
	_timeNext = incomingTime;
}
void Motor::enqueDir(int incomingDir) {
	_dir = _dirNext;
	_dirNext = incomingDir;
}
void Motor::consumeTime() {
	_time = _timeNext;
}
void Motor::consumeDir() {
	_dir = _dirNext;
}

int Motor::getTime() {
	return _time;
}
int Motor::getDir() {
	return _dir;
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