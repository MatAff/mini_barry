#include "Tank.h"
#include <iostream>

using namespace std;

Tank::Tank()
{
    Adafruit_MotorHAT hat;
    _speed = 0;
    _direction = 0;
    _sync();
}

Tank::~Tank() { }

void Tank::keyInput(int key)
{
	  if (key==82) { _speed = _speed + 25; }
	  if (key==84) { _speed = _speed - 25; }
	  if (key==81) { _direction = _direction - 1; }
	  if (key==83) { _direction = _direction + 1; }
	  cout << "Speed: " << _speed << endl;
	  cout << "Direction: " << _direction << endl;
	  _sync();
    _action();
}

void Tank::setSpeed(int speed)
{
    _speed = speed;
    _sync();
    _action();
}

void Tank::setDirection(int direction)
{
    _direction = direction;
    _sync();
    _action();
}

void Tank::stopAll()
{
    _speed = 0;
    _direction = 0;
    _sync();
    _action();
}

void Tank::_sync()
{
  	_rSpeed = _speed - (_direction + _dCorrect);
  	_lSpeed = _speed + (_direction + _dCorrect);

  	if (_rSpeed==0) {
	    	_rDirection = RELEASE;
	  } else {
		    if ((_rSpeed > 0) == _rCorrect) {
			      _rDirection = FORWARD;
		    } else {
			      _rSpeed = _rSpeed * -1;
			      _rDirection = BACKWARD;
		    }
		    _rSpeed = abs(_rSpeed);
	  }

	  if (_lSpeed==0) {
		    _lDirection = RELEASE;
	  } else {
		    if ((_lSpeed > 0) == _lCorrect) {
			      _lDirection = FORWARD;
		    } else {
			      _lDirection = BACKWARD;
		    }
		    _lSpeed = abs(_lSpeed);
	  }
}

void Tank::_action()
{
    rMotor.setSpeed(_rSpeed);
    lMotor.setSpeed(_lSpeed);
    rMotor.run(_rDirection);
    lMotor.run(_lDirection);
}

int Tank::getSpeed()
{
  	return _speed;
}

int Tank::getDirection()
{
  	return _direction;
}

int Tank::getRightSpeed()
{
  	return _rSpeed;
}

int Tank::getLeftSpeed()
{
  	return _lSpeed;
}

Direction Tank::getRightDirection()
{
  	return _rDirection;
}

Direction Tank::getLeftDirection()
{
	  return _lDirection;
}
