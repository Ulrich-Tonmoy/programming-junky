#include "ai.hpp"

void AIPaddle::Update(int ballY) {
    if (y + height / 2 > ballY) {
        y -= speed * GetFrameTime();
    }
    if (y + height / 2 <= ballY) {
        y += speed * GetFrameTime();
    }

    Paddle::LimitMovement();
}