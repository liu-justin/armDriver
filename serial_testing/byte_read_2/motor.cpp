class Motor {
	public:
		Motor(int a1, int a2, int b1, int b2);
		void forward(delay);
		void backward(delay);
		void setStep(w);

	private:
		int _stepCounter;
};

Motor::Motor() {
	this -> stepCounter = 0;
}

void Motor::forward(delay) {
	this->stepCounter += 1;
    this->setStep(Seq[self.stepCounter%4]);
}

void Motor::backward(delay) {
	this->stepCounter -= 1;
    this->setStep(Seq[self.stepCounter%4]);
}

void Motor::setStep(w){

}