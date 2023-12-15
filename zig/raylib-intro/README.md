# Zig Raylib Intro

A template set up for vs code for raylib with zig.

## To run on windows

- [How to setup VS Code with Zig for CPP](https://youtu.be/ddif7SZ1Vp0)
- Download the [raylib](https://github.com/raysan5/raylib/releases) release `raylib-5.0_win64_mingw-w64.zip`
- Unzip it and put in the `lib/raylib` folder the tree will be like bellow

```
├── .vscode
├── lib
│   ├── raylib
│   │   ├── include
│   │   │   ├── raylib.h
│   │   │   ├── raymath.h
│   │   │   └── rlgl.h
│   │   ├── lib
│   │   │   ├── libraylib.a
│   │   │   ├── libraylibdll.a
│   │   │   └── raylib.dll
├── src
│   ├── main.zig
│   └── raylib.zig
├── build.zig
├── build.zig.zon
└── README.md
```
