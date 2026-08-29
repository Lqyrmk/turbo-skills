# turbo-skills ⚡

一个 Claude Code **插件**，包含两个 skill：

| skill | 命令 | 作用 |
|---|---|---|
| **turbo** | `/turbo` | 性能优化 + 可读注释（What / Why / Revisit 三段式） |
| **cost** | `/cost` | 性能算账：量化严重性 / 必要性 / 成本 |

## 它做什么

**turbo**
- 测量驱动的工作流：目标 → 基线 → 定位瓶颈 → 隔离 → 修复 → 自审 → 验证 → 复测 → 补注释 → 汇报
- 语言无关的优化手法目录；大文件热点走隔离模式，不原地改
- 内置红线与自审关卡，阻止过早优化、微优化、用可读性换性能

**cost**
- 严重性分级（🔴 严重 / 🟠 中等 / 🟢 轻微）
- 成本换算（每秒 CPU 占用、每日浪费、可感知程度）
- 必要性结论（必须现在优化 / 建议 / 可缓）

## 安装

```bash
bash install.sh
```

把插件装到 `~/.claude/skills/turbo-skills/`（skills-directory 插件，**重启 Claude Code 后自动加载**）。脚本会清理旧的单 skill 安装，避免 `/turbo` 命名冲突。

> 卸载：`rm -rf ~/.claude/skills/turbo-skills`

## 使用

- 先 `/turbo` 优化 → 需要量化收益时再 `/cost`。
- 两个 skill 也会在描述命中时自动触发（优化类 / 算账类）。

## 开发

见 [CLAUDE.md](CLAUDE.md)。两个 skill 各自独立维护。
