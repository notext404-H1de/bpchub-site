# BPC Hub 上线手册（blog.bpchub.com）

这个项目是一套可直接部署的 Hugo 静态网站，已预配置域名 `https://blog.bpchub.com/`、响应式主题、SEO、RSS、站点地图、合规页、Amazon 联盟披露、文章模板和 GitHub Pages 自动发布。根域 `bpchub.com` 与 `www` 继续服务现有 Shopify 商店。

当前阶段**不需要 Creators API 凭据**。新 Amazon Associates 账号应先把公开网站和原创内容做好，再用 SiteStripe 创建普通联盟链接。

## 你现在拥有的内容

- 品牌：BPC Hub（Beauty & Personal Care Hub）
- 定位：面向北美读者的英文个人护理决策指南
- 博客域名：`blog.bpchub.com`
- 商店域名：`bpchub.com`（保持 Shopify DNS 不变）
- 技术：Hugo 0.164.0 + 原生 CSS + GitHub Pages
- 已有页面：主页、4 个栏目、About、Editorial Policy、Affiliate Disclosure、Medical Disclaimer、Privacy、404
- 已有文章：1 篇英文示范长文
- 已有保护：内容检查器会阻止未披露的 Amazon 短代码上线

## 第 0 步：上线前只确认三件事

1. 你能登录自己的 GitHub 账号。没有就免费注册一个。
2. 你能进入 `bpchub.com` 的 Shopify 域名或实际 DNS 管理后台。
3. 当前 Contact 页面已设为草稿，邮箱开通前不会公开。

不要把 Amazon、GitHub、域名商的密码或验证码发给任何人。

## 第 1 步：在 Windows 本地预览

1. 解压整个项目，路径尽量短，例如 `D:\bpchub-hugo`。
2. 双击 `setup_windows.bat`。它只会把 Hugo 下载到本项目的 `tools\hugo`，不会修改系统目录。
3. 双击 `preview_windows.bat`。
4. 浏览器打开 `http://localhost:1313`。预览窗口保持打开；按 `Ctrl+C` 停止。

如果 PowerShell 阻止脚本，右键 `setup_windows.bat` 选择“以管理员身份运行”通常**不是**正确做法。先把完整报错保存下来；安装脚本已经为当前进程设置了允许执行，不需要系统级权限。

## 第 2 步：确认品牌、域名与 Contact 状态

用 VS Code 或记事本打开 `hugo.yaml`。建议首先确认：

```yaml
baseURL: https://blog.bpchub.com/
title: BPC Hub

params:
  contactEmail: ""
```

邮箱未开通期间保持 `contactEmail: ""`，且 `content/contact.md` 中保持 `draft: true`。开通邮箱后，填入真实地址、把 Contact 改为 `draft: false`，并在 `hugo.yaml` 的 footer 菜单中重新加入 Contact。不要显示无法收信的地址。

主要内容位于 `content` 文件夹；样式位于 `assets/css/main.css`。首版不加载分析、广告或第三方字体，减少成本和隐私负担。

## 第 3 步：创建 GitHub 仓库

最稳妥的方法是安装 GitHub Desktop：

1. 登录 GitHub Desktop。
2. 选择 **Add an Existing Repository from your Hard Drive**，添加解压后的项目目录。
3. 如果它提示该目录还不是仓库，选择 **create a repository**。
4. 仓库名可用 `bpchub-site`，分支使用 `main`。
5. 提交说明写 `Initial BPC Hub site`，点击 **Commit to main**。
6. 点击 **Publish repository**。使用 GitHub 免费方案时，建议公开仓库以使用 Pages。

熟悉命令行时，也可在项目目录执行：

```bash
git init
git branch -M main
git add .
git commit -m "Initial BPC Hub site"
git remote add origin https://github.com/你的用户名/bpchub-site.git
git push -u origin main
```

## 第 4 步：启用 GitHub Pages

1. 打开 GitHub 仓库的 **Settings → Pages**。
2. 在 **Build and deployment** 下把 **Source** 设为 **GitHub Actions**。
3. 打开仓库的 **Actions** 标签，等待 “Build and deploy BPC Hub” 变成绿色。
4. 第一次成功后，先确认 GitHub 提供的临时 `github.io` 地址可以打开。

项目已包含 `.github/workflows/hugo.yaml`，每次推送到 `main` 都会先检查内容，再自动构建和部署。

## 第 5 步：绑定 blog.bpchub.com

先在 GitHub 仓库的 **Settings → Pages → Custom domain** 填写 `blog.bpchub.com` 并保存，再在 Shopify 或实际 DNS 服务商中只新增 `blog` 的 CNAME。具体记录见 `DNS_配置表.md`。

**不要修改或删除 Shopify 使用的 `@`、`www`、A、AAAA 或现有商店 CNAME 记录。**

DNS 生效后：

1. 回到 **Settings → Pages**，确认 DNS check successful。
2. 勾选 **Enforce HTTPS**；若暂时不能勾选，等待证书签发后再试。
3. 测试 `https://blog.bpchub.com` 打开博客，同时确认 `https://bpchub.com` 仍打开 Shopify 商店。
4. 建议在 GitHub 的域名验证页面验证 `bpchub.com`，降低子域名被错误绑定的风险。

DNS 可能几分钟生效，也可能需要最多约 24 小时。不要在传播期间反复更换记录。

## 第 6 步：完成首批 10 篇原创文章

Amazon 正式审核前，网站应保持公开，并准备足够的原创内容。项目内的 `docs/首批10篇文章计划.md` 已给出选题顺序；`docs/文章发布检查表.md` 用于逐篇验收。

创建新文章：

1. 双击 `new_article_windows.bat`。
2. 选择栏目：`skincare`、`hair-care`、`body-care` 或 `guides`。
3. 输入小写英文文件名，例如 `how-to-choose-face-cleanser`。
4. 编辑生成的 Markdown 文件。
5. 审核完毕后，把文件开头的 `draft: true` 改为 `draft: false`。

不要复制厂家或其他网站的文字，不要声称测试过没有实际测试的产品，也不要为了凑数量一次性发布内容空洞的页面。

## 第 7 步：不用 API，先添加 SiteStripe 链接

新账号不能创建 Creators API 凭据时，仍可按账号当前可用功能使用 Amazon Associates 的 SiteStripe 文本链接：

1. 登录 Amazon Associates。
2. 从 Associates 后台进入对应 Amazon 站点的商品页。
3. 使用页面顶部 SiteStripe 生成你的联盟链接。
4. 在文章 Markdown 中使用下面的短代码，不要手工猜测 tracking ID：

```markdown
{{</* amazon-link
  url="粘贴 SiteStripe 生成的完整链接"
  text="View current details on Amazon"
*/>}}
```

同时把文章 front matter 改为：

```yaml
affiliate: true
```

产品卡片写法：

```markdown
{{</* product-card
  title="Product name"
  url="粘贴 SiteStripe 链接"
  label="Best for compact routines"
  summary="Explain the relevant fit and tradeoff without quoting a fixed price."
*/>}}
```

短代码会自动添加 `rel="sponsored nofollow noopener"`、新窗口保护和 “Paid link” 标签。文章顶部和全站页脚也会显示联盟披露。

不要把可能变化的价格写死在正文里；不要手工下载 Amazon 商品图后上传到站点。API 尚未开放时，优先使用文字链接和你拥有版权的非商品图片。

## 第 8 步：每次发布前检查

Windows 本地构建：

```text
双击 build_windows.bat
```

它会运行 `scripts/check_content.py`，检查：

- 正文文章是否有标题、描述、日期和草稿状态
- 使用 Amazon 短代码的文章是否设置 `affiliate: true`
- 公开原创文章是否达到建议数量
- 是否出现绕过短代码的直接 Amazon 链接

发布时可使用 GitHub Desktop，也可双击 `publish_windows.bat`。推送后在 GitHub Actions 中确认部署变绿，再打开线上页面抽查。

## 第 9 步：Amazon 账号推进顺序

1. 在 Amazon Associates 账号中把 `https://blog.bpchub.com` 加入你运营的网站列表。
2. 保持网站公开、导航完整、合规页可访问。
3. 发布至少 10 篇有实质内容的原创英文文章。
4. 使用自己的 SiteStripe tracking ID 添加合规链接。
5. 获取至少 3 笔合格销售，等待 Associates 正式审核。不要用自己的订单凑数，也不要给亲友返现或激励购买。
6. 达到 Creators API 当前要求后再创建应用和凭据。届时可接入之前准备的自动采集工具。

账号门槛是 Amazon 决定的，网站代码不能绕过。你截图中的红叉表示账号资格未满足，不是浏览器故障。

## 常见问题

### 页面能打开，为什么没有产品？

这是有意设计。首版先建立可信内容和审核基础；产品链接必须由你自己的 SiteStripe 生成，不能代填。

### GitHub Actions 报 content check failed

展开失败步骤，查看以 `ERROR:` 开头的行。最常见原因是文章使用了 Amazon 短代码，却没有设置 `affiliate: true`。

### 联系邮箱还没开通怎么办？

当前 Contact 页面和导航入口已隐藏，博客也没有联系表单。域名邮箱开通后再按第 2 步恢复；隐私政策应同时更新为真实可用的联系方式。

### 可以立刻加 Google Analytics 或广告吗？

技术上可以，但首阶段不建议。新增追踪前需要同步更新隐私政策和必要的同意机制，也会增加性能与合规负担。

### API 凭据开放后改哪里？

本网站仍作为公开内容层。Creators API 数据采集在独立自动化项目中运行，不要把密钥写进 Hugo 仓库或浏览器端代码。
