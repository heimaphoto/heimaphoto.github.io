---
title: 一次散步的随拍
date: 2026-07-22
category: 摄影笔记
summary: 我的佳能老 5D 快烂掉了，今天散步时想着拿出来拍几张，试试看还能拍吗，还有那只 Planar 50 的老镜头还能用吗？
lead: 
location: 地点；不需要时删除这一行。
camera: CANON EOS 5D 
thumbnail: ../img/example.jpg
---

## 在这里填写文章标题

正文从这里开始。

可以直接写普通段落。段落之间空一行。

如果需要在指定位置插入图片，写：

{{ image: ../img/example-01.jpg | 图片说明可选 }}

如果需要小标题，可以这样写：

## 小标题

继续写正文。

## 支持格式速记

段落：普通文字即可，段落之间空一行。

链接：[链接文字](https://example.com)

引用：每一行引用前都加 `>`，例如：

> 这是引用第一行
> 这是引用第二行

图片：

{{ image: ../img/example-01.jpg | 图片说明可选 }}

## 七种武器 / Gear 文章速记

分类写 `category: 七种武器`，发布后会进入归档页；归档里的“七种武器”链接会指向 `gear.html` 照片墙，不生成单独的 `category/gear.html`。

缩略图建议放在 `../images/gear/xxx.jpg`，并在 front matter 写：

```yaml
thumbnail: ../images/gear/xxx.jpg
gear_note: A quiet daily camera.
```

同一张 `thumbnail` 可能同时出现在首页文章卡片和 Gear 照片墙。首页按 4:3 显示，Gear 照片墙按 1:1 显示，都会用 `object-fit: cover` 裁切；选图时尽量让主体居中并留一点边。

发布 Gear 文章后，`gear.html` 的照片墙会自动读取真实 Gear 文章的链接、标题和 `thumbnail`。只要存在至少一篇真实 Gear 文章，照片墙就不再显示占位符。hover 第二行优先使用 `gear_note`；如果没有写 `gear_note`，就使用 `summary`。

## 文章图片尺寸建议

普通文章正文图片：长边约 1400px。横图可用 1400px 宽，竖图可用 1200-1400px 高。

文章详情页图片会自动支持点击全屏查看；小图标或不想放大的图片，可用原始 HTML 写 `<img class="no-lightbox" src="../img/icon.png" alt="">` 或 `<img data-no-lightbox src="../img/icon.png" alt="">` 排除。

Gear 缩略图建议用 1200 × 1200px，放在 `../images/gear/xxx.jpg`。这张图会用于首页文章卡片和 Gear 照片墙，主体尽量居中。

JPG 导出质量 80-85 通常够用。

也可以写普通 HTML；以 `<` 开头的行会原样输出。
