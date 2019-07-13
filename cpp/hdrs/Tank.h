#pragma once

#include "Adafruit_MotorHAT.h"

class Tank
{
public:
  Tank();
  ~Tank();

  void keyInput(int key);
  void setSpeed(int speed);
  void setDirection(int direction);
  void stopAll();

  int getSpeed();
  int getDirection();
  int getRightSpeed();
  int getLeftSpeed();

  Direction getRightDirection();
  Direction getLeftDirection();

  bool getRightCorrection();
  bool getLeftCorrection();
  int getDirCorrection();

private:
  Adafruit_MotorHAT hat;
  Adafruit_DCMotor rMotor = hat.getDC(1);
  Adafruit_DCMotor lMotor = hat.getDC(2);

  int _speed;
  int _direction;
  int _rSpeed;
  int _lSpeed;

  Direction _rDirection;
  Direction _lDirection;
  bool _rCorrect;
  bool _lCorrect;
  int _dCorrect;
  int _minSpeed;

  void _sync();
  void _action();
};
