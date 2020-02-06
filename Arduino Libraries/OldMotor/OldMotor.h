#ifndef motor_h
#define motor_h

/*provides stepper motor control thru single steps*/

#include "Arduino.h"

const int numBytes = 128;

class Motor {
	public:
		Motor(int a1, int a2, int b1, int b2, int limit);

		int delayTime[numBytes];
		int stepDirection[numBytes];
		void forward1();
		void backward1();
		void step1(int direction);
		void stepAny(int input);
		void toStep(int step);
		void setStep(int w);
		void home();
		
		int getLimitPin();

		int _stepCounter = 0;
		int speed = 2; // rev/s
		
	private:
		
		int a1_pin;
		int a2_pin;
		int b1_pin;
		int b2_pin;
		int limit_pin;
		bool limit_tripped;
		

};

#endif