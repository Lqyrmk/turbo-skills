#!/usr/bin/env bash
# turbo 安装脚本：将 skills/turbo 复制到用户级 ~/.claude/skills/turbo
# 用法：bash install.sh
set -euo pipefail

SOURCE="$(cd "$(dirname "$0")" && pwd)/skills/turbo"
TARGET="${HOME}/.claude/skills/turbo"

if [ ! -d "$SOURCE" ]; then
  echo "错误：找不到 skill 源目录 $SOURCE" >&2
  exit 1
fi

mkdir -p "${HOME}/.claude/skills"
if [ -d "$TARGET" ]; then
  rm -rf "$TARGET"
fi
cp -r "$SOURCE" "$TARGET"

echo "✓ 已安装 turbo 到 $TARGET"
echo "  现在可以在任意项目用 /turbo 或直接说“帮我优化这段代码”触发。"
echo "  卸载：rm -rf $TARGET"
