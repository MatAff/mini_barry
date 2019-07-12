
#include "Annotate.h"
    
Annotate::Annotate() {}
Annotate::~Annotate() {}
    
void Annotate::addText(cv::Mat& frame, std::string text, int lineNr)
{
    cv::putText(frame, text, cv::Point(10, lineNr * 20),
      cv::FONT_HERSHEY_SIMPLEX, 0.5, cv::Scalar(0,255,0), 1, 1);
}
//
//
//        font = cv2.FONT_HERSHEY_SIMPLEX
//        pos = (10, line_nr * 20)
//        frame = cv2.putText(frame, text, pos, font, 0.5, color, 1)
