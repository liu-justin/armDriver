#ifndef DM542_driver_h
#define DM542_driver_h

/*provides stepper DM542_driver control thru single steps*/

#include "Arduino.h"

const int NUM_BYTES = 64;

class DM542_driver {
	public:
		DM542_driver(int pulse, int direct, int limit, int CW, int CWW);
		int timePy[NUM_BYTES];

		void showTimePy();
		void showDirPy();

		int dirPy[NUM_BYTES];
		int getTimePyCounter();
		void incrementTimePyCounter();
		void setStartReceivingByte(byte incomingStartByte);
		byte getStartReceivingByte();

		void directionForward(); // CCW
		void directionBackward(); // CW
		void directionChange();

		void pulse();
		
		int getLimitPin();

		
		void setStep(int incomingStep);
		int getStep();
		
		
		void setState(int incomingState);
		int getState();

		int getCWFlag();
		int getCCWFlag();


		unsigned long previousTime;
		
	private:
		
		int _pulsePin;
		int _directionPin;
		int _limitPin;
		int _startReceivingByte;

		int _timePyCounter;
		bool _direction;
		int _step;
		int _state;
		int _ccwFlag;
		int _cwFlag;

};

#endif