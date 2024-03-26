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

SET assembly=window

ECHO "Building %assembly%%..."
"C:\\Program Files\\Microsoft Visual Studio\\2022\\Community\\VC\\Tools\\MSVC\\14.39.33519\\bin\\Hostx64\\x86\\cl.exe" %cFilenames% /Fo./bin/ user32.lib gdi32.lib /out:./bin/
ECHO "Build complete."