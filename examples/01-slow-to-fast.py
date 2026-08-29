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


# ---- turbo 优化：换数据结构 + 三段式注释 ----
# What: 建 id → item 的哈希索引，供后续 O(1) 查询
# Why:  dict 查找是 O(1)，避免循环内对 list 的 O(n*m) 扫描，整体降到 O(n+m)
# Revisit: 若 items 和 ids 都很小，线性查找可能更快，可回退为朴素写法
def build_index_fast(ids, items):
    by_id = {it["id"]: it for it in items}
    return [by_id[i] for i in ids if i in by_id]
