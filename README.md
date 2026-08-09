# zjx

Hexo + [Aurora](https://github.com/auroral-ui/hexo-theme-aurora) 个人博客，部署在 GitHub Pages。

## 本地

```bash
npm install
npm run build
npx hexo server
```

> 项目站子路径需要 `tools/patch-aurora-base.py`；`npm run build` 已包含。

## 写文章

```bash
npx hexo new "标题"
```

文章在 `source/_posts/`。史记类可加：

```yaml
categories:
  - 史记
feature: true
```

## 发布

推送到 `main` 后自动发布：

https://zzjxing.github.io/zhangjiaxing-site/
