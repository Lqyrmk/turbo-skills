# turbo ⚡

一个语言无关的 Claude Code skill：**优化代码运行性能，同时保证代码可读、注释讲得清"为什么快"**。

> 仓库 `turbo-skills` 是技能集合的容器（遵循 `<name>-skills` 惯例），当前只含这一个 skill。skill 名为 `turbo`，手动触发 `/turbo`。

## 它做什么

- 测量驱动的工作流：明确目标 → 基线 → 定位瓶颈 → 最小修复 → 验证 → 复测 → 补注释 → 汇报
- 语言无关的优化手法目录（换数据结构、降低复杂度、缓存、批处理、移出循环…）
- 专门给优化过的代码写可读注释：**What / Why / When to revisit** 三要素
- 内置红线，阻止过早优化、微优化、用可读性换性能

## 安装

```bash
bash install.sh
```

把 `skills/turbo/` 复制到 `~/.claude/skills/turbo/`，之后所有项目可用。

> 若提示 `~/.claude/skills` 不存在，脚本会自动创建。卸载：删除 `~/.claude/skills/turbo/`。

## 使用

- **自动触发**：直接说"帮我把这段代码优化一下 / 让它更快"，turbo 会被自动拉起。
- **手动触发**：`/turbo`。

## 开发

见 [CLAUDE.md](CLAUDE.md)。核心就一个文件：`skills/turbo/SKILL.md`。
