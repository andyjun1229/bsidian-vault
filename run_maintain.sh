#!/bin/bash
# 知识库每日维护 - 手动版
# 使用：cd /Users/mac/Documents/Obsidian\ Vault && bash run_maintain.sh

echo "==================================="
echo "📚 知识库每日维护 $(date '+%Y-%m-%d %H:%M')"
echo "==================================="

# Step 1: 检查新素材
echo ""
echo "🔍 [1/3] 检查 raw 新素材..."
python3 /Users/mac/Documents/Obsidian\ Vault/raw/_daily_maintain.py

# Step 2: 统计当前状态
echo ""
echo "📊 [2/3] 知识库状态..."
RAW_COUNT=$(ls /Users/mac/Documents/Obsidian\ Vault/raw/*.md 2>/dev/null | wc -l | tr -d ' ')
WIKI_COUNT=$(ls /Users/mac/Documents/Obsidian\ Vault/wiki/*.md 2>/dev/null | wc -l | tr -d ' ')
OUTPUT_COUNT=$(find /Users/mac/Documents/Obsidian\ Vault/outputs -name '*.md' 2>/dev/null | wc -l | tr -d ' ')
echo "  raw/    $RAW_COUNT 篇"
echo "  wiki/   $WIKI_COUNT 条"
echo "  outputs/ $OUTPUT_COUNT 份"

# Step 3: 检查近7天新增素材
echo ""
echo "📝 [3/3] 近7天新增素材..."
# macOS: 近7天 = -v-7d
SEVEN_DAYS_AGO=$(date -v-7d '+%Y-%m-%d' 2>/dev/null || date -d '7 days ago' '+%Y-%m-%d' 2>/dev/null)
find /Users/mac/Documents/Obsidian\\ Vault/raw -name '*.md' -newermt "$SEVEN_DAYS_AGO" 2>/dev/null | while read f; do
    basename "$f"
done | head -20

echo ""
echo "==================================="
echo "✅ 维护完成"
echo "💡 如需处理新增素材的概念提取，运行："
echo "    hermes"
echo "    然后说：处理 raw 中今天新增的素材，提取概念更新 wiki"
echo "==================================="
