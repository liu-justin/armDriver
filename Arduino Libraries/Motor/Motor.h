#ifndef Motor_h
#define Motor_h

/*provides stepper Motor control thru single steps*/

#include "Arduino.h"

class Motor {
	public:
		Motor(int pulse, int direct, int limit, int CW, int CCW);
		
		void receiveTime(int incomingTime);
		void receiveDir(int incomingDir);
		void enqueTime(int incomingTime);
		void enqueDir(int incomingDir);
		void consumeTime();
		void consumeDir();
		int getTime();
		int getDir();

		void directionForward(); // CCW
		void directionBackward(); // CW
		void directionChange();
		void setDirection(int incomingDir);

		void pulse();
		
		int getLimitPin();

		void pushLimitValue(int incoming);
		bool checkLimitValues();
		void printLimitValues();

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
		
	private:
		
		int _pulsePin;
		int _directionPin;
		int _limitPin;

		int _time;
		int _timeNext;
		int _dir;
		int _dirNext;

		int _relativeMoveCounter;
		bool _direction;
		int _step;
		int _state;
		int _statePrevious;
		int _ccwFlag;
		int _cwFlag;

		int _limitValuesWritePointer = 0;
		static const int _limitValuesSize = 4;
		int _limitValues[_limitValuesSize] = {0,0,0,0};


};

#endif