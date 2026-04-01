# Claude Code for Unreal Engine 5.5

本项目为 Unreal Engine 5.5 开发配置了专用的 Claude Code 智能体系统，供了解UE引擎的开发人员使用，构建了简单的requirement-coding-rewiew-build-summary workflow。

## 智能体架构

### 根智能体路由规则

根据 `CLAUDE.md` 定义，用户请求会被自动路由到以下专用智能体：

- **codeAgent** - C++ 代码编辑任务
- **analyzeAgent** - 只读分析任务  
- **blueprintAgent** - 蓝图资产操作任务
- **reviewAgent** - 代码审查任务

### 1. codeAgent

**用途**: 修改现有的 UE5.5 C++ 类

**功能**:
- 验证目标类是否存在
- 安全更新 .h/.cpp 文件
- 应用 UE5.5 规范（UCLASS、UFUNCTION、UPROPERTY 等）
- 自动调用编译脚本 `quickComplie.bat`

**约束**:
- 仅修改已存在的类，不创建新类
- 最小化修改范围
- 编译前必须读取 `reflectionMacroCheck.md`

### 2. analyzeAgent

**用途**: 分析项目结构和代码组织

**功能**:
- 枚举 C++ 类、结构体、枚举
- 解析模块依赖（.Build.cs）
- 映射继承关系和蓝图暴露状态
- 生成结构化报告

**约束**:
- 只读操作，不修改文件
- 默认仅扫描 `Source/` 目录
- 不访问引擎源码或插件（除非明确指定）

### 3. blueprintAgent

**用途**: 检查和修改蓝图资产

**工作流程**:
1. 定位目标蓝图（Content/ 目录）
2. 使用外部脚本分析结构
3. 向用户确认分析结果
4. 获得批准后应用修改

**功能**:
- 通过 Python 脚本操作 .uasset 文件
- 添加变量、函数、事件图逻辑
- 修改暴露属性和默认值

**约束**:
- 必须经用户确认才能修改
- 仅操作 Content/ 下的资产
- 委托给外部脚本处理二进制文件

### 4. reviewAgent

**用途**: 代码审查（由其他智能体调用）

**审查范围**:
- 用户意图正确性
- UE5 C++ 语法和语义有效性
- 运行时安全性

**约束**:
- 不修改代码
- 不审查命名风格或格式
- 发现问题时返回用户决策

## 可用技能（Skills）

- **update-config** - 配置 settings.json
- **simplify** - 审查和优化代码质量
- **loop** - 定时执行命令
- **schedule** - 创建定时任务
- **claude-api** - 使用 Claude API 开发

## 辅助脚本

- `quickComplie.bat` - 快速编译脚本
- `BlueprintGet.bat` - 蓝图信息获取
- `BlueprintStructureGet.py` - 蓝图结构解析
- `BlueprintGenerate.py` - 蓝图生成/修改

---

*本配置遵循最小化原则，仅在必要时调用智能体，避免过度自动化。*

> TODO : 为编写蓝图脚本的subskill提供可查询的向量数据库，保证调用接口的正确性和接口相关开发效率；为codeAgent接入reviewAgent代码审查功能

> FUTURE : 实现在单个任务中的逐步骤记录，使思考连和调用链可追踪，对于大规模/长流程任务，实现原子级别的中断可恢复