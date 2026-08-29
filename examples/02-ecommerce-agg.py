"""真实感测试用例：电商订单日志聚合（供 /turbo 优化，不含答案）。

模拟电商日志的每日聚合任务，默认 10 万条记录（可传参扩大）：
统计每个用户的订单数、总金额，并标记是否 VIP 用户。

刻意保留了 2 处常见热点（新手但真实的写法）：
1. VIP 名单用 list，循环内 `in` 是线性扫描（整体 O(n·m)）
2. 正则表达式在循环内反复编译

运行：
    python 02-ecommerce-agg.py            # 10 万条
    python 02-ecommerce-agg.py 300000     # 30 万条，更接近工业数据量
"""
import random
import re
import sys
import time

N = int(sys.argv[1]) if len(sys.argv) > 1 else 100_000
VIP_N = 2_000

random.seed(42)
logs = [
    f"{1724900000 + random.randint(0, 1000000)}|u{random.randint(1, 20000)}|"
    f"{random.choice(['view', 'buy', 'cart', 'refund'])}|{round(random.uniform(10, 5000), 2)}"
    for _ in range(N)
]
vip = [f"u{random.randint(1, 20000)}" for _ in range(VIP_N)]


def aggregate(logs, vip):
    """返回 (用户统计 dict, VIP 标记 dict)。"""
    stats = {}     # user -> [订单数, 总金额]
    is_vip = {}
    pat = re.compile(r"^u\d+$")
    for line in logs:
        _, user, action, amount = line.split("|")
        amount = float(amount)
        if user in vip:            # 热点1：list 线性查找，整体 O(n·m)
            is_vip[user] = True
        if pat.match(user):        # 热点2：每行重复编译正则
            cur = stats.get(user)
            if cur is None:
                stats[user] = [1, amount]
            else:
                cur[0] += 1
                cur[1] += amount
    return stats, is_vip


def main():
    t0 = time.perf_counter()
    stats, is_vip = aggregate(logs, vip)
    t1 = time.perf_counter()
    total_amount = round(sum(v[1] for v in stats.values()), 2)
    print(f"数据量 {N} 条 | 耗时 {t1 - t0:.3f}s | "
          f"用户数 {len(stats)} | VIP 数 {len(is_vip)} | 总金额 {total_amount}")


if __name__ == "__main__":
    main()
