
#include <string>
#include <opencv2/opencv.hpp>
#include <opencv2/highgui.hpp>

class Annotate
{
public:    
    Annotate();
    ~Annotate();
    
    static void addText(cv::Mat& frame, std::string text, int lineNr);    
};