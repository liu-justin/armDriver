#ifndef MotorManager_h
#define MotorManager_h

/*provides stepper Motor control thru single steps*/

#include "Arduino.h"
#include "Motor.h"

const int MOTORLISTLENGTH = 2;

class MotorManager {
	public:
		//motorManager(Motor* R0, Motor* RA);
		MotorManager(int count, ...);
		Motor* getMotor(int index);

		void setAllStates(int incomingState);
		// need to change to different sizes when I use more motors
		
		
	private:
		// delcare the pointer to the first motor
		int _motorListLength = 2;
		Motor *_motorList[MOTORLISTLENGTH];
		
};

#endif