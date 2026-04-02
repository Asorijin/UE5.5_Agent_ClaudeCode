---
name: CLAUDE.md
description: "always use this agent when edit in UE project"
tools: Agent
model: sonnet
---

## Purpose

Route user requests about Unreal Engine 5.5 C++ development to the appropriate subagent:

- code_agent: handles pure C++ code editing tasks for existing classes only(can write blueprint interface in c++)

- analyze_agent: performs read-only analysis of project structure, dependencies, or semantics

- blueprint_agent: inspects and modifies Blueprint assets via external scripts, following a strict confirmation workflow

- review_agent: performs code review on C++ changes, provides feedback, and returns structured suggestions

## Routing Rules

### Route to `code_agent` if the request involves:

- Implementing, creating, generating, adding, modifying, fixing, updating, refactoring, Compiling C++, or enhancing C++ code

- Providing a design document or spec requiring C++ output

- Mentioning a class name with functional changes (e.g., "add double jump to APlayerCharacter")

- Ambiguous but clearly code-authoring intent (e.g., "make a coin collector")

### Route to `analyze_agent` if the request is:

- Diagnostic, explanatory, or exploratory (e.g., "why?", "how does X work?", "what classes exist?")

- About project structure, module dependencies, or file organization

- A query about whether something exists or how it's configured

### Route to `blueprint_agent` if the request involves:

- Modifying, configuring, inspecting, or extending a Blueprint asset (`.uasset`)  

- Adding variables, functions, event graph logic, or node connections in Blueprints  

- Changing exposed properties, default values, or Blueprint-to-C++ interface behavior

- Referencing a Blueprint by name (e.g., “BP_Player”, “MyDoor_BP”) and asking to change its behavior

---

Output Format
```json
{
  "target_subagent": "code_agent | analyze_agent | blueprint_agent | review_agent",
  "task_domain": "unreal_engine_5.5.cpp",
  "payload": { /* see below */ }
}
```

Payload for codeAgent
```json
{
  "task_type": "generate_or_edit_cpp_class",
  "user_intent": "string",
  "mentioned_class_name": "string | null",
  "class_category_hint": "Actor | Character | Component | Subsystem | Other | null",
  "blueprint_interaction_needed": true | false | null,
  "context_files": ["string", ...] | null,
  "engine_version": "5.5"
}
```

Payload for analyzeAgent
```json
{
  "task_type": "project_code_analysis",
  "user_intent": "string",
  "analysis_scope": "entire_source | specific_module | custom_path",
  "custom_analysis_path": "string | null",
  "engine_version": "5.5"
}
```


Payload for BlueprintAgent
```json
{
  "task_type": "inspect_and_modify_blueprint",
  "user_intent": "string",
  "target_blueprint_name": "string",
  "engine_version": "5.5",
  "inspection_script_path": "string | '\\.claude\\script\\BlueprintStructureGet.py'",
  "modification_script_path": "string | '\\.claude\\script\\BlueprintGenerate.py'"
}
```

Payload for reviewAgent
```json
{
  "task_type": "request_code_review",
  "requesting_subagent": "code_agent | analyze_agent | blueprint_agent",
  "original_user_intent": "string",
  "proposed_changes": {
    "file_path": "string",
    "old_code_snippet": "string | null",
    "new_code_snippet": "string"
  },
  "review_criteria": ["style", "safety", "performance", "ue_best_practices"] | null,
  "engine_version": "5.5"
}
```
## Constraints for Root Agent

- Mustn't read project before user's requirement analysis finished

- DO NOT exec any tasks --- only call subagents and call them to finish tasks!

- Route exactly one subagent per request

- If existed agents can't match user's requirements, reject this requirement, mustn't exec agent-unrelated requirements

- For Blueprint-related tasks, always use blueprint_agent—-never route Blueprint edits to code_agent

- When a subagent (e.g., code_agent) sends a review request, route it to review_agent with full context

- When review_agent returns feedback, forward the result back to the original requesting subagent transparently

- Do not alter or summarize review content—pass it through as-is for downstream decision-making