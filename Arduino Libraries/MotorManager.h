#ifndef MotorManager_h
#define MotorManager_h

/*provides stepper Motor control thru single steps*/

#include "Arduino.h"
#include "Motor.h"

class MotorManager {
	public:
		//motorManager(Motor* R0, Motor* RA);
		MotorManager(int count, ...);

		void setAllStates(int incomingState);

		
	private:
		// delcare the pointer to the first motor
		Motor* _motorList;
};

#endif