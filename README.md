# cakeworthy 🎂

A tiny CLI that tracks overdue invoices and tells you when one hits a **cake milestone**.

## The story

In December 2013, the non-profit behind MusicBrainz (MetaBrainz) was owed ~$20,000 by Amazon — invoice #144, unpaid for almost 3 years, nearly 10% of their annual budget. Six months of polite pestering went nowhere.

So they ordered a $30 anniversary cake from Larsen's Danish Bakery in Seattle, delivered it to Amazon HQ, and posted a photo publicly. BoingBoing picked it up.

Within 24 hours, Amazon's accounts-payable team found the blocking problem, fixed it, and overnighted a check.

**A $30 cake beat six months of polite emails.** cakeworthy is built on that energy.

> Source: MetaBrainz Blog, ["Using cakes for social engineering"](http://blog.metabrainz.org/2013/12/05/using-cakes-for-social-engineering/) (Dec 2013)

## What it does

- `cakeworthy check` — scans your `invoices.json` and lists invoices that reached a milestone: **30 / 60 / 90 / 180 / 365 / 730 / 1095 days** overdue (满月 / 双月 / 季度 / 半年 / 周年 / 两周年 / 三周年).
- `cakeworthy card <id>` — prints an ASCII anniversary cake and drafts a playful, MetaBrainz-style public note in **English + 中文**. What you do with the cake is your business.

## Usage

```bash
# one file, stdlib only — no install
python3 cakeworthy.py init          # create invoices.json template
python3 cakeworthy.py check         # which invoices are cake-worthy today?
python3 cakeworthy.py card INV-001  # print the anniversary card
```

`invoices.json` format:

```json
[
  {
    "id": "INV-2026-001",
    "client": "Acme Corp",
    "amount": 4800.00,
    "currency": "USD",
    "due": "2026-06-01",
    "service": "API integration work"
  }
]
```

## 中文

一个追踪逾期发票的小工具：当某张发票逾期达到 30/60/90/180/365/730/1095 天这些"整天数"时，提醒你它已经"值得送个蛋糕了"，并生成一张 ASCII 周年蛋糕卡 + 得体又幽默的公开催款文案（中英双语）。

灵感来自 2013 年 MetaBrainz 的真实故事：Amazon 拖欠约 $20,000 发票近三年，六个月的礼貌催款石沉大海；他们订了个 $30 的三周年蛋糕送到 Amazon 总部并公开晒图，24 小时内支票就寄出来了。

## License

MIT
