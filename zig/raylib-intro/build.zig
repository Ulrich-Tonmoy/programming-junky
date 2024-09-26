const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    // For Raylib -------------------------------- Start
    const raylib_dep = b.dependency("raylib-zig", .{
        .target = target,
        .optimize = optimize,
    });
    const raylib = raylib_dep.module("raylib"); // main raylib module
    const raylib_artifact = raylib_dep.artifact("raylib"); // raylib C library
    // For Raylib -------------------------------- End

    const exe = b.addExecutable(.{
        .name = "raylib-intro",
        .root_source_file = b.path("src/main.zig"),
        .target = target,
        .optimize = optimize,
    });

    // For Raylib -------------------------------- Start
    exe.linkLibrary(raylib_artifact);
    exe.root_module.addImport("raylib", raylib);
    // For Raylib -------------------------------- End

    b.installArtifact(exe);

    const run_cmd = b.addRunArtifact(exe);

    run_cmd.step.dependOn(b.getInstallStep());

    if (b.args) |args| {
        run_cmd.addArgs(args);
    }

    const run_step = b.step("run", "Run the app");
    run_step.dependOn(&run_cmd.step);
}
