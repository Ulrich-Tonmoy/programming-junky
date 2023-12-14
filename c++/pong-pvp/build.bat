@ECHO OFF
SetLocal EnableDelayedExpansion

REM Get a list of all the .c files.
SET cppFilenames=
FOR /R %%f in (*.cpp) do (
    SET cppFilenames=!cppFilenames! %%f
)
REM Set the path to the Raylib library
SET RAYLIB_DIR=./lib/raylib

REM Create the "bin" folder if it doesn't exist.
IF NOT EXIST "./bin" (
    mkdir "./bin"
)

SET assembly=Pong

ECHO "Building %assembly%..."

@REM zig c++ %cppFilenames% -I%RAYLIB_DIR%/include -L%RAYLIB_DIR%/lib -lraylib -lmsvcrt -o ./bin/%assembly%.exe
zig c++ %cppFilenames% -I%RAYLIB_DIR%/include -L%RAYLIB_DIR%/lib -lraylibdll -lmsvcrt -o ./bin/%assembly%.exe
copy  "%RAYLIB_DIR%\lib\raylib.dll" "./bin/"
ECHO "Build complete."