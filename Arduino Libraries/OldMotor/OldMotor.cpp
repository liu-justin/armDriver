#include "Arduino.h"
#include "Motor.h"

// array of tuples would work better but oh well
int seq [4][4] = {
  {1,0,1,0},
  {0,1,1,0},
  {0,1,0,1},
  {1,0,0,1}
};

Motor::Motor(int a1, int a2, int b1, int b2, int limit) {
	a1_pin = a1;
	a2_pin = a2;
	b1_pin = b1;
	b2_pin = b2;
	limit_pin = limit;
	limit_tripped = false;
	pinMode(a1_pin, OUTPUT);
	pinMode(a2_pin, OUTPUT);
	pinMode(b1_pin, OUTPUT);
	pinMode(b2_pin, OUTPUT);
	pinMode(limit, INPUT);
	

}

// forward is positive angle, so CCW
void Motor::forward1() {
	this->_stepCounter += 1;
    this->setStep(_stepCounter);
}

// this is clockwise
void Motor::backward1() {
	  this->_stepCounter -= 1;
    this->setStep(_stepCounter);
}

void Motor::step1(int direction) {
	//if (step == 1 or step == -1 or step == 0) {
	if (direction <= 1 and direction >= -1) {
		_stepCounter += direction;
		this->setStep(this->_stepCounter);
	}
}

void Motor::stepAny(int input) {
	int direction = input/abs(input);
	for (int i=0; i<abs(input); i++) {
		this->step1(direction);
	}
}

void Motor::toStep(int step) {
	int distance = step - this->_stepCounter;
	for (int i=0; i<abs(distance); i++) {
		this->step1(distance/abs(distance));
	}
	//while(step != _stepCounter) {
	//	this->step1((step < 0) - (step > 0));
	//}
}

void Motor::setStep(int w){
	digitalWrite(a1_pin, seq[w%4][0]);
	digitalWrite(a2_pin, seq[w%4][1]);
	digitalWrite(b1_pin, seq[w%4][2]);
	digitalWrite(b2_pin, seq[w%4][3]);
}

int Motor::getLimitPin(){
	return limit_pin;
}


/*void Motor::home(){
	unsigned long previousTime = millis();
	limit_tripped = Serial.read(limit_pin);
	while(!this->limit_pin) {
		unsigned long currentTime = millis();
		if(currentTime - previousTime > 5){
			// move slowly, maybe 1 rev/sec --> 200steps/sec --> 5ms/step
			this->backward1();
			previousTime = currentTime;
		}
	}
}*/
