#include <Motor.h>
#include <MotorManager.h>
#include <ros.h>
#include <v1_two_axis/BlindMotorCommand.h>
#include <v1_two_axis/LimitSwitch.h>

Motor R0(2,3,4);
Motor RA(5,6,7);
MotorManager mm(&R0, &RA);

ros::NodeHandle nh;

void blindMotorCommandCallback ( const v1_two_axis::BlindMotorCommand& command) {
  mm.getMotor(command.index)->setDirection(command.rotationDirection);
  mm.getMotor(command.index)->pulse();
}
ros::Subscriber<v1_two_axis::BlindMotorCommand> sub("topic_blind_motor_command", &blindMotorCommandCallback );

v1_two_axis::LimitSwitch limitSwitchMessage;
ros::Publisher pub("topic_limit_switch", &limitSwitchMessage );

void setup()
{
//  Serial.begin(57600);
  nh.initNode();
  nh.subscribe(sub);
  nh.advertise(pub);
}

void loop()
{
  for (int i = 0; i < MOTOR_COUNT; i++) {
    mm.getMotor(i)->pushLimitValue();
    if (mm.getMotor(i)->limitValueChanged()) {
//      Serial.print("Motor: ");
//      Serial.print(i);
//      Serial.print(" limitvalue: ");
//      Serial.println(mm.getMotor(i)->getCurrentLimitValue());
      limitSwitchMessage.motorIndex = i;
      limitSwitchMessage.tripped = mm.getMotor(i)->getCurrentLimitValue();
      pub.publish( &limitSwitchMessage );
    }
  }
  nh.spinOnce();
}
