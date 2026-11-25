# eBay API

[English](#english) · [中文](#中文)

## English

This repo reads public eBay data with Python or curl. You can search live listings and sold listings by keyword, and read a listing's details. You need one EveryInfra API key. You do not need an eBay account or cookie. The same API also works as an MCP tool in Claude and Cursor. Billing is per call: these 3 capabilities cost $0.96 to $1.39 per 1,000 calls. Failed calls and empty results are not charged. The EveryInfra eBay API has 5 capabilities, all listed on the platform page: <https://everyinfra.com/en/ebay-api?utm_source=github&utm_medium=example_repo&utm_campaign=ebay-api>

### Quick start

```bash
git clone https://github.com/everyinfra/ebay-api.git
cd ebay-api
pip install -r requirements.txt
export EVERYINFRA_API_KEY=<your API key>
python main.py search "mechanical keyboard" --out listings.csv
python main.py item "<listing url>" --out item.json
python main.py sold "mechanical keyboard" --out sold.csv
```

- For `item`, pass a listing link (for example https://www.ebay.com/itm/<item number>, any country site) or the bare item number. The `url` from a `search` result works.
- `search` gives asking prices; `sold` gives prices of ended or sold listings. Keep them apart.
- Without `--out`, the command prints the first 3 rows as JSON. With `--out`, it saves a .csv or .json file. The CSV has a BOM, so Excel opens it without garbled text.
- Register at everyinfra.com, then create the API key in the console. Steps: <https://everyinfra.com/en/docs?utm_source=github&utm_medium=example_repo&utm_campaign=ebay-api#quickstart>

### curl

```bash
curl -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"platform":"ebay","action":"search","params":{"keyword":"mechanical keyboard"}}'
```

All capabilities use the same URL. Change `action` and `params` to call another one. Examples for `product_detail` and `sold` are in [examples/curl.sh](examples/curl.sh).

### Claude and Cursor (MCP)

The remote MCP URL is <https://api.everyinfra.com/mcp>. Add the `Authorization: Bearer` header with your API key. EveryInfra runs the server, so you install no local program.

Claude Code:

```bash
claude mcp add --transport http everyinfra https://api.everyinfra.com/mcp --header "Authorization: Bearer <API Key>"
```

Cursor and other clients that read `mcp.json` ([examples/mcp.json](examples/mcp.json)):

```json
{
  "mcpServers": {
    "everyinfra": {
      "url": "https://api.everyinfra.com/mcp",
      "headers": {
        "Authorization": "Bearer <API Key>"
      }
    }
  }
}
```

Custom connectors in Claude on the web and desktop, and ChatGPT, accept only a URL. Enter <https://api.everyinfra.com/mcp/all>, sign in to EveryInfra when asked, and allow access. You do not need to enter a key. Full steps: <https://everyinfra.com/en/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=ebay-api>

### Price

| `action` | Per 1,000 calls |
|---|---|
| `search` | $1.39 |
| `product_detail` | $0.96 |
| `sold` | $1.39 |

- Billing is per call, about $0.00096 to $0.0014 each. Failed calls, empty results, parameter errors, and authentication failures are not charged.
- A new account gets a $1 trial allowance, valid for 24 hours. No credit card is needed. How to claim it: <https://everyinfra.com/en/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=ebay-api>
- Prices for the other 2 eBay capabilities are on the platform page: <https://everyinfra.com/en/ebay-api?utm_source=github&utm_medium=example_repo&utm_campaign=ebay-api>

### Fields

These are the fields that the 3 capabilities returned in our test. Each meaning is the first sentence of the field's entry in the API documentation. The link under each table has the full text.

#### `search` (keyword search)

| Field | Meaning |
|---|---|
| `item_id` | Item ID. |
| `title` | Title. null when the platform has no titles (for example text-only posts). |
| `url` | Link to the record on the platform. |
| `price` | Price as a number without a currency symbol; see currency. |
| `price_text` | Price as originally displayed; may be a range. |
| `currency` | Currency code of the price (for example CNY, USD). |
| `condition` | Item condition (new, refurbished or used). |
| `shipping` | Shipping description. |
| `seller` | Seller name. |
| `image_url` | Image link. |
| `scraped_at` | Time the data was collected. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |

All parameters and fields: <https://everyinfra.com/en/ebay-api/search?utm_source=github&utm_medium=example_repo&utm_campaign=ebay-api>

#### `product_detail` (product details)

| Field | Meaning |
|---|---|
| `item_id` | Item ID. |
| `title` | Title. null when the platform has no titles (for example text-only posts). |
| `subtitle` | Subtitle the seller wrote (product_detail), often a promotional line; absent when there is none. |
| `url` | Link to the record on the platform. |
| `price` | Price as a number without a currency symbol; see currency. |
| `currency` | Currency code of the price (for example CNY, USD). |
| `condition` | Item condition (new, refurbished or used). |
| `availability` | Stock status as eBay states it (product_detail), such as InStock or OutOfStock. |
| `listing_type` | Listing format (auction or fixed price). |
| `best_offer_enabled` | Whether buyers can make the seller an offer (Best Offer) (product_detail). |
| `ends_at` | When the auction or timed listing ends (product_detail), ISO 8601 in UTC; absent for fixed-price listings without an end time. |
| `quantity_available` | Units still available (product_detail); absent when the seller does not show it. |
| `quantity_sold` | Units sold on this listing (product_detail); absent when not shown. |
| `watchers` | People watching the listing (product_detail); absent when eBay does not show it. |
| `brand` | Brand, from the listing's brand or the Brand item specific; absent when the listing does not show it. |
| `model` | Model, from the Model item specific; absent when the listing does not show it. |
| `product_id` | eBay catalog product ID (product_detail); absent when the listing shows none. |
| `categories` | Category path from broad to narrow (product_detail). |
| `image_url` | Image link. |
| `images` | Array of image links in the platform's display order; absent when there are no images. |
| `item_location` | Where the item ships from, as eBay shows it (product_detail). |
| `shipping_price` | Shipping cost amount. |
| `free_shipping` | Whether shipping is free (product_detail). |
| `returns_accepted` | Whether the seller accepts returns (product_detail). |
| `seller` | Seller name. |
| `seller_url` | Link to the seller's store page (product_detail). |
| `seller_feedback_score` | Seller feedback score (net total of positive feedback). |
| `seller_positive_percent` | Seller positive feedback rate, as a percentage. |
| `updated_at` | When this listing record was last updated (product_detail), ISO 8601 in UTC. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |

All parameters and fields: <https://everyinfra.com/en/ebay-api/product_detail?utm_source=github&utm_medium=example_repo&utm_campaign=ebay-api>

#### `sold` (sold listings)

| Field | Meaning |
|---|---|
| `id` | The record's unique ID on the platform. |
| `url` | Link to the record on the platform. |
| `name` | Name of the object itself, for account, product and business capabilities. |
| `sold_price` | Final sold price. |
| `total_price` | Total price including shipping. |
| `currency` | Currency code of the price (for example CNY, USD). |
| `sold_at` | Time of the sale. |
| `condition` | Item condition (new, refurbished or used). |
| `listing_type` | Listing format (auction or fixed price). |
| `best_offer_accepted` | Whether the seller accepted a Best Offer. |
| `seller_username` | Seller username. |
| `seller_feedback_score` | Seller feedback score (net total of positive feedback). |
| `seller_positive_percent` | Seller positive feedback rate, as a percentage. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |
| `shipping_price` | Shipping cost amount. |

All parameters and fields: <https://everyinfra.com/en/ebay-api/sold?utm_source=github&utm_medium=example_repo&utm_campaign=ebay-api>

### FAQ

**Do I need an eBay account or cookie to call the API?**

No. Send the `Authorization: Bearer` header with your API key. The request body holds `platform`, `action`, and the capability parameters. You do not scan a QR code, keep a login session, or open a browser.

**How much does it cost? Are failed calls charged? Is there a free allowance?**

Billing is per call, from $0.96 per 1,000 calls. Failed calls, empty results, parameter errors, and authentication failures are not charged. A new account gets a $1 trial allowance, valid for 24 hours. No credit card is needed. How to claim it: <https://everyinfra.com/en/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=ebay-api>

**Can I connect the eBay API to Claude or Cursor?**

Yes. The remote MCP URL is <https://api.everyinfra.com/mcp>. Add the `Authorization: Bearer` header with your API key. You install no local program. Setup for Claude, Cursor, ChatGPT, and Claude Code: <https://everyinfra.com/en/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=ebay-api>.

**What legal points apply when I use eBay data?**

The EveryInfra Terms of Service require you to make sure your use of the data follows applicable law and the terms of the relevant platform. Do not use the data for anything illegal or anything that violates privacy or intellectual property rights. Do not use bulk scraping for harassment, fraud, or other abuse. When you use personal information such as nicknames and avatars, keep only the fields your business needs.

**Which eBay data can I get?**

The EveryInfra eBay API has 5 capabilities:

- keyword search
- store
- reviews
- sold listings
- product details

Parameters and return fields for each capability are on the platform page: <https://everyinfra.com/en/ebay-api?utm_source=github&utm_medium=example_repo&utm_campaign=ebay-api>

### Tested

Before release, we ran the 3 commands in Quick start against the live API with this repo's code.

| Command | Time (Singapore, UTC+8) | Rows | Charged |
|---|---|---|---|
| `python main.py search "mechanical keyboard" --out listings.csv` | 2026-11-25 13:21 | 20 | $0.001389 |
| `python main.py item "<listing url>" --out item.json` | 2026-11-25 13:22 | 1 | $0.000958 |
| `python main.py sold "mechanical keyboard" --out sold.csv` | 2026-11-25 13:22 | 20 | $0.001389 |

## 中文

本仓库用 Python 或 curl 读 eBay 公开数据：按关键词搜在售商品和已售记录，读商品详情。只需一把 EveryInfra API Key，不用 eBay 账号和 Cookie，也能作为 MCP 工具接进 Claude、Cursor。按调用次数计费，这 3 个能力每千次 $0.96 到 $1.39，失败和空结果不收费。eBay 共 5 个能力：<https://everyinfra.com/ebay-api?utm_source=github&utm_medium=example_repo&utm_campaign=ebay-api>

### 快速开始

```bash
git clone https://github.com/everyinfra/ebay-api.git
cd ebay-api
pip install -r requirements.txt
export EVERYINFRA_API_KEY=<你的 API Key>
python main.py search "mechanical keyboard" --out listings.csv
python main.py item "<商品链接>" --out item.json
python main.py sold "mechanical keyboard" --out sold.csv
```

- `item` 传商品链接（如 https://www.ebay.com/itm/<商品号>，各国站点都行）或纯数字商品号，可用 `search` 结果里的 `url`。
- `search` 是挂牌价，`sold` 是已结束或售出的成交价，两者不要混用。
- 不加 `--out` 时打印前 3 条 JSON；加 `--out` 存成 .csv 或 .json。CSV 带 BOM，Excel 直接打开不乱码。
- API Key 在 everyinfra.com 注册后到控制台创建，步骤见 <https://everyinfra.com/docs?utm_source=github&utm_medium=example_repo&utm_campaign=ebay-api#quickstart>

### 用 curl 调

```bash
curl -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"platform":"ebay","action":"search","params":{"keyword":"mechanical keyboard"}}'
```

所有能力都发到同一个地址，换 `action` 和 `params` 就行；`product_detail`、`sold` 的写法见 [examples/curl.sh](examples/curl.sh)。

### 接进 Claude、Cursor（MCP）

远程 MCP 地址是 <https://api.everyinfra.com/mcp>，请求头加 `Authorization: Bearer` 和 API Key；服务器由 EveryInfra 运行，不用装本地程序。

Claude Code：

```bash
claude mcp add --transport http everyinfra https://api.everyinfra.com/mcp --header "Authorization: Bearer <API Key>"
```

Cursor 等读 `mcp.json` 的客户端（[examples/mcp.json](examples/mcp.json)）：

```json
{
  "mcpServers": {
    "everyinfra": {
      "url": "https://api.everyinfra.com/mcp",
      "headers": {
        "Authorization": "Bearer <API Key>"
      }
    }
  }
}
```

Claude 网页版和桌面版的自定义连接器、ChatGPT 只能填网址：填 <https://api.everyinfra.com/mcp/all>，连接时登录 EveryInfra 并允许，不用填 Key。完整步骤见 <https://everyinfra.com/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=ebay-api>

### 价格

| 能力 | `action` | 每千次 |
|---|---|---|
| 关键词搜索 | `search` | $1.39 |
| 商品详情 | `product_detail` | $0.96 |
| 已售商品 | `sold` | $1.39 |

- 按调用次数计费，每次约 $0.00096 到 $0.0014；失败、空结果、参数错误和鉴权失败都不收费。
- 新账号有 $1 试用额度，24 小时内有效，不用信用卡，领取方式见 <https://everyinfra.com/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=ebay-api>
- eBay 其他 2 个能力的单价见平台页 <https://everyinfra.com/ebay-api?utm_source=github&utm_medium=example_repo&utm_campaign=ebay-api>

### 返回字段

下面是这 3 个能力实测返回的字段，含义取自接口文档每条说明的第一句，完整说明在每张表下面的链接里。

#### `search`（关键词搜索）

| 字段 | 含义 |
|---|---|
| `item_id` | 商品 ID。 |
| `title` | 标题。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `price` | 价格数值，不含货币符号；币种见 currency。 |
| `price_text` | 价格的原始展示文本，可能是区间。 |
| `currency` | 价格币种代码（如 CNY、USD）。 |
| `condition` | 成色（全新/翻新/二手）。 |
| `shipping` | 运费说明。 |
| `seller` | 卖家名。 |
| `image_url` | 图片链接。 |
| `scraped_at` | 数据抓取时刻。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |

完整参数和字段：<https://everyinfra.com/ebay-api/search?utm_source=github&utm_medium=example_repo&utm_campaign=ebay-api>

#### `product_detail`（商品详情）

| 字段 | 含义 |
|---|---|
| `item_id` | 商品 ID。 |
| `title` | 标题。 |
| `subtitle` | 卖家写的副标题（product_detail），常是促销语；没写时没有。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `price` | 价格数值，不含货币符号；币种见 currency。 |
| `currency` | 价格币种代码（如 CNY、USD）。 |
| `condition` | 成色（全新/翻新/二手）。 |
| `availability` | 库存状态（product_detail）：InStock / OutOfStock 等，eBay 原文。 |
| `listing_type` | 上架方式（拍卖/一口价）。 |
| `best_offer_enabled` | 是否可以向卖家议价（product_detail，Best Offer）。 |
| `ends_at` | 拍卖或限时商品的结束时间（product_detail，ISO，UTC）；一口价长期在售的没有。 |
| `quantity_available` | 还剩多少件可买（product_detail）；卖家不显示时没有。 |
| `quantity_sold` | 已售件数（product_detail）。 |
| `watchers` | 关注（加入观察列表）的人数（product_detail）；eBay 不显示时没有。 |
| `brand` | 品牌，取自商品页的品牌或物品属性里的 Brand；商品页没写时没有这个字段。 |
| `model` | 型号，取自物品属性里的 Model；商品页没写时没有这个字段。 |
| `product_id` | 产品目录 ID。 |
| `categories` | 类目路径，从大到小（product_detail）。 |
| `image_url` | 图片链接。 |
| `images` | 全部商品大图链接（product_detail）。 |
| `item_location` | 发货地（product_detail），eBay 显示的原文。 |
| `shipping_price` | 运费金额。 |
| `free_shipping` | 是否包邮（product_detail）。 |
| `returns_accepted` | 是否接受退货（product_detail）。 |
| `seller` | 卖家名。 |
| `seller_url` | 卖家店铺页链接（product_detail）。 |
| `seller_feedback_score` | 卖家信用分（累计好评净值）。 |
| `seller_positive_percent` | 卖家好评率，百分数。 |
| `updated_at` | 这条报价记录的更新时间（product_detail，ISO，UTC）。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |

完整参数和字段：<https://everyinfra.com/ebay-api/product_detail?utm_source=github&utm_medium=example_repo&utm_campaign=ebay-api>

#### `sold`（已售商品）

| 字段 | 含义 |
|---|---|
| `id` | 该记录在原平台上的唯一标识。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `name` | 名称。 |
| `sold_price` | 成交价。 |
| `total_price` | 含运费总价。 |
| `currency` | 价格币种代码（如 CNY、USD）。 |
| `sold_at` | 成交时间。 |
| `condition` | 成色（全新/翻新/二手）。 |
| `listing_type` | 上架方式（拍卖/一口价）。 |
| `best_offer_accepted` | 是否接受议价（Best Offer）。 |
| `seller_username` | 卖家用户名。 |
| `seller_feedback_score` | 卖家信用分（累计好评净值）。 |
| `seller_positive_percent` | 卖家好评率，百分数。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |
| `shipping_price` | 运费金额。 |

完整参数和字段：<https://everyinfra.com/ebay-api/sold?utm_source=github&utm_medium=example_repo&utm_campaign=ebay-api>

### 常见问题

**调用时要不要提供 eBay 账号或 Cookie？**

不用，请求头带 `Authorization: Bearer` 和 API Key 就能调，请求体写 `platform`、`action` 和能力参数。不用扫码、维护登录状态，也不用开浏览器。

**怎么收费？失败了收不收钱？有免费额度吗？**

按调用次数计费，每千次 $0.96 起。失败、空结果、参数错误和鉴权失败都不收费。新账号有 $1 试用额度，24 小时内有效，不用信用卡，领取方式见定价页 <https://everyinfra.com/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=ebay-api>

**能把 eBay 接口接进 Claude、Cursor 吗？**

能，远程 MCP 地址是 <https://api.everyinfra.com/mcp>，请求头加 `Authorization: Bearer` 和 API Key，不用装本地程序。Claude、Cursor、ChatGPT、Claude Code 配置见 <https://everyinfra.com/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=ebay-api>。

**用 eBay 数据要注意哪些合规问题？**

EveryInfra 服务条款要求你自行确保数据用法符合适用法律和相关平台条款，禁止用于违法、侵犯隐私或知识产权，或批量抓取用于骚扰、欺诈等恶意用途。用到昵称、头像等个人信息时，只留业务用得上的字段。

**可以拿到 eBay 的哪些数据？**

eBay 有 5 个能力：关键词搜索、店铺、评价、已售商品、商品详情。每个能力的参数和返回字段见平台页 <https://everyinfra.com/ebay-api?utm_source=github&utm_medium=example_repo&utm_campaign=ebay-api>

### 实测记录

发布前用本仓的代码对线上接口跑过一遍，命令就是「快速开始」里的 3 条。

| 命令 | 时间（新加坡时间） | 返回条数 | 扣费 |
|---|---|---|---|
| `python main.py search "mechanical keyboard" --out listings.csv` | 2026-11-25 13:21 | 20 | $0.001389 |
| `python main.py item "<商品链接>" --out item.json` | 2026-11-25 13:22 | 1 | $0.000958 |
| `python main.py sold "mechanical keyboard" --out sold.csv` | 2026-11-25 13:22 | 20 | $0.001389 |

`product_detail` 返回的一条（正文截到 60 字，作者字段没放进来）：

```json
{
  "item_id": "267452287168",
  "title": "Akko 5098B Prunus Lannesiana Mechanical Keyboard With LCD Screen, Pink",
  "price": 49.99,
  "currency": "USD",
  "brand": "Akko",
  "model": "5098B"
}
```

## License

MIT
