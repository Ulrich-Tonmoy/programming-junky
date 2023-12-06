REM Build script for test
@ECHO OFF
SetLocal EnableDelayedExpansion

REM Get a list of all the .c files.
SET cFilenames=
FOR /R %%f in (*.cpp) do (
    SET cFilenames=!cFilenames! %%f
)

REM echo "Files:" %cFilenames%

REM Create the "bin" folder if it doesn't exist.
IF NOT EXIST "./bin" (
    mkdir "./bin"
)

SET assembly=main

ECHO "Building %assembly%%..."
zig c++ %cFilenames%  -o ./bin/%assembly%.exe