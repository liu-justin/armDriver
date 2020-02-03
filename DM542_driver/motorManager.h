#ifndef motorManager_h
#define motorManager_h

/*provides stepper DM542_driver control thru single steps*/

#include "Arduino.h"

class motorManager {
	public:
		motorManager(DM542_driver* R0, DM542_driver* RA);

		
	private:
		DM542_driver* _motorList[];
};

#endif