#include "ball.hpp"

void Ball::Draw() {
    DrawCircle(x, y, radius, color);
}

void Ball::Update(int* p_score, int* a_score) {
    x += speedX;
    y += speedY;

    if (y + radius >= GetScreenHeight() || y - radius <= 0) {
        speedY *= -1;
    }
    if (x + radius >= GetScreenWidth()) {
        (*a_score)++;
        Ball::ResetBall();
    }
    if (x - radius <= 0) {
        (*p_score)++;
        Ball::ResetBall();
    }
}

void Ball::ResetBall() {
    x = GetScreenWidth() / 2;
    y = GetScreenHeight() / 2;

    speedX = 5;
    speedY = 5;

    int speed_choice[2] = {-1, 1};
    speedX *= speed_choice[GetRandomValue(0, 1)];
    speedY *= speed_choice[GetRandomValue(0, 1)];
}