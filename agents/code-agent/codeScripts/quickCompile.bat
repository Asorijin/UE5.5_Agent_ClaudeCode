cd ../../
@echo off
setlocal

set PROJECT_FILE=H:\UE\forlearn\forlearn.uproject
set PLATFORM=Win64
set CONFIGURATION=Development
set ENGINE_ROOT=D:\UE_5.5

for %%F in ("%PROJECT_FILE%") do set PROJECT_NAME=%%~nF

echo [Quick Build] %PROJECT_NAME% - %CONFIGURATION%^|%PLATFORM%
echo.

"%ENGINE_ROOT%\Engine\Binaries\DotNET\UnrealBuildTool\UnrealBuildTool.exe" ^
    %PROJECT_NAME% %CONFIGURATION% %PLATFORM% ^
    -Project="%PROJECT_FILE%" ^
    -TargetType=Editor ^
    -WaitMutex ^
    -progress

if errorlevel 1 (
    echo.
    echo  Build FAILED.
    pause
) else (
    echo.
    echo  Build SUCCEEDED.
)