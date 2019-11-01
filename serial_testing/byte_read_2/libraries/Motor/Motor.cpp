#include "Arduino.h"
#include "Motor.h"

// array of tuples would work better but oh well
int seq [4][4] = {
  {1,0,1,0},
  {0,1,1,0},
  {0,1,0,1},
  {1,0,0,1}
};

Motor::Motor(int a1, int a2, int b1, int b2) {
	_a1 = a1;
	_a2 = a2;
	_b1 = b1;
	_b2 = b2;
	pinMode(a1, OUTPUT);
	pinMode(a2, OUTPUT);
	pinMode(b1, OUTPUT);
	pinMode(b2, OUTPUT);
	

}

void Motor::forward(int delay) {
	this->_stepCounter += 1;
    this->setStep(seq[_stepCounter%4]);
}

void Motor::backward(int delay) {
	  this->_stepCounter -= 1;
    this->setStep(seq[_stepCounter%4]);
}

void Motor::setStep(int w){

}
