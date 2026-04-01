@echo off
set PROJECT="H:\UE\forlearn\forlearn.uproject"
set SCRIPT="H:\UE\forlearn\.claude\script\BlueprintGenerate.py"

UnrealEditor-Cmd.exe %PROJECT% -run=pythonscript -script=%SCRIPT%