import re
from datetime import date
from collections import defaultdict

ALIASES = {"NFLX": "Netflix", "NETFLIX": "Netflix", "NOTION": "Notion"}

def clean_merchant(raw: str) -> str:
    s = re.sub(r"^(SP|SQ|TST|PAYPAL|GOOGLE)\s*\*\s*", "", raw.upper())
    s = re.sub(r"\.COM|\bINC\b|\bLABS\b|[\d-]{3,}|\b[0-9A-F]{5,}\b", " ", s)
    key = s.split()[0] if s.split() else raw
    return next((v for k, v in ALIASES.items() if key.startswith(k)), key.title())

def detect_subscriptions(tx):
    groups = defaultdict(list)
    for d, m, amt in tx:
        groups[clean_merchant(m)].append((date.fromisoformat(d), amt))
    result = []
    for merchant, items in groups.items():
        items.sort()
        if len(items) < 3:
            continue
        gaps = [(b[0] - a[0]).days for a, b in zip(items, items[1:])]
        if not all(27 <= g <= 33 for g in gaps):
            continue
        hikes = [(a[1], b[1]) for a, b in zip(items, items[1:])
                 if b[1] > a[1] * 1.10]          # 相邻两次比，涨超 10% 记为涨价
        last_day, last_amt = items[-1]
        y, m = divmod(last_day.month, 12)        # 下个月同一天
        nxt = date(last_day.year + y, m + 1, min(last_day.day, 28))
        result.append({"merchant": merchant, "period": "monthly", "amount": last_amt,
                       "price_hikes": hikes, "next_charge": nxt.isoformat()})
    return result
