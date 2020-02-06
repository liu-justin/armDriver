#include "Arduino.h"
#include "MotorManager.h"
#include "Motor.h"
#include <stdio.h>
#include <stdarg.h>

// MotorManager::MotorManager(int count, ...) {
// 	va_list ap;

// 	va_start(ap, count);
// 	for (int i = 0; i < count; i++) {
// 		//_motorList[i] = va_arg(ap, Motor*);
// 		_motorList[i] = va_arg(ap, Motor*);
// 	}
// 	va_end(ap);
// }

MotorManager::MotorManager(...) {
	va_list ap;

	va_start(ap, MOTOR_COUNT);
	for (int i = 0; i < MOTOR_COUNT; i++) {
		//_motorList[i] = va_arg(ap, Motor*);
		_motorList[i] = va_arg(ap, Motor*);
	}
	va_end(ap);
}

// forward is positive angle, so CCW
Motor* MotorManager::getMotor(int index) {
	return _motorList[index];
}

void MotorManager::setAllStates(int incomingState) {
	for (int i = 0; i < MOTOR_COUNT; i++) {
		_motorList[i]->setState(incomingState);
	}
}

void MotorManager::setAllStatesBut(int incomingState, int index) {
	for (int i = 0; i < MOTOR_COUNT; i++) {
		if (i != index)
			_motorList[i]->setState(incomingState);
	}
}

void MotorManager::revertAllStates() {
	for (int i = 0; i < MOTOR_COUNT; i++) {
		_motorList[i]->revertState();
	}	
}

void MotorManager::revertAllStatesBut(int index) {
	for (int i = 0; i < MOTOR_COUNT; i++) {
		if(i != index)
			_motorList[i]->revertState();
	}	
}

bool MotorManager::checkStates(int incomingState) {
	for (int i = 0; i < MOTOR_COUNT; i++) {
		if (_motorList[i]->getState() != incomingState)
			return false;
	}
	return true;
}

// // this is clockwise
// void MotorManager::directionBackward() {
// 	_direction = false;
// 	digitalWrite(_directionPin, _direction);
// }

// void MotorManager::directionChange(){
// 	_direction = !_direction;
// 	digitalWrite(_directionPin, _direction);
// }

// // should be a -1 or 1 coming in
// void MotorManager::setDirection(int incomingDir) {
// 	_direction = incomingDir*0.5 + 0.5;
// }

// void MotorManager::setStep(int incomingStep) {
// 	_step = incomingStep;
// }

// int MotorManager::getStep() {
// 	return _step;
// }

// void MotorManager::pulse(){
// 	digitalWrite(_pulsePin, HIGH);
// 	digitalWrite(_pulsePin, LOW);
// 	_step += (2*_direction)-1;
// }

// void MotorManager::setState(int incomingState) {
// 	_state = incomingState;
// 	// Serial.print("Setting state to ");
// 	// Serial.println(incomingState);
// }

// int MotorManager::getState() {
// 	return _state;
// }

// int MotorManager::getTimePyCounter() {
// 	return _timePyCounter;
// }

// void MotorManager::incrementTimePyCounter() {
// 	_timePyCounter++;
// }

// int MotorManager::getCCWFlag() {
// 	return _ccwFlag;
// }

// int MotorManager::getCWFlag() {
// 	return _cwFlag;
// }

// int MotorManager::getLimitPin(){
// 	return _limitPin;
// }

// void MotorManager::setStartReceivingByte(byte incomingStartByte) {
// 	_startReceivingByte = incomingStartByte;
// }

// byte MotorManager::getStartReceivingByte() {
// 	return _startReceivingByte;
// }

// void MotorManager::showTimePy() {
// 	Serial.println("Showing the time array in the object");
// 	for (int i = 0; i < NUM_BYTES; i++) {
// 		Serial.print(timePy[i]);
// 		Serial.print(" ");
// 	}
// }

// void MotorManager::showDirPy() {
// 	Serial.println("Showing the direction array in the object");
// 	for (int i = 0; i < NUM_BYTES; i++) {
// 		Serial.print(dirPy[i]);
// 		Serial.print(" ");
// 	}
// }

// int MotorManager::getRelativeMoveCounter() {
// 	return _relativeMoveCounter;
// }

// void MotorManager::setRelativeMoveCounter(int incomingCounter) {
// 	_relativeMoveCounter = incomingCounter;
// }

// void MotorManager::decrementRelativeMoveCounter() {
// 	_relativeMoveCounter -= 1;
// }