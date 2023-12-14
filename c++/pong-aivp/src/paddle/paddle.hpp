#pragma once

#include "raylib.h"

class Paddle {
   protected:
    void LimitMovement();

   public:
    float x, y;
    float width, height;
    int speed;
    Color color;

    Rectangle GetRect();
    void Draw();
    void Update();
};