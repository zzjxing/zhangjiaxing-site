# zjx

Hexo + Fluid 个人博客，部署在 GitHub Pages。

## 本地

```bash
npm install
npx hexo server
```

## 写文章

```bash
npx hexo new "标题"
```

文章在 `source/_posts/`。史记类文章建议加：

```yaml
categories:
  - 史记
```

## 发布

推送到 `main` 后，GitHub Actions 自动构建并发布：

https://zzjxing.github.io/zhangjiaxing-site/
