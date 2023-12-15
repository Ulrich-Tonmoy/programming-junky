# Zig Raylib Intro

A template set up for vs code for raylib with zig.

## To run on windows

- [YouTube Video](https://youtu.be/BJYNPs_rCJg)

- Copy this folder link `https://github.com/Ulrich-Tonmoy/programming-junky/tree/main/zig/raylib-intro`.
- Download the folder with [download-directory](https://download-directory.github.io/) or [DownGit](https://minhaskamal.github.io/DownGit) and unzip it.
- Open the folder wth [vs code](https://code.visualstudio.com/download) and it will prompt you to install a extension so install it.
- Then press `ctrl + shift + p` to open the `Command Palette` then write `zig` will show some suggestion.
- First select `Zig Setup: Install Zig` to install zig compiler it will prompt version list select the latest.
- Then it will prompt you to install `ZLS` if doesn't then `Command Palette` search & select `Zig Language Server: Install Server` to install zls.
- Then again open Command Palette with `ctrl + shift + p` and search `>Open User Settings (JSON)` and it will open settings.json file.
- From settings. json copy the `zig.path` value like this or just use this default installation path `c:\\Users\\{User Name}\\AppData\\Roaming\\Code\\User\\globalStorage\\ziglang.vscode-zig\\zig_install,`
- Then add that to the environment path follow YouTube video to set a variable to path.
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

- Finally press `ctrl + shift + b` or in the terminal run the command `zig build run` to run the project
