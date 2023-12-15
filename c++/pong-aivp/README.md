# Zig Compiler C++ Raylib Pong Game

A template set up for vs code for raylib Pong Game project with zig compiler.

## To run on windows

- [How to setup VS Code with Zig for CPP](../zig-cpp/)
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
│   └── main.cpp
├── build.bat
└── README.md
```

- Finally press `ctrl + F5` or `ctrl + fn + F5`(on laptop keyboard) to run the project
