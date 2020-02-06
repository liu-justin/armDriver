#ifndef MotorVector_h
#define MotorVector_h

#include "Arduino.h"

#define VECTOR_INIT_CAPACITY 4

class MotorVector {
	public:
		MotorVector();
		void add(Motor);
		void *get(int);
	private:
	    void **_items;
	    int _capacity;
	    int _total;
}

#endif