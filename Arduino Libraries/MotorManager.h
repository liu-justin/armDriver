#ifndef MotorManager_h
#define MotorManager_h

/*provides stepper Motor control thru single steps*/

#include "Arduino.h"
#include "Motor.h"

class motorManager {
	public:
		motorManager(Motor* R0, Motor* RA);

		void setAllStates(int incomingState);

		
	private:
		Motor* _motorList[2];
};

#endif