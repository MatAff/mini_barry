
#include "Twist.h"

Twist::Twist(double forward, double rotate) 
{
    this->forward = forward;
    this->rotate = rotate;
}

Twist::~Twist() {}

double Twist::getForward()
{
    return forward;
}

double Twist::getRotate()
{
    return rotate;
}
    
void Twist::set(double forward, double rotate)
{
    this->forward = forward;
    this->rotate = rotate;
}

void Twist::setForward(double forward)
{
    this->forward = forward;
}

void Twist::setRotate(double rotate)
{
    this->rotate = rotate;
}

std::string Twist::toString()
{
    std::string text = "Forward: " + std::to_string(forward) + "; " + "Rotate: " + std::to_string(rotate);
    return text;
}
    
