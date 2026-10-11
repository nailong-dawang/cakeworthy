#!/usr/bin/env python3
"""
cakeworthy — overdue-invoice "cake milestone" tracker.

Inspired by the 2013 MetaBrainz story: after ~3 years of an unpaid $20,000
invoice (#144) from Amazon, they sent Amazon an "anniversary cake" celebrating
3 years of non-payment, posted a photo publicly — and the check was on its way
within 24 hours. A $30 cake beat six months of polite pestering.

cakeworthy doesn't nag. It just tells you which of your invoices have hit a
"cake milestone" (30/60/90/180/365/730 days overdue) and drafts a playful,
MetaBrainz-style public note for each one. What you do with the cake is up to you.

Usage:
    cakeworthy init                  # create a sample invoices.json
    cakeworthy check [--file F]       # list invoices that hit a milestone
    cakeworthy card <invoice-id>      # print the anniversary card + post drafts
"""

import argparse
import json
import sys
from datetime import date, datetime
from pathlib import Path

DEFAULT_FILE = Path("invoices.json")

# (days, english label, chinese label)
MILESTONES = [
    (30, "1 month", "满月"),
    (60, "2 months", "双月"),
    (90, "a quarter", "季度"),
    (180, "half a year", "半年"),
    (365, "1 year", "周年"),
    (730, "2 years", "两周年"),
    (1095, "3 years", "三周年"),
]


def days_overdue(due: str) -> int:
    try:
        due_date = datetime.strptime(due, "%Y-%m-%d").date()
    except ValueError:
        print(f"error: bad due date '{due}' (want YYYY-MM-DD)", file=sys.stderr)
        sys.exit(1)
    return (date.today() - due_date).days


def milestone_for(days: int):
    """Return the biggest milestone reached, or None."""
    hit = None
    for m in MILESTONES:
        if days >= m[0]:
            hit = m
    return hit


def load_invoices(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"error: {path} not found — run `cakeworthy init` first", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"error: {path} is not valid JSON: {e}", file=sys.stderr)
        sys.exit(1)


def cake_ascii(lines):
    width = max(len(l) for l in lines) + 4
    bar = "=" * (width + 2)
    candles = "   " + " ".join("i" for _ in range((width - 6) // 4 + 1))
    out = [candles, "  " + bar]
    for l in lines:
        out.append("  | " + l.center(width - 2) + " |")
    out += ["  " + bar, " " + "/" + "_" * (width) + "\\"]
    return "\n".join(out)


def cmd_init(path: Path):
    if path.exists():
        print(f"{path} already exists, leaving it alone")
        return
    sample = [
        {
            "id": "INV-2026-001",
            "client": "Acme Corp",
            "amount": 4800.00,
            "currency": "USD",
            "due": "2026-06-01",
            "service": "API integration work",
        },
        {
            "id": "INV-2026-002",
            "client": "Globex",
            "amount": 1200.00,
            "currency": "USD",
            "due": "2026-10-01",
            "service": "Consulting",
        },
    ]
    path.write_text(json.dumps(sample, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote sample {path} — edit it with your real invoices")


def cmd_check(path: Path):
    invoices = load_invoices(path)
    hits = []
    for inv in invoices:
        days = days_overdue(inv["due"])
        if days < 0:
            continue
        m = milestone_for(days)
        if m:
            hits.append((days, m, inv))
    if not hits:
        print("No cake milestones today. Enjoy the quiet. 🎂-less")
        return
    hits.sort(reverse=True)
    print(f"{len(hits)} invoice(s) are cake-worthy today:\n")
    for days, m, inv in hits:
        amount = f"{inv.get('currency', 'USD')} {inv['amount']:,.2f}"
        print(f"  🎂 {inv['id']} — {inv['client']} — {amount}")
        print(f"     {days} days overdue → {m[1]} anniversary ({m[2]})")
        print(f"     run: cakeworthy card {inv['id']}\n")


def cmd_card(path: Path, invoice_id: str):
    invoices = load_invoices(path)
    inv = next((i for i in invoices if i["id"] == invoice_id), None)
    if inv is None:
        print(f"error: no invoice '{invoice_id}' in {path}", file=sys.stderr)
        sys.exit(1)
    days = days_overdue(inv["due"])
    m = milestone_for(days)
    amount = f"{inv.get('currency', 'USD')} {inv['amount']:,.2f}"
    if m is None:
        print(f"{invoice_id} is {days} days overdue — not cake-worthy yet. Patience.")
        return

    label = f"{m[1].upper()} OF UNPAID INVOICE"
    print(cake_ascii([inv["id"], label, amount, f"{days} days and counting"]))
    print()
    print("--- suggested public note (EN) ---")
    print(
        f"Today we celebrate a special anniversary: it has been {days} days "
        f"({m[1]}) since invoice {inv['id']} ({amount}) for \"{inv.get('service', 'services rendered')}\" "
        f"went unpaid by {inv['client']}. 🎂 We sent a cake. The invoice is still "
        f"hungry. (Inspired by MetaBrainz, 2013: a $30 cake collected a $20,000 "
        f"debt from Amazon in 24 hours.)"
    )
    print()
    print("--- 建议公开文案 (中文) ---")
    print(
        f"今天是个值得纪念的日子：发票 {inv['id']}（{amount}，{inv.get('service', '服务')}）"
        f"被 {inv['client']} 拖欠已经 {days} 天（{m[2]}）了。🎂 我们决定送个蛋糕庆祝一下。"
        f"（灵感来源：2013 年 MetaBrainz 给 Amazon 送了个三周年蛋糕，$30 的蛋糕 24 小时内收回了 $20,000 欠款。）"
    )


def main(argv=None):
    ap = argparse.ArgumentParser(prog="cakeworthy", description="overdue-invoice cake milestone tracker")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init", help="create a sample invoices.json")
    p_init.add_argument("--file", default=str(DEFAULT_FILE))

    p_check = sub.add_parser("check", help="list invoices that hit a cake milestone")
    p_check.add_argument("--file", default=str(DEFAULT_FILE))

    p_card = sub.add_parser("card", help="print the anniversary card for one invoice")
    p_card.add_argument("invoice_id")
    p_card.add_argument("--file", default=str(DEFAULT_FILE))

    args = ap.parse_args(argv)
    path = Path(args.file)
    if args.cmd == "init":
        cmd_init(path)
    elif args.cmd == "check":
        cmd_check(path)
    elif args.cmd == "card":
        cmd_card(path, args.invoice_id)


if __name__ == "__main__":
    main()
