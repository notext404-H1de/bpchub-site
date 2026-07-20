# BPC Hub

Hugo site for [blog.bpchub.com](https://blog.bpchub.com), an independent English-language beauty and personal care guide for North American readers. The root domain remains connected to the existing Shopify storefront.

请从 **[README_部署说明.md](README_部署说明.md)** 开始，按步骤完成本地预览、GitHub Pages 发布、DNS 绑定和 Amazon SiteStripe 链接配置。

## Quick checks

```bash
python3 scripts/check_content.py
hugo --gc --minify
```

The site intentionally contains no client-side analytics, advertising scripts, or API credentials in its initial version.
