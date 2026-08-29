# CLAUDE.md

这个项目是 **turbo-skills** —— 一个 Claude Code skill 的源码仓库，目前只包含一个 **turbo** skill。

## 命名约定

- **仓库名 `turbo-skills`**：技能集合的容器，遵循 `<name>-skills` 惯例（如 `agent-skills`）。将来加新 skill 不用改仓库名。
- **skill 名 `turbo`**：手动触发 `/turbo`。触发名由 `skills/<name>/` 目录名（装好后是 `~/.claude/skills/<name>/`）决定，frontmatter 的 `name` 需与之保持一致。
- 项目名与触发名**解耦**：仓库叫 `turbo-skills` 不影响 `/turbo` 的触发。

## 项目用途

turbo 是一个语言无关的性能优化 skill：在保证代码可读的前提下优化运行效率，并为每处"不再直观"的优化补充可读注释（What / Why / When to revisit）。

## 目录结构

```
turbo-skills/
├── CLAUDE.md              # 本项目文档（本文件）
├── README.md              # 对外说明 + 安装方法
├── install.sh             # 安装脚本：复制 skill 到用户级目录
├── skills/
│   └── turbo/
│       └── SKILL.md       # skill 本体（核心交付物）
└── examples/              # 演示与验证用示例
```

## 开发流程

1. 修改 `skills/turbo/SKILL.md`（唯一的逻辑核心）。
2. 改完用示例冒烟验证：`/turbo` 在任意项目触发，确认工作流和输出格式符合预期。
3. 安装到用户级：`bash install.sh`（复制到 `~/.claude/skills/turbo/`）。
4. commit 节奏：骨架 / 核心 / 文档 / 工具示例 分步提交，每个里程碑一个 commit。

## 设计约束

- **保持单文件（默认）**。SKILL.md 控制在 5–15KB，默认不引入 references 目录；仅在出现"大且可选"内容时按「体量纪律」拆分。
- **语言无关**。内容不得绑定具体编程语言；示例用伪代码或通用写法。
- **先做 skill，不做 plugin**。除非将来需要 hook / 多组件 / 分发，才考虑迁移成 plugin（届时 skill 挪入 `skills/` 即可，结构已兼容）。

## 体量纪律

turbo 是单文件设计，靠纪律防膨胀。**当前基线：SKILL.md 12.2KB**（硬线 15KB）。

### 加内容前的三问
1. 这段内容**每次优化都用得上**吗？
2. 会不会让某条规则变成**第三处重复**？
3. 是不是**大且可选**（大段、且不是每次都用）？

三问全过 → 加进 SKILL.md；任一不过 → 不加，或进 `references/`。

### 拆 references 的触发条件
出现"大且可选"的内容时（如各语言 profiler 速查表），才拆：
- 候选：自审清单 → `references/self-grill.md`、优化手法目录 → `references/techniques.md`。
- 拆法：SKILL.md 只留工作流核心，对应步骤改为引用 `references/<file>.md`。

### 15KB 硬线
- 超过 15KB → 二选一：**停止加内容**，或**立即拆 references**（拆时同步更新工作流对应步骤的引用）。

### 冗余纪律
- 同一规则最多出现**两处**（定义处 + 一处交叉引用）；出现第三处 → 合并成"定义处 + 其他位置引用它"。

## 验证

- SKILL.md frontmatter 必须含 `name: turbo` 和双语言 description（中英触发词）。
- 工作流必须覆盖 9 步：明确目标 → 基线 → 定位瓶颈 → 最小修复 → 自审 → 验证 → 复测 → 补注释 → 汇报（与 SKILL.md 保持同步）。
- 红线规则（过早优化 / 微优化 / 用可读性换性能 / 改行为换速度）必须保留。
