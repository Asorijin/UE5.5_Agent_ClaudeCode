@echo off
set PROJECT="H:\UE\forlearn\forlearn.uproject"
set SCRIPT="H:\UE\forlearn\.claude\script\BlueprintStructureGet.py MyDefaultMap /Game/Characters/BP_Player.BP_Player"

UnrealEditor-Cmd.exe %PROJECT% -run=pythonscript -script=%SCRIPT%