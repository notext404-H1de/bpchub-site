# Amazon 链接短代码示例（不要直接发布）

以下 URL 只是占位符，不能作为真实联盟链接发布。请从你自己的 Amazon Associates SiteStripe 复制完整链接。

## 文本链接

```markdown
{{</* amazon-link
  url="https://www.amazon.com/your-sitestripe-link"
  text="View current details on Amazon"
*/>}}
```

## 产品卡片

```markdown
{{</* product-card
  title="Exact current product name"
  url="https://www.amazon.com/your-sitestripe-link"
  label="Best for small bathrooms"
  summary="A concise explanation of fit and tradeoff; do not place a fixed price here."
*/>}}
```

文章 front matter 同时设置：

```yaml
affiliate: true
```
