#include <iostream>
#include <raylib.h>

#include "food.hpp"

using namespace std;

Color Green = {173, 204, 96, 255};
Color DarkGreen = {43, 51, 24, 255};

int CellSize = 30;
int CellCount = 25;

int main() {
    InitWindow(CellSize * CellCount, CellSize * CellCount, "Retro Snake");
    Image icon = LoadImage("assets/icon.png");
    SetWindowIcon(icon);
    SetTargetFPS(60);

    Food food = Food(CellCount);

    while (WindowShouldClose() == false) {
        BeginDrawing();

        ClearBackground(Green);
        food.Draw(CellSize);

        EndDrawing();
    }

    CloseWindow();
    return 0;
}