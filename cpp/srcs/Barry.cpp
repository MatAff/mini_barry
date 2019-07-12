// General

// Open CV
#include <opencv2/opencv.hpp>
#include <opencv2/highgui.hpp>

// Robot classes
#include "Camera.h"
#include "FPS.h"
#include "Annotate.h"

//#include "Recorder.h"

#define KEY_ESC 27

// Exits program on detection of Ctrl+C (SIGINT)
//void ctrl_c_handler(int s){
//    std::cout << "Caught signal " << s << std::endl;
//}

Camera cam;
FPS fps = FPS(1000);

// Main program
int main(int argc,char ** argv)
{
//    signal(SIGINT, ctrl_c_handler);

    cv::Mat frame(cv::Size(640,480), CV_8UC3);
    bool running = true;

    // Main loop
    while (running)
    {
        // sense
        frame = cv::Scalar(0,0,0);
        cam.get(frame);
        fps.update();

        Annotate::addText(frame, fps.getString(), 1);
 
        imshow("Live", frame);

        int key = cv::waitKey(5);

        if (key==KEY_ESC) {
            running = false;
        }
   }

    return 0;
}
