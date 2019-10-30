

class Motor {
	public:
		Motor(int a1, int a2, int b1, int b2);
		void forward(int delay);
		void backward(int delay);
		void setStep(int w);

	private:
		int stepCounter;
};

// array of tuples would work better but oh well
int seq [4][4] = {
  {1,0,1,0},
  {0,1,1,0},
  {0,1,0,1},
  {1,0,0,1}
};

void Motor::forward(int delay) {
	this->stepCounter += 1;
    this->setStep(seq[stepCounter%4]);
}

void Motor::backward(int delay) {
	  this->stepCounter -= 1;
    this->setStep(seq[stepCounter%4]);
}

void Motor::setStep(int w){

}
