REM Build script for test
@ECHO OFF
SetLocal EnableDelayedExpansion

REM Get a list of all the .c files.
SET cFilenames=
FOR /R %%f in (*.c) do (
    SET cFilenames=!cFilenames! %%f
)

REM Create the "bin" folder if it doesn't exist.
IF NOT EXIST "./bin" (
    mkdir "./bin"
)

SET assembly=server

ECHO "Building %assembly%%..."
zig cc %cFilenames% -lWs2_32 -o ./bin/%assembly%.exe
copy  "src\index.html" "./bin/"
ECHO "Build complete."