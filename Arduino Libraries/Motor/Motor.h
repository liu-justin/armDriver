#ifndef Motor_h
#define Motor_h

/*provides stepper Motor control thru single steps*/

#include "Arduino.h"

const int NUM_BYTES = 64;

class Motor {
	public:
		Motor(int pulse, int direct, int limit, int CW, int CCW);
		int timePy[NUM_BYTES];
		int dirPy[NUM_BYTES];
		void showTimePy();
		void showDirPy();
		
		void setReceivedTime(int incomingTime);
		void setReceivedDir(int incomingDir);
		int getReceivedTime();
		int getReceivedDir();
		
		int getTimePyCounter();
		void incrementTimePyCounter();
		void setStartReceivingByte(byte incomingStartByte);
		byte getStartReceivingByte();

		void directionForward(); // CCW
		void directionBackward(); // CW
		void directionChange();
		void setDirection(int incomingDir);

		void pulse();
		
		int getLimitPin();

		
		void setStep(int incomingStep);
		int getStep();
		
		
		void setState(int incomingState);
		int getState();
		int getStatePrevious();
		void revertState();

		int getCWFlag();
		int getCCWFlag();

		void decrementRelativeMoveCounter();
		int getRelativeMoveCounter();
		void setRelativeMoveCounter(int incomingCounter);



		unsigned long previousTime;
		int previousMajorStep;
		
	private:
		
		int _pulsePin;
		int _directionPin;
		int _limitPin;
		int _startReceivingByte;

		int _receivedTime;
		int _receivedDir;

		int _timePyCounter;
		int _relativeMoveCounter;
		bool _direction;
		int _step;
		int _state;
		int _statePrevious;
		int _ccwFlag;
		int _cwFlag;

};

#endif