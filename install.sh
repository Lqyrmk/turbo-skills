#!/usr/bin/env bash
# turbo-skills 安装脚本：把插件装为 skills-directory 插件（自动加载）。
# 用法：bash install.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
TARGET="${HOME}/.claude/skills/turbo-skills"

# 校验插件结构
if [ ! -f "${ROOT}/.claude-plugin/plugin.json" ]; then
  echo "错误：找不到插件清单 .claude-plugin/plugin.json" >&2
  exit 1
fi
if [ ! -d "${ROOT}/skills/turbo" ] || [ ! -d "${ROOT}/skills/cost" ]; then
  echo "错误：缺少 skills/turbo 或 skills/cost" >&2
  exit 1
fi

mkdir -p "${HOME}/.claude/skills"

# 清理旧的单 skill 安装，避免 /turbo 命名冲突
if [ -d "${HOME}/.claude/skills/turbo" ]; then
  rm -rf "${HOME}/.claude/skills/turbo"
  echo "  已移除旧的单 skill 安装 ~/.claude/skills/turbo"
fi
if [ -d "$TARGET" ]; then
  rm -rf "$TARGET"
fi

# 复制插件本体（.claude-plugin + skills）
mkdir -p "$TARGET"
cp -r "${ROOT}/.claude-plugin" "$TARGET/"
cp -r "${ROOT}/skills" "$TARGET/"

echo "✓ 已安装插件 turbo-skills 到 $TARGET"
echo "  重启 Claude Code 后生效：/turbo 优化、/cost 算账"
echo "  卸载：rm -rf $TARGET"
