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

// if it returns false, it hasn't been initialized
bool MotorManager::checkTimes() {
	for (int i = 0; i < MOTOR_COUNT; i++) {
		if (_motorList[i]->getTime() == -1)
			return false;
	} 
	return true;
}