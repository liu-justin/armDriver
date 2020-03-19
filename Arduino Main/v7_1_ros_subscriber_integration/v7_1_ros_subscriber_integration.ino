#include <Motor.h>
#include <MotorManager.h>
#include <ros.h>
#include <v1_two_axis/BlindMotorCommand.h>
#include <v1_two_axis/LimitSwitch.h>

Motor R0(2,3,4,42,103);
Motor RA(5,6,7,34,81);

MotorManager mm(&R0, &RA);

ros::NodeHandle nh;

void messageCallback( const v1_two_axis::BlindMotorCommand& blind_msg) {
  mm.getMotor(blind_msg.index)->setDirection(blind_msg.direction);
  mm.getMotor(blind_msg.index)->pulse(); 
}

ros::Subscriber<v1_two_axis::BlindMotorCommand> sub("topic_blind_motor_command", &messageCallback);

v1_two_axis::LimitSwitch trip;
ros::Publisher pub("topic_limit_switch", &trip);

void setup() {
  Serial.begin(57600);
  
  nh.initNode();
  nh.subscribe(sub);
  nh.advertise(pub);
}

void loop() {
  for (int i = 0; i < MOTOR_COUNT; i++) {
//    Serial.print("motor index: ");
//    Serial.print(i);

    mm.getMotor(i)->pushLimitValue(digitalRead(mm.getMotor(i)->getLimitPin()));
//    Serial.print("; limit values stored: ");
//    mm.getMotor(i)->printLimitValues();

    if (mm.getMotor(i)->checkLimitValues()){
          Serial.print("motor index: ");
          Serial.println(i);
          trip.motorIndex = i;
          trip.tripped = mm.getMotor(i)->checkLimitValues();
          pub.publish(&trip);
    }
//    int currentLimitValue = digitalRead(mm.getMotor(i)->getLimitPin());
//    if (currentLimitValue != mm.getMotor(i)->getPreviousLimitValue()){
//      trip.motorIndex = i;
//      trip.tripped = bool(currentLimitValue);
//      mm.getMotor(i)->setPreviousLimitValue(currentLimitValue);
//      pub.publish(&trip);
//
//      Serial.print("motor index: ");
//      Serial.print(i);
//      Serial.println(digitalRead(currentLimitValue));
//    }
  }

  nh.spinOnce();
}
