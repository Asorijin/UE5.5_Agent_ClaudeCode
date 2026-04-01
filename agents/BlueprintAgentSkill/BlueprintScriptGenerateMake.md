This document defines the internal procedure that the BlueprintAgent must follow during Step 4 (Apply Changes) of its workflow. It is not a standalone agent—it is a detailed action plan executed within the BlueprintAgent’s own logic.

Step 4.1: Analyze Operation Intent

Based on prior steps, determine which of the following applies:

A. Modify existing Blueprint
→ blueprint_info.found_in_content_dir == true
→ Use inspection_summary to understand current structure
→ Plan changes (e.g., “add float variable JumpPower”, “connect EventBeginPlay to PrintString”)

B. Create new Blueprint from C++ class
→ blueprint_info.found_in_content_dir == false
→ User intent must imply creation (e.g., “make BP based on AMyActor”)
→ Extract C++ class name from user_intent (e.g., AMyActor, MyCharacter)
→ Target path inferred from naming convention (e.g., /Game/Blueprints/BP_MyActor.BP_MyActor)

> If case B is detected but no valid C++ class can be extracted, set status = "error" and halt.

Step 4.2: Dynamically Generate script\BlueprintGenerate.py

every time call this workflow, write(if really need write a new one) a new, self-contained Python script to script\BlueprintGenerate.py with the following properties:

No external parameters: Since BlueprintGenerate.bat does not pass arguments, all data must be hard-coded into the .py file:

TARGET_BP_PATH: Full asset path (e.g., /Game/Characters/BP_Player.BP_Player)

PARENT_CPP_CLASS_NAME: Only if creating (e.g., "MyCharacter")

MAP_CONTEXT: Typically "MyDefaultMap" (used to load editor world)

Specific change instructions (e.g., variable names, default values, node connections)

Use only safe Unreal Editor Python API (unreal module):

For modification: unreal.load_object(None, path)

For creation: unreal.EditorAssetLibrary.create_asset(...) with BlueprintFactory

Always call unreal.BlueprintEditorLibrary.compile_blueprint(bp) at the end

Minimal logging:
```python
unreal.log("BlueprintGenerate: Starting...")
# ... work ...
unreal.log("BlueprintGenerate: Success.")
# OR
unreal.log_error("Failed to find parent class.")
```
Template logic:
```python
import unreal

TARGET_BP_PATH = "/Game/Blueprints/BP_Door.BP_Door"
PARENT_CPP_CLASS_NAME = "ADoorBase"   # None if modifying existing
MAP_CONTEXT = "MyDefaultMap"

unreal.log("BlueprintGenerate: Initializing...")

if unreal.EditorAssetLibrary.does_asset_exist(TARGET_BP_PATH):
    bp = unreal.load_object(None, TARGET_BP_PATH)
    # Apply modifications per user request
else:
    parent_class = unreal.find_class(PARENT_CPP_CLASS_NAME)
    if not parent_class:
        unreal.log_error(f"C++ class {PARENT_CPP_CLASS_NAME} not found!")
        exit(1)
    factory = unreal.BlueprintFactory()
    factory.parent_class = parent_class
    bp = unreal.EditorAssetLibrary.create_asset(
        asset_name="BP_Door",
        package_path="/Game/Blueprints",
        asset_class=unreal.Blueprint,
        factory=factory
    )
    # Optional: add initial nodes/variables
# ← Insert user-requested logic here (generated dynamically)
unreal.BlueprintEditorLibrary.compile_blueprint(bp)
unreal.log("BlueprintGenerate: Completed.")
```

If additional functionality is needed or certain features are unnecessary, they can be added or removed according to actual requirements.

The generated script must be deterministic, side-effect aware, and safe to run.

Step 4.3: Request Code Review from reviewAgent

Before executing, pause the BlueprintAgent workflow and BlueprintAgent should send a structured request to the main CLAUDE process to invoke reviewAgent:

```json
{
  "action": "request_review",
  "from_agent": "BlueprintAgent",
  "review_target": "BlueprintGenerate.py",
  "context": {
    "user_original_request": "<user_intent>",
    "operation_type": "modify_existing | create_from_cpp",
    "target_asset_path": "/Game/...",
    "cpp_parent_class": "MyCharacter (if applicable)"
  },
  "code_content": "<full content of script/BlueprintGenerate.py>",
  "expected_behavior": "Describe what the script should do in plain English"
}
```
Do not proceed until the main system returns review_result: approved

If review_result: rejected, return status: "error" with reviewer feedback

Step 4.4: Execute & Report (No Extra Confirmation)

Once review is approved:

1. Notify user:

Script reviewed and approved. Executing blueprint operation automatically...

2. Run:
```cmd
script\BlueprintGenerate.bat
```

3. Capture output and exit code

4. On success:

Set status: "success" (or "created_new" if newly created)

Return message:

Blueprint updated successfully at /Game/.... Ready to use in editor.

5. on failure:

Parse stderr/stdout for unreal.log_error(...) lines

Return detailed error, e.g.:

Execution failed:
C++ class 'MyCharacter' not registered — ensure it's compiled and visible to editor.
Set status: "error"
Important: Because the code has passed formal review, no additional user confirmation is required before execution.

## Constraints (Enforced by BlueprintAgent)

- Never execute BlueprintGenerate.py without prior review
- Never guess C++ class names—must be extractable from user intent
- All asset paths must reside under /Game/ (i.e., in Content/)
- Generated script must compile the Blueprint before exiting
- Logging must be minimal—only progress and errors