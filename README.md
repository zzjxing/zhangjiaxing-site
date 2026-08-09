# zhangjiaxing-site

zjx 的个人站点：关于、项目、笔记、《史记》白话讲。  
技术栈：**Astro** + **GitHub Pages**。

线上地址（部署后）：

`https://zzjxing.github.io/zhangjiaxing-site/`

## 本地预览

需要 Node.js 22+。

```bash
npm install
npm run dev
```

浏览器打开终端提示的本地地址。注意开发时也会带上 `/zhangjiaxing-site/` 前缀。

## 发布到 GitHub Pages

1. 安装 [Git](https://git-scm.com/)（若尚未安装）
2. 在 GitHub 新建**公开**仓库，名字建议：`zhangjiaxing-site`
3. 本地执行：

```bash
git init
git add .
git commit -m "Initial Astro personal site"
git branch -M main
git remote add origin https://github.com/zzjxing/zhangjiaxing-site.git
git push -u origin main
```

4. 打开仓库 **Settings → Pages**
   - Source 选 **GitHub Actions**
5. 打开 **Actions** 页，等待 `Deploy to GitHub Pages` 跑完（约 1～2 分钟）

上线后访问：https://zzjxing.github.io/zhangjiaxing-site/

### 域名信息

当前已按用户名 `zzjxing` 配置：

- `site`: `https://zzjxing.github.io`
- `base`: `/zhangjiaxing-site`

若仓库改成 `zzjxing.github.io` 用户主站，把 `base` 改成 `'/'`。

## 写新文章

| 类型 | 目录 |
|------|------|
| 史记章节 | `src/content/shiji/*.md`（需 `title` / `order` / 可选 `summary`） |
| 笔记 | `src/content/notes/*.md`（需 `title` / `date`） |
| 项目 | `src/content/projects/*.md`（需 `title` / `summary`） |

史记章节的上一篇 / 下一篇会按 `order` 自动生成。

## 与 Notion

Notion 里已有一份连载备份；本仓库是正式发布源。两边不必强制同步。
