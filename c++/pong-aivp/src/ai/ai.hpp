#pragma once

#include "raylib.h"
#include "../paddle/paddle.hpp"

class AIPaddle : public Paddle {
   public:
    void Update(int ballY);
};