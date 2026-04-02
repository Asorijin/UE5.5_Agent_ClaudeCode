This subskill governs the dynamic configuration and execution of script\BlueprintGet.bat to inspect one or more Unreal Engine 5.5 Blueprint assets.

## Objective
Generate accurate structural metadata for each target Blueprint by:

1. Modifying BlueprintGet.bat to set the correct map context and Blueprint asset path, only map context and blueprint path, never change anything else

2. Executing the batch script to run the inspection Python tool

3. Repeating the process for every requested Blueprint

Input Requirements

- List of target Blueprints, each specified as a full asset path (e.g., /Game/Characters/BP_Player.BP_Player)

- desired map name for editor context (reject requirement if unspecified)

## Procedure

> every script must exist, if not, search them in \\.claude\script again

For each Blueprint in the input list:

1. Edit script\BlueprintGet.bat

Locate the line:

```bat
set SCRIPT="H:\UE\forlearn\.claude\script\BlueprintStructureGet.py MyDefaultMap /Game/Characters/BP_Player.BP_Player"
```
Replace only the two argument values inside the quotes with:

```bat
set SCRIPT="H:\UE\forlearn\.claude\script\BlueprintStructureGet.py <MAP_NAME> <FULL_BLUEPRINT_PATH>"
```

Attention:Perhaps this bat file had changed by forward operation, so the content in file maybe look like replaced, just check if content match your need, if not, change it as you need

Where:

<MAP_NAME> is either the user-provided map name or MyDefaultMap

<FULL_BLUEPRINT_PATH> is the current Blueprint’s full asset path (e.g., /Game/Blueprints/Door_BP.Door_BP)

2. Execute the batch script
Run:

```cmd
script\BlueprintGet.bat
```

Capture its output (typically written to a .json or .txt file, or printed to stdout).

3. Record the result

Associate the inspection output with the current Blueprint path for later reporting.

4. Proceed to next Blueprint (if any)

## Constraints

- Under no circumstances should BlueprintStructureGet.py be modified, edited, or replaced.

- Critical Restriction: Only the <MAP_NAME> and <FULL_BLUEPRINT_PATH> tokens inside the set SCRIPT=... line may be replaced. No formatting changes are permitted under any circumstance.

- Never assume default paths—always use the Blueprint path provided

- If multiple Blueprints are given, process them sequentially, not in parallel

- The Python script BlueprintStructureGet.py must accept exactly two arguments: <MapName> and <BlueprintPath>

- This subskill only handles script configuration and execution—it does not interpret the inspection results