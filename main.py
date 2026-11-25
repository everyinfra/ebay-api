"""eBay API 示例（eBay API in Python）。

  python main.py search "mechanical keyboard" --out listings.csv # 搜在售商品 / search listings
  python main.py item "<商品链接>" --out item.json               # 商品详情 / listing detail
  python main.py sold "mechanical keyboard" --out sold.csv       # 已售记录 / sold listings
"""
import argparse

from everyinfra import fetch, report


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search", help="按关键词搜在售商品 / search live listings")
    s.add_argument("keyword")
    s.add_argument("--condition", help="New / Used / Refurbished / For parts or not working")
    s.add_argument("--domain", help="站点，默认 ebay.com / site, default ebay.com")
    i = sub.add_parser("item", help="商品详情 / one listing")
    i.add_argument("url")
    so = sub.add_parser("sold", help="已售记录 / sold listings")
    so.add_argument("keyword")
    so.add_argument("--days", type=int, help="往前看几天，默认 30 / days back, default 30")
    for x in (s, i, so):
        x.add_argument("--out", help="存成 .csv 或 .json / write .csv or .json")
    a = p.parse_args()

    if a.cmd == "search":
        params = {"keyword": a.keyword, **({"condition": a.condition} if a.condition else {}), **({"domain": a.domain} if a.domain else {})}
        rows, charged = fetch("search", params)
    elif a.cmd == "item":
        rows, charged = fetch("product_detail", {"url": a.url})
    else:
        params = {"keyword": a.keyword, **({"days": a.days} if a.days else {})}
        rows, charged = fetch("sold", params)
    report(rows, charged, a.out)


if __name__ == "__main__":
    main()
