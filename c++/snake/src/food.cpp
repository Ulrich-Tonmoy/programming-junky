#include "food.hpp"

Food::Food(int cellCount) {
    Image image = LoadImage("assets/food.png");
    texture = LoadTextureFromImage(image);
    UnloadImage(image);
    position = GenerateRandomPosition(cellCount);
}

Food::~Food() {
    UnloadTexture(texture);
}

void Food::Draw(int cellSize) {
    DrawTexture(texture, position.x * cellSize, position.y * cellSize, WHITE);
}

Vector2 Food::GenerateRandomPosition(int cellCount) {
    float x = GetRandomValue(0, cellCount - 1);
    float y = GetRandomValue(0, cellCount - 1);
    return Vector2{x, y};
}