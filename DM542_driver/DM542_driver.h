#ifndef DM542_driver_h
#define DM542_driver_h

/*provides stepper DM542_driver control thru single steps*/

#include "Arduino.h"

const int numBytes = 128;

class DM542_driver {
	public:
		DM542_driver(int pulse, int direct, int limit);
		int delayTime[numBytes];
		int stepDirection[numBytes];
		void directionForward();
		void directionBackward();
		void directionChange();
		void pulse();
		int pulseInt(int steps);
		void home();
		
		int getLimitPin();

		int _stepCounter = 1;
		int speed = 1; // rev/s
		long delayTimeTest;
		bool direction;
		
	private:
		
		int pulse_pin;
		int direction_pin;
		int limit_pin;
		bool limit_tripped;

		

};

#endif