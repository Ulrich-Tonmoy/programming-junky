# Zig C++

A template set up for vs code for cpp project with zig compiler.

## To run on windows

- Copy this folder link `https://github.com/Ulrich-Tonmoy/programming-junky/tree/main/c%2B%2B/zig-cpp`.
- Download the folder with [download-directory](https://download-directory.github.io/) or [DownGit](https://minhaskamal.github.io/DownGit) and unzip it.
- Open the folder wth [vs code](https://code.visualstudio.com/download) and it will prompt you to install two extension so install them.
- Then press `ctrl + shift + p` to open the Command Palette then write `zig` will show some suggestion.
- First select `Zig Setup: Install Zig` to install zig compiler it will prompt version list select the latest.
- (optional) Then select `Zig Language Server: Install Server` to install zls.
- Then again open Command Palette with `ctrl + shift + p` and search `>Open User Settings (JSON)` and it will open settings.json file.
- From settings. json copy the `zig.path` value like this or just use this default installation path `c:\\Users\\Tonmoy\\AppData\\Roaming\\Code\\User\\globalStorage\\ziglang.vscode-zig\\zig_install,`
- Then add that to the environment path follow [this video](https://youtu.be/BJYNPs_rCJg) to set a variable to path.
- Finally press `ctrl + F5` or `ctrl + fn + F5`(on laptop keyboard) to run the project
