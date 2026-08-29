# CLAUDE.md

这个项目是 **turbo-skills** —— 一个 Claude Code 插件仓库，包含两个 skill：**turbo**（性能优化）和 **cost**（性能算账）。

## 命名约定

- **仓库名 `turbo-skills`**：技能集合的容器，遵循 `<name>-skills` 惯例（如 `agent-skills`）。将来加新 skill 不用改仓库名。
- **skill 名**：`turbo` → `/turbo`，`cost` → `/cost`。触发名由 `skills/<name>/` 目录名决定，frontmatter 的 `name` 需与之保持一致；插件内无冲突时裸名直接可用。
- 项目名与触发名**解耦**：仓库叫 `turbo-skills` 不影响 `/turbo` 的触发。

## 项目用途

- **turbo**：语言无关的性能优化 skill，在保证代码可读的前提下优化运行效率，并为每处优化补充三段式注释（What / Why / Revisit）。
- **cost**：性能算账 skill，把性能数字换算成严重性 / 必要性 / 成本。

两者可衔接：`/turbo` 优化后，需要量化收益时用 `/cost`。

## 目录结构

```
turbo-skills/                  # 插件根
├── .claude-plugin/
│   └── plugin.json           # 插件清单（name/version/description）
├── skills/
│   ├── turbo/SKILL.md        # /turbo 性能优化
│   └── cost/SKILL.md         # /cost 性能算账
├── CLAUDE.md                 # 本项目文档（本文件）
├── README.md                 # 对外说明 + 安装方法
├── install.sh                # 安装为 skills-directory 插件
└── examples/                 # 演示与验证用示例
```

## 开发流程

1. 修改 `skills/turbo/SKILL.md`（唯一的逻辑核心）。
2. 改完用示例冒烟验证：`/turbo` 在任意项目触发，确认工作流和输出格式符合预期。
3. 安装为插件：`bash install.sh`（装到 `~/.claude/skills/turbo-skills/`，重启生效；也可 `claude --plugin-dir .` 临时加载调试）。
4. commit 节奏：骨架 / 核心 / 文档 / 工具示例 分步提交，每个里程碑一个 commit。

## 设计约束

- **保持单文件（默认）**。SKILL.md 控制在 5–15KB，默认不引入 references 目录；仅在出现"大且可选"内容时按「体量纪律」拆分。
- **语言无关**。内容不得绑定具体编程语言；示例用伪代码或通用写法。
- **已是插件**（多 skill 触发升级）。`.claude-plugin/plugin.json` 为清单，`skills/` 自动发现，无需在 manifest 里声明 skill。只有再加 hook / agent 等组件时才需扩展 manifest。

## 体量纪律

turbo 与 cost 各自单文件设计，靠纪律防膨胀。**当前基线：turbo/SKILL.md ~13.5KB、cost/SKILL.md ~2.2KB**（硬线各 15KB）。

### 加内容前的三问
1. 这段内容**每次优化都用得上**吗？
2. 会不会让某条规则变成**第三处重复**？
3. 是不是**大且可选**（大段、且不是每次都用）？

三问全过 → 加进 SKILL.md；任一不过 → 不加，或进 `references/`，或**拆成独立 skill**（内容足够独立时，如 cost）。

### 拆 references 或拆独立 skill 的触发条件
出现"大且可选"的内容时（如各语言 profiler 速查表），按内容独立性二选一：
- **拆 references**：内容属于某个 skill 的扩展细节 → `references/<file>.md`，SKILL.md 对应步骤改为引用它。
- **拆独立 skill**：内容足够独立、可单独命令调用（如算账 → `cost`）→ 新建 `skills/<name>/`。

### 15KB 硬线
- 超过 15KB → 三选一：**停止加内容** / **立即拆 references** / **拆成独立 skill**（拆时同步更新工作流对应步骤的引用）。

### 冗余纪律
- 同一规则最多出现**两处**（定义处 + 一处交叉引用）；出现第三处 → 合并成"定义处 + 其他位置引用它"。

## 验证

- 每个 SKILL.md frontmatter 必须含 `name`（turbo / cost）和双语言 description（中英触发词）。
- 工作流必须覆盖 9 步：明确目标 → 基线 → 定位瓶颈 → 最小修复 → 自审 → 验证 → 复测 → 补注释 → 汇报（与 SKILL.md 保持同步）。
- 红线规则（过早优化 / 微优化 / 用可读性换性能 / 改行为换速度）必须保留。
- 插件结构：`.claude-plugin/plugin.json` 存在，且 `claude plugin validate .` 通过。
