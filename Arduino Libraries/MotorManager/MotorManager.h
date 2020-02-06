#ifndef MotorManager_h
#define MotorManager_h

/*provides stepper Motor control thru single steps*/

#include "Arduino.h"
#include "Motor.h"

const int MOTOR_COUNT = 2;

class MotorManager {
	public:
		//motorManager(Motor* R0, Motor* RA);
		MotorManager(...);
		Motor* getMotor(int index);

		void setAllStates(int incomingState);
		void setAllStatesBut(int incomingState, int index);
		void revertAllStates();
		void revertAllStatesBut(int index);

		bool checkStates(int incomingState);
		// need to change to different sizes when I use more motors
		
		
	private:
		// delcare the pointer to the first motor
		Motor *_motorList[MOTOR_COUNT];
		
};

#endif