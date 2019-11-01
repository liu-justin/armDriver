#ifndef motor_h
#define motor_h

/*provides stepper motor control thru single steps*/

#include "Arduino.h"

class Motor {
	public:
		Motor(int a1, int a2, int b1, int b2);
		void forward(int delay);
		void backward(int delay);
		void setStep(int w);

	private:
		int _stepCounter = 0;
		int _a1;
		int _a2;
		int _b1;
		int _b2;
};

#endif