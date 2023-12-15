const std = @import("std");
const rl = @import("raylib.zig");

pub fn main() !void {
    rl.InitWindow(800, 450, "Raylib");

    while (!rl.WindowShouldClose()) {
        rl.BeginDrawing();
        rl.ClearBackground(rl.BLACK);
        rl.DrawText("Congrats! You created your first window!", 190, 200, 20, rl.WHITE);
        rl.EndDrawing();
    }
    rl.CloseWindow();
}
