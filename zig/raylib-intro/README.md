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
- Copy this and paste in the explorer or open run and run this `%AppData%/Code/User/globalStorage/ziglang.vscode-zig/zig_install` and copy the `zig.exe` path.
- Then add that to the environment path follow YouTube video to set a variable to path.
- Andd Open vs code Settings json by `Ctrl+Shift+p` and `Open User Settings (JSON)` and add the copied path like` "zig.path": "C:\\Users\\Tonmoy\\AppData\\Roaming\\Code\\User\\globalStorage\\ziglang.vscode-zig\\zig_install\\zig.exe",`
- If you want updated raylib go to [Ryalib Repo](https://github.com/raysan5/raylib) click on latest commit and get the id from the link.
- Example: `https://github.com/raysan5/raylib/commit/55e83468c9bb515a5f2725751e5f187a7b9b5afd` here the id is `55e83468c9bb515a5f2725751e5f187a7b9b5afd`.
- And update the id in the `build.zig.zon` url `https://github.com/Not-Nik/raylib-zig/archive/new id should be here.tar.gz`

```
├── .vscode
├── src
│   ├── main.zig
│   └── raylib.zig
├── build.zig
├── build.zig.zon
└── README.md
```

- Finally press `ctrl + shift + b` or in the terminal run the command `zig build run` to run the project
