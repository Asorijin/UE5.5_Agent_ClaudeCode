# Reflection Macro Checklist

all UE Object code must obey following rules:

## Class/Struct

- `UCLASS()` / `USTRUCT(BlueprintType)` / `UENUM(BlueprintType)` as needed.

- If Uclass maybe used in blueprint, use `UCLASS(Blueprintable)` instead, specially every `AActor`,`ACharactor`,`APawn` should use `UCLASS(Blueprintable)`

- `GENERATED_BODY()` present and correctly scoped.

## Properties
- Choose `EditDefaultsOnly` vs `EditAnywhere` deliberately.
- Add `BlueprintReadOnly` or `BlueprintReadWrite` intentionally.
- Add metadata (`ClampMin`, `AllowPrivateAccess`, etc.) only when justified.

## Functions
- Use `BlueprintCallable` for actions.
- Use `BlueprintPure` for read-only queries.
- Use explicit `Category` naming.

## Networking
- Mark RPC with `Server/Client/NetMulticast` and reliability intentionally.
- Add validation/authority checks in implementation path.