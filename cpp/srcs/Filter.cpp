
#include "Filter.h"
#include <vector>

Filter::Filter(cv::Scalar lower, cv::Scalar upper) 
{
    this->lower = lower;
    this->upper = upper;
}

Filter::~Filter() {}

cv::Mat Filter::getMask() 
{
    return maskFrame;
}

cv::Mat Filter::getMasked()
{
    return maskedFrame;
}

void Filter::apply(const cv::Mat& frame)
{
    cv::cvtColor(frame, hsvFrame, cv::COLOR_BGR2HSV); // convert to hsv
    inRange(hsvFrame, lower, upper, maskFrame); // apply limits
    maskedFrame = cv::Mat::zeros(cv::Size(640,480), CV_8UC3); // Clear masked frame
    frame.copyTo(maskedFrame, maskFrame); // create masked frame
}

double Filter::getBlockPos(int height, int stroke)
{
    int top = int(height - stroke / 2.0);
    int bottom = int(height + stroke / 2.0);
    int nrBlocks = 21;
    double blockWidth = (double) maskFrame.cols / (double) nrBlocks;
    
    int maxBlock = 10; // if all counts are zero the middle direction is selected
    int maxCount = 10;
    
    //std::vector<int> blockCounts;
    for(size_t bNr=0; bNr < nrBlocks; ++bNr) 
    {
        int left = bNr * blockWidth;
        int right = (bNr + 1) * blockWidth;
        cv::Rect roi(left, top, int(blockWidth), stroke);
        cv::Mat block = maskFrame(roi); 
        int count = cv::sum(block)[0];
        if (count > maxCount) {
            maxCount = count;
            maxBlock = bNr;
        }
    }
    
    return (double) maxBlock / (nrBlocks - 1) * 2.0 - 1.0;
}
