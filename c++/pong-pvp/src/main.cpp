#include "raylib.h"

struct Ball {
    float x, y;
    float speedX, speedY;
    float radius;

    void Draw() {
        DrawCircle(x, y, radius, WHITE);
    }
};

struct Paddle {
    float x, y;
    float speed;
    float width, height;

    Rectangle GetRect() {
        return Rectangle{x - width / 2, y - height / 2, width, height};
    }

    void Draw() {
        DrawRectangleRec(GetRect(), WHITE);
    }
};

int main(void) {
    InitWindow(1280, 720, "Pong");
    SetWindowState(FLAG_VSYNC_HINT);

    Ball ball;
    ball.x = GetScreenWidth() / 2.f;
    ball.y = GetScreenHeight() / 2.f;
    ball.radius = 5;
    ball.speedX = 300;
    ball.speedY = 300;

    Paddle leftPaddle;
    leftPaddle.x = 50;
    leftPaddle.y = GetScreenHeight() / 2;
    leftPaddle.width = 10;
    leftPaddle.height = 100;
    leftPaddle.speed = 500;

    Paddle rightPaddle;
    rightPaddle.x = GetScreenWidth() - 50;
    rightPaddle.y = GetScreenHeight() / 2;
    rightPaddle.width = 10;
    rightPaddle.height = 100;
    rightPaddle.speed = 500;

    const char* winText = nullptr;

    while (!WindowShouldClose()) {
        ball.x += ball.speedX * GetFrameTime();
        ball.y += ball.speedY * GetFrameTime();

        if (ball.y < 0) {
            ball.y = 0;
            ball.speedY *= -1;
        }
        if (ball.y > GetScreenHeight()) {
            ball.y = GetScreenHeight();
            ball.speedY *= -1;
        }

        // if (IsKeyDown(KEY_W) || IsKeyDown(KEY_UP)) {
        //     leftPaddle.y -= leftPaddle.speed * GetFrameTime();
        // }
        // if (IsKeyDown(KEY_S) || IsKeyDown(KEY_DOWN)) {
        //     leftPaddle.y = leftPaddle.speed * GetFrameTime();
        // }

        if (IsKeyDown(KEY_W)) {
            leftPaddle.y -= leftPaddle.speed * GetFrameTime();
        }
        if (IsKeyDown(KEY_S)) {
            leftPaddle.y += leftPaddle.speed * GetFrameTime();
        }

        if (IsKeyDown(KEY_UP)) {
            rightPaddle.y -= rightPaddle.speed * GetFrameTime();
        }
        if (IsKeyDown(KEY_DOWN)) {
            rightPaddle.y += rightPaddle.speed * GetFrameTime();
        }

        if (CheckCollisionCircleRec(Vector2{ball.x, ball.y}, ball.radius, leftPaddle.GetRect())) {
            if (ball.speedX < 0) {
                ball.speedX *= -1.1f;
                ball.speedY = (ball.y - leftPaddle.y) / (leftPaddle.height / 2) * -ball.speedX;
            }
        }
        if (CheckCollisionCircleRec(Vector2{ball.x, ball.y}, ball.radius, rightPaddle.GetRect())) {
            if (ball.speedX > 0) {
                ball.speedX *= -1.1f;
                ball.speedY = (ball.y - rightPaddle.y) / (rightPaddle.height / 2) * -ball.speedX;
            }
        }

        if (ball.x < 0) {
            winText = "Right Player Wins!";
        }
        if (ball.x > GetScreenWidth()) {
            winText = "Left Player Wins!";
        }

        if (winText && IsKeyPressed(KEY_SPACE)) {
            winText = nullptr;
            ball.x = GetScreenWidth() / 2.f;
            ball.y = GetScreenHeight() / 2.f;
            ball.speedX = 300;
            ball.speedY = 300;
        }

        BeginDrawing();

        ClearBackground(BLACK);
        DrawFPS(10, 10);

        if (winText) {
            int textWidth = MeasureText(winText, 60);
            DrawText(winText, GetScreenWidth() / 2 - textWidth / 2, GetScreenHeight() / 2, 60, RED);
        }
        if (!winText) {
            ball.Draw();
            leftPaddle.Draw();
            rightPaddle.Draw();
        }
        EndDrawing();
    }

    CloseWindow();

    return 0;
}