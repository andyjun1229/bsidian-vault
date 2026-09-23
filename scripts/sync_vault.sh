#!/bin/bash
# vault 双向同步脚本 —— 两台电脑共用（本机 + 家里 iMac）
# 逻辑：pull --rebase（自动解决已知冲突）→ 有改动就 commit → push（带重试）
# 用法：bash scripts/sync_vault.sh
# 放进 cron：每天自动执行，保证 GitHub 上始终是最新统一知识库

set -o pipefail
VAULT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$VAULT" || exit 1
MACHINE=$(scutil --get ComputerName 2>/dev/null || hostname)
CHANGED=0

echo "[$(date '+%F %T')] 同步开始 @ $MACHINE"

# 0. 先提交本地未暂存变更（必须在 pull 之前，否则 rebase 会被卡死）
git add -A 2>/dev/null
if ! git diff --cached --quiet; then
    git commit -m "同步@$MACHINE $(date '+%F %H:%M')" >/dev/null && echo "已提交本地改动"
fi

# 1. 拉取远端，rebase 到本地之上
if ! git pull --rebase origin main >/tmp/vault_sync_pull.log 2>&1; then
    # 2. 冲突自动处理：机器特定文件取本地，自动生成文件重新生成
    CONFLICTS=$(git diff --name-only --diff-filter=U)
    if [ -n "$CONFLICTS" ]; then
        echo "冲突文件: $CONFLICTS"
        for f in $CONFLICTS; do
            case "$f" in
                outputs/__catalog.md)
                    git checkout --ours "$f" 2>/dev/null || git checkout --theirs "$f";;
                .obsidian/*)
                    git checkout --ours "$f";;   # Obsidian 配置各机器保留自己的
                *)
                    git checkout --ours "$f";;   # 笔记内容默认保留本地版本
            esac
            git add "$f"
        done
        GIT_EDITOR=true git rebase --continue >/dev/null 2>&1 || {
            echo "rebase 无法自动完成，请手动处理"; exit 1; }
        echo "冲突已自动解决"
    fi
fi

# 3. 本地有改动就提交
if ! git diff --quiet HEAD 2>/dev/null || [ -n "$(git status -s)" ]; then
    git add -A
    if ! git diff --cached --quiet; then
        git commit -m "同步@$MACHINE $(date '+%F %H:%M')" >/dev/null && CHANGED=1
        echo "已提交本地改动"
    fi
fi

# 4. 推送（网络不稳，重试 3 次）
PUSHED=0
for i in 1 2 3; do
    if git push origin main >/tmp/vault_sync_push.log 2>&1; then
        PUSHED=1; break
    fi
    sleep 5
done

# 5. 收尾：catalog 兜底重新生成（合并后可能过期）
python3 "$VAULT/scripts/gen_catalog.py" >/dev/null 2>&1
if ! git diff --quiet HEAD -- outputs/__catalog.md 2>/dev/null; then
    git add outputs/__catalog.md
    if ! git diff --cached --quiet; then
        git commit -m "目录更新@$MACHINE" >/dev/null 2>&1
        git push origin main >/dev/null 2>&1
    fi
fi

if [ $PUSHED -eq 1 ]; then
    echo "[$(date '+%F %T')] 同步完成：推送成功"
else
    echo "[$(date '+%F %T')] 推送失败（网络问题），本地已提交，下次重试"
    exit 1
fi
