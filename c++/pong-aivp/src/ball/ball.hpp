#pragma once

#include "raylib.h"

class Ball {
   public:
    float x, y;
    float speedX, speedY;
    int radius;
    Color color;

    void Draw();
    void Update(int* p_score, int* a_score);
    void ResetBall();
};