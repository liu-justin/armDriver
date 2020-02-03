#ifndef motorManager_h
#define motorManager_h

/*provides stepper Motor control thru single steps*/

#include "Arduino.h"

class motorManager {
	public:
		motorManager(Motor* R0, Motor* RA);

		
	private:
		Motor* _smotorList[];
};

#endif