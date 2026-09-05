---
title: 网站文章页面增加英文区块
date: 2026-09-05
category: 建站记录
summary: 本站文章页面增加双语支持，以下是制定的规范备忘。
lead: 最近在 X 上发现很多优秀的摄影师账号，我也想加入进去，虽然早就有 Twitter 账号，但很多年没登录了。X 具有国际性，在上面更适合发英文信息。跟 AI 聊了一下，我不想增加自己负担，所有英文翻译就交给他去处理了。
---

## 网站文章页面增加英文区块

以下是 AI 为我制定的双语支持规范，由 ChatGPT 聊天体制定，由 Codex 添加进技能执行。

> ### 请为 HEIMA PHOTO 增加文章页中英双语支持。

> 请先完整检查当前项目的 Markdown 解析方式、front matter、文章页模板、image shortcode、CSS 和响应式布局，再开始修改。
> 
> 这次修改的核心原则是：
> 
> 保持 HEIMA PHOTO 现有设计和 Markdown 写作方式；不重新设计网站；不让程序自动决定中英文正文或照片的位置。Markdown 中写在哪里，页面就显示在哪里。
> 
> ⸻
> 
> 一、首页保持不变
> 
> 这次只修改文章详情页。
> 
> 首页保持目前的中文形式：
> 
> * 不修改首页文章列表和卡片布局。
> * 不在首页增加英文标题、英文摘要。
> * 不改变现有卡片高度和排版。
> * 不因为双语功能调整首页 CSS。
> 
> 即使 Markdown front matter 中以后存在英文元数据，目前首页也不读取和显示。
> 
> ⸻
> 
> 二、Lead 固定采用“中文 + English”
> 
> 文章页顶部现有 lead 区域改为支持双语。
> 
> Markdown/front matter 中增加可选字段：
> 
> lead: 中文 lead
> lead_en: English lead
> 
> 页面显示顺序固定为：
> 
> 中文 lead
> English lead
> 
> 视觉要求：
> 
> * 中文 lead 尽量保持目前样式不变。
> * English lead 紧跟中文 lead。
> * English lead 字号可以比中文略小。
> * English lead 文字颜色比中文稍轻，但必须保持良好可读性。
> * 两者之间只有较小的垂直间距。
> * 不使用卡片、背景、边框。
> * 不使用斜体作为语言区别。
> * 不显示额外的 “ENGLISH” 标签。
> 
> 如果旧文章没有 lead_en，则完全按照目前的方式只显示中文 lead，不留空白。
> 
> ⸻
> 
> 三、正文的核心原则：Markdown 决定一切顺序
> 
> 这是本次修改最重要的原则。
> 
> 不要让模板自动移动、拆分或重新排列任何正文、英文区块或图片。
> 
> Markdown 中：
> 
> * 中文写在哪里，就显示在哪里。
> * English 区块写在哪里，就显示在哪里。
> * image shortcode 写在哪里，图片就显示在哪里。
> 
> 程序只负责把不同类型的内容按照相应样式渲染出来。
> 
> 例如一篇文章可以是：
> 
> 中文第一段
> ENGLISH(English translation of paragraph 1)
> 照片 1(中英 caption)
> 中文第二段
> ENGLISH(English translation of paragraph 2)
> 照片 2(中英 caption)
> 中文第三段...
> 
> 另一篇短文章也可以是：
> 
> 中文第一段
> 中文第二段
> 中文第三段
> ENGLISH(English translation of all three paragraphs)
> 照片 1
> 照片 2
> 
> 还可以是：
> 
> 中文第一、二段
> ENGLISH(English translation)
> 照片
> 中文第三、四段
> ENGLISH(English translation)
> 照片
> 
> 以上都必须使用完全相同的模板和 CSS，不需要特殊处理。
> 
> 不要假设英文一定在中文之后，也不要假设照片一定在英文之前或之后。
> 
> ⸻
> 
> 四、设计一个简单的 English 正文区块语法
> 
> 请根据项目现有 Markdown parser 的能力，选择最简单、最稳定、最容易长期维护的方式来标记英文正文。
> 
> 优先考虑类似：
> 
> :::english
> English text here.
> :::
> 
> 最终渲染为类似：
> 
> <section class="article-en">
>   ...
> </section>
> 
> 如果当前 Markdown parser 不适合 :::english 这种 container/directive 语法，请不要为了实现它引入大型依赖。
> 
> 可以选择与现有系统更兼容的简单方案。
> 
> 但最终 Markdown 必须做到：
> 
> 1. 容易手写；
> 2. 一眼能够看出这是英文区块；
> 3. 可以在一篇文章中出现多次；
> 4. 可以插在正文任何位置；
> 5. 不影响前后 image shortcode；
> 6. 旧文章完全兼容。
> 
> 请在修改完成后告诉我最终推荐的 Markdown 写法。
> 
> ⸻
> 
> 五、English 区块的视觉设计
> 
> English 区块的目的不是把页面切成两个明显区域，而只是让读者自然知道：
> 
> “这里是前面中文内容对应的英文版本。”
> 
> 因此不要：
> 
> * 使用不同背景色；
> * 使用卡片；
> * 使用边框；
> * 使用阴影；
> * 使用明显色块；
> * 改变整个页面背景。
> 
> English 区块仍然属于同一篇文章。
> 
> 每个 English 区块顶部显示一个低调的：
> 
> ENGLISH
> 
> 视觉建议：
> 
> * 小字号；
> * 正常或稍轻字重；
> * 适当 letter-spacing；
> * 颜色比正文稍轻；
> * 与上方中文内容留出适当空间；
> * 不要做成明显的大标题。
> 
> ⸻
> 
> 六、英文正文宽度略窄
> 
> 英文长文阅读时行宽可以比中文略窄。
> 
> 请先检查当前中文正文实际的 max-width，不要直接照搬固定数字。
> 
> 设计原则：
> 
> 如果当前中文正文约为：
> 
> max-width: 680px;
> 
> 那么英文正文可以考虑：
> 
> max-width: 600px ~ 620px;
> 
> 并保持居中。
> 
> 但这只是设计原则，请根据现有页面实际尺寸确定最终数值。
> 
> 目的只是让英文行长更舒服，不是让英文看起来像另一个独立页面。
> 
> ⸻
> 
> 七、英文正文字体与颜色
> 
> 不要额外加载新的 Web Font。
> 
> 继续使用网站现有的西文字体/font stack。
> 
> 英文正文：
> 
> * 字号与中文正文接近；
> * 可以略小，但差异不要明显；
> * 行高针对英文阅读稍作优化；
> * 文字颜色可以比中文正文稍轻；
> * 但必须保证足够的对比度和阅读舒适度。
> 
> 整体效果应该是：
> 
> 中文是页面主要视觉语言，English 稍微退后半级，但仍然是正式正文，而不是注释。
> 
> ⸻
> 
> 八、图片 caption 增加中英双语
> 
> 目前网站已有类似：
> 
> {{ image: image-path | 中文 caption }}
> 
> 的图片 shortcode。
> 
> 请在保持旧语法兼容的前提下，为它增加英文 caption。
> 
> 优先考虑：
> 
> {{ image: image-path | 中文 caption | English caption }}
> 
> 如果根据当前 parser 的实现，有更简单可靠的方案，可以调整，但不要为了 caption 引入复杂依赖。
> 
> ⸻
> 
> 九、双语 caption 的桌面布局
> 
> 当图片同时存在中文和英文 caption 时：
> 
> 桌面端显示要求：
> 
> * 中文在左；
> * English 在右；
> * 中间使用一条很淡的竖向分隔线；
> * 两边留出舒适间距；
> * 两边宽度合理；
> * 整个 caption 仍然保持低调；
> * English caption 颜色可以略浅。
> 
> 不要让 caption 的视觉重量超过照片。
> 
> ⸻
> 
> 十、双语 caption 的手机布局
> 
> 要求：
> 
> * 两者之间保持较小间距；
> * English 可以略浅；
> * 使用正常可用宽度。
> 
> 如果只有中文 caption：
> 
> {{ image: image-path | 中文 caption }}
> 
> 必须继续保持目前的单语 caption 显示方式。
> 
> ⸻
> 
> 十一、不要自动处理正文翻译关系
> 
> 程序不需要知道：
> 
> “这个 English 区块对应前面的哪几段中文。”
> 
> 这个关系由 Markdown 作者自己决定。
> 
> 例如：
> 
> 中文第一段。
> :::english
> English translation of the first paragraph.
> :::
> 
> 或者：
> 
> 中文第一段。
> 中文第二段。
> 中文第三段。
> :::english
> English translation of all three paragraphs.
> :::
> 
> 对于模板而言没有区别。
> 
> 不要开发自动翻译、自动匹配中文段落、自动移动 English 区块之类的逻辑。
> 
> English 区块只是一个带特殊样式的 Markdown 内容容器。
> 
> ⸻
> 
> 十二、响应式设计
> 
> 请重点检查：
> 
> * Desktop
> * iPad / Tablet
> * Mobile
> 
> 特别确认：
> 
> 1. English 正文在桌面端略窄；
> 2. Tablet 上不要因为固定宽度造成异常；
> 3. Mobile 上 English 正文自然使用可用宽度；
> 4. lead + lead_en 在手机上间距自然；
> 5. 多个 English 区块连续出现在一篇文章中时布局正常；
> 6. English 区块前后紧邻图片 shortcode 时布局正常。
> 
> ⸻
> 
> 十三、旧文章必须完全向后兼容
> 
> 网站已经存在大量中文 Markdown。
> 
> 这是硬性要求：
> 
> * 旧 Markdown 不需要修改。
> * 没有 lead_en 时不显示英文 lead。
> * 没有 English 区块时页面和目前保持一致。
> * 旧 image shortcode 继续正常工作。
> * 只有中文 caption 时保持现有 caption 布局。
> * 不修改文章 URL。
> * 不修改现有图片路径规则。
> * 不因为新增 CSS 改变旧文章正文宽度或视觉效果。
> 
> ⸻
> 
> 十四、尽量最小化代码改动
> 
> 不要重构与双语功能无关的代码。
> 
> 不要为了实现这个功能引入大型框架或复杂依赖。
> 
> 优先利用现有：
> 
> * Markdown parser
> * article template
> * image shortcode parser
> * CSS
> * responsive breakpoint
> 
> 实现。
> 
> HEIMA PHOTO 的设计原则仍然是：
> 
> 简单、克制、长期可维护。
> 
> 双语功能应该像原本就属于网站一样，而不是在现有网站上外挂了一套“国际版”。
> 
> ⸻
> 
> 十五、完成后请不要直接继续大范围修改
> 
> 第一阶段先完成一个最小可运行版本。
> 
> 完成后请向我说明：
> 
> 1. 修改了哪些文件；
> 2. 每个文件修改了什么；
> 3. English 区块最终采用什么 Markdown 语法；
> 4. 双语 image caption 最终采用什么语法；
> 5. 新增了哪些 CSS class；
> 6. English 正文最终采用多大 max-width，以及为什么；
> 7. English 正文和 English lead 使用了什么字号、颜色和行高；
> 8. Desktop / Tablet / Mobile 分别如何处理；
> 9. 如何保证旧文章兼容。
> 
> 不要在第一阶段为了“优化”而继续修改首页、导航、About、Gear 或其他页面。
