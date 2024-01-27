#pragma once

#include "raylib.h"

class Food {
   public:
    Vector2 position = {5, 6};
    Texture2D texture;

    Food(int cellCount);
    ~Food();

    void Draw(int cellSize);
    Vector2 GenerateRandomPosition(int cellCount);
};
