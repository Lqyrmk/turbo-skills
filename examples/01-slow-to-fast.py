"""示例：turbo 的工作方式。

左侧是"慢代码"，右侧是 turbo 风格优化 + 注释（What / Why / When to revisit）。
这是演示，不是规范；具体优化以 SKILL.md 为准。
"""

# ---- 慢：从一个大列表里反复查找 ----
# ids 和 items 都很大；下面在循环里对 list 做线性查找，整体 O(n*m)。
def build_index_slow(ids, items):
    index = []
    for i in ids:
        for it in items:
            if it["id"] == i:
                index.append(it)
                break
    return index


# ---- turbo 优化：换数据结构 + 注释 ----
# items 按 id 预建哈希索引，查询 O(1)，整体从 O(n*m) 降到 O(n+m)。
# When to revisit：如果 items 极小而 ids 极小时线性查找可能更快，但一般情况下哈希更优。
def build_index_fast(ids, items):
    by_id = {it["id"]: it for it in items}  # 一次 O(m) 建索引
    return [by_id[i] for i in ids if i in by_id]
