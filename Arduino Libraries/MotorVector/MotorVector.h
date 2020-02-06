#ifndef MotorVector_h
#define MotorVector_h

#include "Arduino.h"
#include "Motor.h"

#define VECTOR_INIT_CAPACITY 4

class MotorVector {
	public:
		MotorVector();
		int total();
		static void resize(int incomingcapacity);
		void add(Motor);
		Motor* get(int);
		void free();

	private:
	    Motor *_items;
	    int _capacity;
	    int _total;
}; // dont forget this semicolon, spent alot of time troubleshooting this

#endif