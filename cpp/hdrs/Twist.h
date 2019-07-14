
#include <string>

class Twist
{
public:
    Twist(double forward, double rotate);
    ~Twist();

    double getForward();
    double getRotate();
    
    void set(double forward, double rotate);
    void setForward(double forward);
    void setRotate(double rotate);
    
    std::string toString();
    
private:
    double forward;
    double rotate;
};


//class Twist(object):
//
//    def __init__(self, forward=0.0, rotate=0.0):
//        self.forward = forward
//        self.rotate = rotate
//
//    def to_string(self):
//        return 'Twist: %.2f %.2f' % (self.forward, self.rotate)
//
//    #def print(self):
//    #    print(self.to_string())
//
//    def set(self, forward=0.0, rotate=0.0):
//        self.forward = forward
//        self.rotate = rotate
//
//    def set_rotate(self, rotate):
//        self.rotate = rotate
//
//    def man(self, key):
//        if key == KEY_FORWARD : self.forward += 0.05
//        if key == KEY_BACKWARD : self.forward -= 0.05
//        if key == KEY_LEFT : self.rotate += 0.05
//        if key == KEY_RIGHT : self.rotate -= 0.05
//
//    def as_line(self):
//        S = (320, 340)
//        E = (int(320 - self.rotate * 100), 240)
//        return S, E
