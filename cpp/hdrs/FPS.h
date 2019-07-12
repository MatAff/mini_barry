#pragma once

#include <string>

class FPS
{
public:
    FPS(int setWaitTime);
    ~FPS();

    // Getters
    double getFPS();
    double getTimeTaken();
    long getFrameCount();
    std::string getString();

    // Update
    bool update();

private:
    int waitTime;
    int nrFrames;
    int lastTime;
    long frameCount;
    double fps;
    double timeTaken;
    int getTimeMM();
};

//static FPS gFps(1000); // TODO: find out why this was used for AVC
