
#include "FPS.h"
#include <stdio.h>
#include <sys/timeb.h>
#include <iostream>
#include <unistd.h>

FPS::FPS(int setWaitTime)
{
    waitTime = setWaitTime;
    fps = 0;
    timeTaken = 0;
    lastTime = getTimeMM();
    nrFrames = 0;
    frameCount = 0;
}

FPS::~FPS() { }

int FPS::getTimeMM()
{
      struct timespec t;
      clock_gettime(CLOCK_MONOTONIC,  &t);
      return (t.tv_sec * 1000)+(t.tv_nsec*1e-6);
}

bool FPS::update()
{
    nrFrames++;
    frameCount++;
    int curTime = getTimeMM();
    if(curTime - lastTime > waitTime)
    {
   	timeTaken = (curTime - lastTime) / nrFrames;
        fps = nrFrames / double(curTime - lastTime) * 1000;
        nrFrames = 0;
        lastTime = curTime;
        return true;
    } else {
        return false;
    }
}

double FPS::getFPS()
{
    return fps;
}

double FPS::getTimeTaken()
{
    return timeTaken;
}

long FPS::getFrameCount()
{
     return frameCount;
}

std::string FPS::getString()
{
    std::string text = "FPS: " + std::to_string((int) fps);
    return text;
}
