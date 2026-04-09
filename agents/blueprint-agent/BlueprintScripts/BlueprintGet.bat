@echo off
set PROJECT="H:\UE\forlearn\forlearn.uproject"
set SCRIPT="H:\UE\forlearn\.claude\agents\blueprint-agent\BlueprintScripts\BlueprintStructureGet.py /Game/Characters/Mannequins/Animations/ABP_Manny.ABP_Manny"

"D:\UE_5.5\Engine\Binaries\Win64\UnrealEditor-Cmd.exe" %PROJECT% -run=pythonscript -script=%SCRIPT%