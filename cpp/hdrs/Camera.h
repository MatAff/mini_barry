
#include <opencv2/opencv.hpp>
#include <opencv2/highgui.hpp>

class Camera
{
public:
    Camera();
    ~Camera();
    
    void get(cv::Mat& frame);
    
private:
    cv::VideoCapture cap = cv::VideoCapture(0);
};