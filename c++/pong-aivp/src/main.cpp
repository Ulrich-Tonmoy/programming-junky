#include "raylib.h"
#include "ball/ball.hpp"
#include "paddle/paddle.hpp"
#include "ai/ai.hpp"

int main() {
    Color Green = Color{38, 185, 154, 255};
    Color DarkGreen = Color{20, 160, 133, 255};
    Color LightGreen = Color{129, 204, 184, 255};
    Color Yellow = Color{243, 213, 91, 255};

    int player_score = 0;
    int ai_score = 0;
    const char* winText = nullptr;

    const int screen_width = 1280;
    const int screen_height = 720;

    InitWindow(screen_width, screen_height, "Pong");
    SetTargetFPS(60);

    Ball ball;
    ball.x = screen_width / 2;
    ball.y = screen_height / 2;
    ball.speedX = 330;
    ball.speedY = 330;
    ball.radius = 10;
    ball.color = Yellow;

    AIPaddle leftPaddle;
    leftPaddle.width = 25;
    leftPaddle.height = 120;
    leftPaddle.x = 10;
    leftPaddle.y = screen_height / 2 - leftPaddle.height / 2;
    leftPaddle.speed = 500;
    leftPaddle.color = WHITE;

    Paddle rightPaddle;
    rightPaddle.width = 25;
    rightPaddle.height = 120;
    rightPaddle.x = screen_width - rightPaddle.width - 10;
    rightPaddle.y = screen_height / 2 - rightPaddle.height / 2;
    rightPaddle.speed = 500;
    rightPaddle.color = WHITE;

    while (WindowShouldClose() == false) {
        if (player_score >= 10) {
            winText = "Player Player Wins!";
        }
        if (ai_score >= 10) {
            winText = "AI Wins!";
        }

        if (winText && IsKeyPressed(KEY_SPACE)) {
            winText = nullptr;
            player_score = 0;
            ai_score = 0;
            ball.ResetBall();
        }

        BeginDrawing();

        ball.Update(&player_score, &ai_score);
        leftPaddle.Update(ball.y);
        rightPaddle.Update();
        DrawLine(screen_width / 2, 0, screen_width / 2, screen_height, WHITE);

        if (CheckCollisionCircleRec(Vector2{ball.x, ball.y}, ball.radius, rightPaddle.GetRect())) {
            ball.speedX *= -1.1;
        }
        if (CheckCollisionCircleRec(Vector2{ball.x, ball.y}, ball.radius, leftPaddle.GetRect())) {
            ball.speedX *= -1.1;
        }

        ClearBackground(DarkGreen);
        DrawRectangle(screen_width / 2, 0, screen_width / 2, screen_height, Green);
        DrawCircle(screen_width / 2, screen_height / 2, 150, LightGreen);
        if (winText) {
            int textWidth = MeasureText(winText, 60);
            DrawText(winText, GetScreenWidth() / 2 - textWidth / 2, GetScreenHeight() / 2, 60, RED);
        }
        if (!winText) {
            ball.Draw();
            leftPaddle.Draw();
            rightPaddle.Draw();
        }
        DrawText(TextFormat("%i", GetFPS()), 10, 10, 50, WHITE);
        DrawText(TextFormat("%i", ai_score), screen_width / 4 - 20, 20, 80, WHITE);
        DrawText(TextFormat("%i", player_score), 3 * screen_width / 4 - 20, 20, 80, WHITE);

        EndDrawing();
    }

    CloseWindow();
    return 0;
}