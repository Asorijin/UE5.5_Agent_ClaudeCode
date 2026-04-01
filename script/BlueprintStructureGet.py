import unreal
import json
import sys

def dump_blueprint_structure(asset_path):
    """
    读取指定蓝图资产的完整节点结构
    :param asset_path: 蓝图资产路径，如 '/Game/MyBP.MyBP'
    """
    # 加载蓝图资产
    blueprint = unreal.load_asset(asset_path)
    if not blueprint or not isinstance(blueprint, unreal.Blueprint):
        unreal.log_error(f"无效的蓝图资产: {asset_path}")
        return

    result = {
        "blueprint_name": blueprint.get_name(),
        "graphs": []
    }

    # 获取所有函数/事件图表
    for graph in blueprint.function_graphs + blueprint.macro_graphs:
        graph_info = {
            "graph_name": graph.get_graph_name(),
            "nodes": []
        }

        # 遍历所有节点
        for node in graph.get_nodes():
            node_info = {
                "node_name": node.get_node_title().strip(),
                "node_class": node.get_class().get_name(),
                "guid": str(node.node_guid),
                "position": [node.node_pos.x, node.node_pos.y],
                "pins": []
            }

            # 遍历所有引脚
            for pin in node.pins:
                pin_info = {
                    "pin_name": pin.pin_name,
                    "direction": "input" if pin.direction == unreal.EdGraphPinDirection.input else "output",
                    "linked_to": []
                }

                # 获取连接的目标引脚
                for linked_pin in pin.linked_to:
                    linked_info = {
                        "node_guid": str(linked_pin.get_outer().node_guid),
                        "pin_name": linked_pin.pin_name
                    }
                    pin_info["linked_to"].append(linked_info)

                node_info["pins"].append(pin_info)

            graph_info["nodes"].append(node_info)

        result["graphs"].append(graph_info)

    # 输出结果（可改为写入文件）
    unreal.log(f"=== 蓝图结构: {asset_path} ===")
    unreal.log(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    # 期望命令行格式: script.py <MapName> <BlueprintPath>
    if len(sys.argv) != 3:
        unreal.log_error("Usage: python script.py <MapName> <BlueprintPath>")
        unreal.log_error("Example: python dump.py MyDefaultMap /Game/YourBlueprint.YourBlueprint")
        sys.exit(1)

    map_name = sys.argv[1]
    blueprint_path = sys.argv[2]

    # 加载地图（使用你原注释中的格式）
    level_path = f"/Game/maps/{map_name}.{map_name}"
    unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).load_level(level_path)

    # 调用你原有的函数
    dump_blueprint_structure(blueprint_path)