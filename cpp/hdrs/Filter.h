
#include <opencv2/opencv.hpp>
#include <opencv2/highgui.hpp>

class Filter
{
public:
    Filter(cv::Scalar lower, cv::Scalar upper);
    ~Filter();
    
    cv::Mat getMask();
    cv::Mat getMasked();
    
    void apply(const cv::Mat& frame);
    double getBlockPos(int height, int stroke);
    // void key_handler(key);
    
    // ??? get_lines();
    
private:
    cv::Scalar lower;
    cv::Scalar upper; 
    cv::Mat hsvFrame;
    cv::Mat maskFrame;
    cv::Mat maskedFrame;
};
