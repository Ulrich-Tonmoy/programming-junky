#include "ai.hpp"

void AIPaddle::Update(int ballY) {
    if (y + height / 2 > ballY) {
        y -= speed;
    }
    if (y + height / 2 <= ballY) {
        y += speed;
    }

    Paddle::LimitMovement();
}