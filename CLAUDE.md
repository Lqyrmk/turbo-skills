# CLAUDE.md

这个项目是 **turbo** —— 一个 Claude Code skill 的源码仓库。

## 项目用途

turbo 是一个语言无关的性能优化 skill：在保证代码可读的前提下优化运行效率，并为每处"不再直观"的优化补充可读注释（What / Why / When to revisit）。

## 目录结构

```
turbo/
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

- **保持单文件**。SKILL.md 控制在 5–15KB，不引入 references 目录。复杂度靠精炼，不靠堆文件。
- **语言无关**。内容不得绑定具体编程语言；示例用伪代码或通用写法。
- **先做 skill，不做 plugin**。除非将来需要 hook / 多组件 / 分发，才考虑迁移成 plugin（届时 skill 挪入 `skills/` 即可，结构已兼容）。

## 验证

- SKILL.md frontmatter 必须含 `name: turbo` 和双语言 description（中英触发词）。
- 工作流必须覆盖：明确目标 → 基线 → 定位瓶颈 → 最小修复 → 验证 → 复测 → 补注释 → 汇报。
- 红线规则（过早优化 / 微优化 / 用可读性换性能 / 改行为换速度）必须保留。
