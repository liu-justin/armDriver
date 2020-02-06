#include <Motor.h>
#include <MotorManager.h>

Motor R0(2,3,4,42,103);
Motor RA(5,6,7,34,81);


// To use MotorVector, I would need to initialize the MotorVector first, then add them in; more work figuring the vector out than just modifying motorListLength
// if i could find a way to do mv.add(motor) in the Motor class, then it would be nice
//MotorVector mv();
//mv.add(R0);
//mv.add(RA);

// 

void setup() {
  
  Serial.begin(9600);
  
  //R0.setState(10);
  //Serial.println(R0.getState());
}
// have to do work on this, set this up for Motors instead of string
//  vector v;
//  vector_init(&v);
//  vector_add(&v, &R0);
//  vector_add(&v, &RA);
//  for (int i = 0; i < vector_total(&v); i++)
//    Serial.println(vector_get(&v, i).getState());


void loop() {
  // put your main code here, to run repeatedly:

}
