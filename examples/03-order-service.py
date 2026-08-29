"""订单服务模块 —— 隔离模式测试用例（仅供 /turbo 优化，不含答案）。

一个模拟的"大模块"：包含订单校验、库存、优惠、通知、报表等多个功能。
其中只有 `generate_daily_report` 是性能热点：对大量订单做 VIP 名单匹配时
用了 list 线性查找。该热点依赖模块级小函数 `_format_money`。

期望 /turbo 走「优化隔离」：
1. 把 generate_daily_report（连同依赖 _format_money 和所需 import）
   提取到 benchmark/order_service_fragment.py
2. 在片段副本上 建基线 → 优化 → 复测
3. 验证通过后回填原文件，不触碰其它函数

运行：python examples/03-order-service.py [订单数]
"""
import datetime
import random
import sys
import time

# ============ 配置 ============
VIP_LIST = [f"u{random.randint(1, 20000)}" for _ in range(2000)]
STOCK = {f"sku{i}": random.randint(0, 500) for i in range(500)}


# ============ 非热点功能 ============
def validate_order(order):
    """基础校验：用户、金额、地址。"""
    errors = []
    if not order.get("user"):
        errors.append("缺少用户")
    if order.get("amount", 0) <= 0:
        errors.append("金额非法")
    if not order.get("address"):
        errors.append("缺少地址")
    return errors


def compute_discount(amount, coupon_code):
    """根据优惠码算折后价。"""
    discounts = {"SAVE10": 0.90, "SAVE20": 0.80}
    code = coupon_code.upper().strip()
    return round(amount * discounts.get(code, 1.0), 2)


def check_stock(order, stock):
    """检查库存是否充足。"""
    sku = order.get("sku")
    if sku is None:
        return False
    return stock.get(sku, 0) >= order.get("qty", 1)


def reserve_stock(order, stock):
    """扣减库存。"""
    sku = order.get("sku")
    if sku in stock:
        stock[sku] = max(0, stock[sku] - order.get("qty", 1))


def send_notification(user, title, body):
    """模拟发送通知（此处只拼消息，不真发）。"""
    return f"[{title}] {user}: {body[:80]}"


def apply_tax(amount, region):
    """按区域加税。"""
    rates = {"CN": 0.13, "US": 0.07, "EU": 0.20, "OTHER": 0.0}
    return round(amount * (1 + rates.get(region, 0.0)), 2)


def cleanup_old_logs(logs, keep_days=30):
    """清理过期日志。"""
    now = 1724900000 + 86400 * keep_days
    return [log for log in logs if log[2] >= now - 86400 * keep_days]


def summarize_channels(orders):
    """按渠道聚合订单数。"""
    ch = {}
    for order in orders:
        c = order.get("channel", "web")
        ch[c] = ch.get(c, 0) + 1
    return ch


def render_receipt(order, user):
    """渲染订单回执文本。"""
    lines = [f"订单 {order['id']}", f"用户 {user}"]
    lines.append(f"金额 {order['amount']:.2f}")
    if order.get("coupon"):
        lines.append(f"优惠码 {order['coupon']}")
    return "\n".join(lines)


def get_user_tier(user, spend):
    """按累计消费返回用户等级。"""
    if spend >= 100000:
        return "金"
    if spend >= 50000:
        return "银"
    return "普通"


def cancel_order(order_id, orders):
    """取消未发货订单。"""
    for order in orders:
        if order["id"] == order_id and order["status"] == "pending":
            order["status"] = "cancelled"
            return True
    return False


def process_batch(batch, stock):
    """批量处理订单：校验、库存、通知。"""
    results = []
    for order in batch:
        errors = validate_order(order)
        if errors:
            results.append(("invalid", order["id"], errors))
            continue
        if not check_stock(order, stock):
            results.append(("out_of_stock", order["id"], []))
            continue
        reserve_stock(order, stock)
        send_notification(order["user"], "下单成功", f"金额 {order['amount']}")
        results.append(("ok", order["id"], []))
    return results


# ============ 热点：每日报表 ============
def _format_money(amount):
    """金额格式化（generate_daily_report 的直接依赖）。"""
    return f"{amount:.2f}"


def generate_daily_report(orders, vip):
    """生成当日订单报表（热点：数据量大时慢）。

    输入：orders 为 [(uid, amount, timestamp), ...]，vip 为名单 list。
    返回：(报表字符串, 各 VIP 用户订单数统计 dict)。
    """
    lines = ["日期,用户,VIP,金额"]
    stats = {}
    for uid, amount, ts in orders:
        date = datetime.date.fromtimestamp(ts)
        if uid in vip:                       # 热点：list 线性查找，整体 O(n·m)
            stats[uid] = stats.get(uid, 0) + 1
            lines.append(f"{date}|{uid}|VIP|{_format_money(amount)}")
        else:
            lines.append(f"{date}|{uid}||{_format_money(amount)}")
    return "\n".join(lines), stats


# ============ 入口 ============
def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 30000
    random.seed(42)
    orders = [
        (f"u{random.randint(1, 20000)}", round(random.uniform(10, 5000), 2),
         1724900000 + random.randint(0, 100000))
        for _ in range(n)
    ]
    t0 = time.perf_counter()
    report, stats = generate_daily_report(orders, VIP_LIST)
    t1 = time.perf_counter()
    print(f"订单数 {n} | 耗时 {t1 - t0:.3f}s | "
          f"报表行数 {len(report.splitlines())} | VIP订单数 {len(stats)}")


if __name__ == "__main__":
    main()
