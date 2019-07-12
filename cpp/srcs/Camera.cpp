
#include "Camera.h"

Camera::Camera() 
{
    std::cout << "Getting camera" << std::endl;
    if (!cap.isOpened()) { throw std::runtime_error("ERROR: Unable to open the camera."); }
    cap.set(cv::CAP_PROP_FRAME_WIDTH, 640);
    cap.set(cv::CAP_PROP_FRAME_HEIGHT, 480);
}

Camera::~Camera() {}

void Camera::get(cv::Mat& frame) 
{
    cap >> frame;
    if (frame.empty()) {
        std::cerr << "ERROR: Unable to grab from the camera." << std::endl;
    }
}

