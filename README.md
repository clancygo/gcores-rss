# Gcores RSS（GitHub 自动更新版）

本项目自动抓取 [机核网最新文章](https://www.gcores.com/articles)，每天生成一次 RSS 文件并托管在 GitHub Pages。

## 📦 使用步骤

1. Fork 或下载本仓库。
2. 启用 **GitHub Actions**：进入仓库 → 点击 “Actions” → 启用 workflow。
3. 打开 “Settings → Pages”，设置 Source 为 `gh-pages` 分支。
4. 几分钟后访问：

```
https://你的用户名.github.io/gcores-rss/feed.xml
```

即可获得自动更新的 RSS。

## ⚙️ 修改更新频率

在 `.github/workflows/build.yml` 中修改：

```
cron: '0 0 * * *'
```

例如：

- 每 3 小时更新一次：`0 */3 * * *`
- 每天一次（默认）：`0 0 * * *`

---

本项目完全免费，无需服务器或 Render。

