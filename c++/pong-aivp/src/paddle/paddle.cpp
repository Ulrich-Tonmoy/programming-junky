#include "paddle.hpp"

void Paddle::LimitMovement() {
    if (y <= 0) {
        y = 0;
    }
    if (y + height >= GetScreenHeight()) {
        y = GetScreenHeight() - height;
    }
}

Rectangle Paddle::GetRect() {
    return Rectangle{x, y, width, height};
}

void Paddle::Draw() {
    DrawRectangleRounded(GetRect(), 0.8, 0, color);
}

void Paddle::Update() {
    // if (IsKeyDown(KEY_W)) {
    // }
    // if (IsKeyDown(KEY_S)) {
    // }

    if (IsKeyDown(KEY_UP)) {
        y -= speed;
    }
    if (IsKeyDown(KEY_DOWN)) {
        y += speed;
    }

    Paddle::LimitMovement();
}