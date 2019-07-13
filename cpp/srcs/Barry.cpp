// General

// Open CV
#include <opencv2/opencv.hpp>
#include <opencv2/highgui.hpp>

// Robot classes
#include "Camera.h"
#include "FPS.h"
#include "Annotate.h"
#include "Filter.h"
#include "Twist.h"
#include "Tank.h"
//#include "Recorder.h"

#define KEY_ESC 27


// Exits program on detection of Ctrl+C (SIGINT)
//void ctrl_c_handler(int s){
//    std::cout << "Caught signal " << s << std::endl;
//}

// main program
int main(int argc,char ** argv)
{
//    signal(SIGINT, ctrl_c_handler);

    int SENSE_HEIGHT = 400;
    int SENSE_WIDTH = 10;

    Camera cam;
    FPS fps(1000);
    Twist twist(1.00, 0.00);
    Tank tank = Tank();

    Filter greenFilter = Filter(cv::Scalar(25, 30, 50), cv::Scalar(55, 255, 255));

    cv::Mat frame(cv::Size(640,480), CV_8UC3);
    bool running = true;

    // main loop
    while (running)
    {
        // sense
        frame = cv::Scalar(0,0,0);
        cam.get(frame);
        fps.update();
std::cout << fps.getString() << std::endl;

        // filter
        greenFilter.apply(frame);    
        cv::Mat maskedFrame = greenFilter.getMasked();
        double pos = greenFilter.getBlockPos(SENSE_HEIGHT, SENSE_WIDTH);
        
        // set twist
        double rotate = pos * -0.20;
        twist.setRotate(rotate);

        // annotate
        cv::Mat& dispFrame = maskedFrame;
        Annotate::addText(dispFrame, fps.getString(), 1);
        Annotate::addText(dispFrame, std::to_string(pos), 2);
        Annotate::addText(dispFrame, twist.toString(), 3);
       
        // drive
        int intSpeed = (int) twist.getForward() * 255;
        int intDirection = (int) twist.getRotate() * 255;
        tank.setSpeed(intSpeed);
        tank.setDirection(intDirection);
        twist.setForward(0.35);
       
        // show
        //imshow("Live", dispFrame);
        //int key = cv::waitKey(5);

        //if (key==KEY_ESC) {
        //    running = false;
        //}
   }

    return 0;
}
