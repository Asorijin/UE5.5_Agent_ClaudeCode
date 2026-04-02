@echo off
set PROJECT="H:\UE\forlearn\forlearn.uproject"
set SCRIPT="H:\UE\forlearn\.claude\script\BlueprintGenerate.py"

"D:\UE_5.5\Engine\Binaries\Win64\UnrealEditor-Cmd.exe" %PROJECT% -run=pythonscript -script=%SCRIPT%