# Heima Photo 手动发布备忘录

这份文件用于在无法使用 Codex 时，自己用仓库里的发布脚本生成网站页面。  
如果以后发布脚本、目录结构或文章格式有变化，请同步修改这份备忘录。

## 1. 进入网站仓库

打开终端，进入 Heima Photo 仓库：

```bash
cd /Users/wangbin/Documents/git/heimaphoto.github.io
```

可以先看一下当前改动：

```bash
git status --short
```

## 2. 准备文章 Markdown

文章放在 `md/` 文件夹内。可以参考 `md/_template.md`，但不要直接发布 `_template.md`，脚本会忽略所有 `_` 开头的 Markdown 文件。

文章文件名会成为最终文章页面的文件名。例如：

```text
md/64-example.md
```

发布后会生成：

```text
article/64-example.html
```

文章开头必须有 front matter，至少包含：

```yaml
---
title: 文章标题
date: 2026-06-16
category: 散文
summary: 首页文章卡片使用的摘要。
---
```

常用可选字段：

```yaml
lead: 文章页标题下方的导言。
category_slug: prose
thumbnail: ../img/example.jpg
location: 地点
camera: 相机或器材
gallery:
  - ../img/example-01.jpg
  - ../img/example-02.jpg
```

注意：front matter 尽量保持简单单行格式，尤其是 `summary`、`lead`。不要写成 YAML 多行块，否则脚本可能解析失败。

常用分类：

```yaml
散文: prose
摄影: photography
摄影笔记: Photography
看的艺术: TheArtOfSeeing
摄影技术: technology
器材: gear
建站: website
建站记录: site
生活: life
```

如果新增了一个从未用过的分类，最好同时检查 `tools/publish_article.py` 里的 `CATEGORY_SLUGS` 和 `CATEGORY_EN`，避免生成奇怪的哈希分类页。

## 3. 正文格式

正文可以直接写普通 Markdown 段落。段落之间空一行。

链接：

```markdown
[链接文字](https://example.com)
```

引用：

```markdown
> 这是引用第一行
> 这是引用第二行
```

图片：

```markdown
{{ image: ../img/example-01.jpg | 图片说明可选 }}
```

也可以写普通 HTML。以 `<` 开头的行会原样输出。

## 4. 运行发布脚本

在仓库根目录运行：

```bash
python3 tools/publish_article.py md/64-example.md
```

命令里指定一篇文章即可。脚本会重新扫描整个 `md/` 和 `photo-md/`，并重建相关页面。

`tools/` 里还有一个 `publish_photo.py`，它是给 `photo-md/` 摄影作品用的便捷入口。它内部仍然调用 `publish_article.py` 的同一套生成系统，所以原理是一样的。

发布普通文章时用：

```bash
python3 tools/publish_article.py md/64-example.md
```

发布 `photo-md/` 里的摄影作品时，也可以用：

```bash
python3 tools/publish_photo.py photo-md/example.md
```

正常输出类似：

```text
Published 63 article(s), 2 photo work(s).
```

发布脚本会更新这些页面：

```text
index.html
archive.html
about.html
article/*.html
category/*.html
portfolio/index.html
photo/*.html
```

首页里的手工块会被保留，例如：

```text
MANUAL-HERO
MANUAL-RECOMMENDATIONS
MANUAL-FEATURED-PHOTOS
```

也就是说：首页右上角 hero 图片区域、侧栏手工链接、精选照片这三块都可以手工调整；只要保留对应的 `START` / `END` 注释标记，下次发布时脚本会尽量保留这些内容。

但不要在生成区里做只想长期保留的手工修改，因为下次发布可能会被脚本覆盖。

## 5. 本地预览

在仓库根目录启动本地服务器：

```bash
python3 -m http.server 8000
```

浏览器打开：

```text
http://127.0.0.1:8000
```

重点检查：

- 首页最新文章和侧栏手工链接
- 新文章页面
- `archive.html`
- 对应的 `category/*.html`
- `about.html` 里的分类链接
- 上一篇、下一篇导航

预览结束后，在终端按 `Ctrl+C` 停止服务器。

## 6. 发布前检查

查看改动：

```bash
git status --short
```

如果想看具体差异：

```bash
git diff
```

可以检查脚本语法：

```bash
python3 -B -c "compile(open('tools/publish_article.py', encoding='utf-8').read(), 'tools/publish_article.py', 'exec')"
```

如果文章改了分类或文件名，注意是否需要删除旧的生成页。例如从：

```text
article/43-prose.html
```

改为：

```text
article/43-Photography.html
```

旧页面不会自动删除，需要确认没有链接指向它后再删除。

## 7. 提交并推送

确认无误后：

```bash
git add .
git commit -m "Publish new article"
git push
```

推送后，GitHub Pages 会自动更新线上网站。
