# blog.bpchub.com DNS 配置表（保留 Shopify 商店）

目标结构：

- `https://bpchub.com` 与 `https://www.bpchub.com`：继续访问 Shopify 商店
- `https://blog.bpchub.com`：访问 GitHub Pages 上的 BPC Hub 内容站

## 修改顺序

1. 先在 GitHub 仓库 `notext404-H1de/bpchub-site` 的 **Settings → Pages → Custom domain** 填 `blog.bpchub.com` 并保存。
2. 再到 Shopify Admin 的 **Settings → Domains**，打开 `bpchub.com` 的 DNS 设置；如果 Shopify 只连接但不管理该域名，则去实际域名服务商管理 DNS。
3. 只添加下面这一条记录。
4. 等 GitHub 显示 DNS check successful 后启用 **Enforce HTTPS**。

## 唯一需要新增的记录

| 类型 | 主机/名称 | 值/目标 | TTL |
| --- | --- | --- | --- |
| CNAME | `blog` | `notext404-H1de.github.io` | 自动或 600 |

目标中不要包含 `https://`、斜杠或仓库名 `bpchub-site`。

## 绝对不要改的记录

- 不要修改根域 `@` 的 Shopify A/AAAA 记录。
- 不要修改 `www` 的 Shopify CNAME。
- 不要删除任何 MX、TXT、SPF、DKIM 或验证记录。
- 不要点击“重置全部 DNS”。Shopify 官方说明指出，重置可能删除已有子域名 CNAME。
- 不要使用 `*.bpchub.com` 通配符记录。

如果已经存在名为 `blog` 的 A、AAAA 或 CNAME，先确认它是否仍在使用；同一个主机名不能同时保留冲突记录。

## 验收

- `https://blog.bpchub.com` 打开 BPC Hub 首页
- `https://bpchub.com` 仍打开 Shopify 商店
- `https://www.bpchub.com` 仍按原方式访问 Shopify 商店
- GitHub Pages 中 Custom domain 为 `blog.bpchub.com`
- GitHub Pages 显示 DNS check successful，并已启用 HTTPS
- 仓库 `static/CNAME` 文件内容为 `blog.bpchub.com`

DNS 通常在几分钟至 24 小时内传播。传播期间不要反复切换记录。

官方文档：

- Shopify 添加和编辑子域名：https://help.shopify.com/en/manual/domains/add-a-domain/add-subdomains
- GitHub Pages 自定义子域名：https://docs.github.com/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site
- GitHub Pages 域名验证：https://docs.github.com/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages
