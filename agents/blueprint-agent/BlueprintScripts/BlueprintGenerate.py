import unreal

# ── Hard-coded task data ──────────────────────────────────────────────────────

TARGET_BP_PATH = "/Game/Blueprints/BP_forlearnCharacter.BP_forlearnCharacter"

# Asset references to assign to CDO properties
IMC_DEFAULT_PATH = "/Game/ThirdPerson/Input/IMC_Default.IMC_Default"
IA_JUMP_PATH     = "/Game/ThirdPerson/Input/Actions/IA_Jump.IA_Jump"
IA_MOVE_PATH     = "/Game/ThirdPerson/Input/Actions/IA_Move.IA_Move"
IA_LOOK_PATH     = "/Game/ThirdPerson/Input/Actions/IA_Look.IA_Look"
IA_SHOOT_PATH    = "/Game/ThirdPerson/Input/Actions/IA_Shoot.IA_Shoot"
IA_AIM_PATH      = "/Game/ThirdPerson/Input/Actions/IA_Aim.IA_Aim"

# ── Main ──────────────────────────────────────────────────────────────────────

unreal.log("BlueprintGenerate: Starting CDO property assignment...")

# Step 1 – Load the Blueprint
if not unreal.EditorAssetLibrary.does_asset_exist(TARGET_BP_PATH):
    unreal.log_error(f"BlueprintGenerate: Blueprint not found at {TARGET_BP_PATH}!")
    raise SystemExit(1)

bp = unreal.load_asset(TARGET_BP_PATH)
if bp is None or not isinstance(bp, unreal.Blueprint):
    unreal.log_error(f"BlueprintGenerate: Failed to load Blueprint at {TARGET_BP_PATH}!")
    raise SystemExit(1)

unreal.log(f"BlueprintGenerate: Loaded {bp.get_name()}")

# Step 2 – Get the Blueprint's generated class (CDO container)
gen_class = bp.generated_class()
if gen_class is None:
    unreal.log_error("BlueprintGenerate: Blueprint has no generated_class!")
    raise SystemExit(1)

cdo = unreal.get_default_object(gen_class)
if cdo is None:
    unreal.log_error("BlueprintGenerate: Failed to get CDO!")
    raise SystemExit(1)

unreal.log(f"BlueprintGenerate: Got CDO of type {gen_class.get_name()}")

# Step 3 – Load all required assets
imc_default = unreal.load_asset(IMC_DEFAULT_PATH)
ia_jump     = unreal.load_asset(IA_JUMP_PATH)
ia_move     = unreal.load_asset(IA_MOVE_PATH)
ia_look     = unreal.load_asset(IA_LOOK_PATH)
ia_shoot    = unreal.load_asset(IA_SHOOT_PATH)
ia_aim      = unreal.load_asset(IA_AIM_PATH)

# Verify all assets loaded successfully
missing = []
if imc_default is None: missing.append(IMC_DEFAULT_PATH)
if ia_jump     is None: missing.append(IA_JUMP_PATH)
if ia_move     is None: missing.append(IA_MOVE_PATH)
if ia_look     is None: missing.append(IA_LOOK_PATH)
if ia_shoot    is None: missing.append(IA_SHOOT_PATH)
if ia_aim      is None: missing.append(IA_AIM_PATH)

if missing:
    for m in missing:
        unreal.log_error(f"BlueprintGenerate: Asset not found: {m}")
    raise SystemExit(1)

unreal.log("BlueprintGenerate: All referenced assets loaded.")

# Step 4 – Assign CDO properties inside a transaction
with unreal.ScopedEditorTransaction("Set BP_forlearnCharacter CDO input properties") as trans:
    cdo.set_editor_property("DefaultMappingContext", imc_default)
    cdo.set_editor_property("JumpAction",            ia_jump)
    cdo.set_editor_property("MoveAction",            ia_move)
    cdo.set_editor_property("LookAction",            ia_look)
    cdo.set_editor_property("ShootAction",           ia_shoot)
    cdo.set_editor_property("AimAction",             ia_aim)

unreal.log("BlueprintGenerate: CDO properties assigned.")

# Step 5 – Compile and save
unreal.BlueprintEditorLibrary.compile_blueprint(bp)
unreal.EditorAssetLibrary.save_asset(TARGET_BP_PATH)
unreal.log("BlueprintGenerate: Completed.")
