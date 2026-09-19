---
title: 给七种武器的Published Work增加子标题功能
date: 2026-09-19
category: 建站记录
summary: 为七种武器页面的 Published Work 增加轻量的二级分类：只需在 camera、lens 或 film 元数据中以 `:::` 标记子标题，便能按不同机型或胶卷风格归档作品，同时保持旧文章兼容。
lead: 为了更清楚地记录同一件器材下的不同使用风格，我给七种武器的 Published Work 增加了可选子标题。这个小约定不改变现有文章，只让作品与器材之间的关联多了一层整理方式。
---

## 给七种武器的Published Work增加子标题功能

为详细记录不同胶卷或相机app中的不同风格，我考虑给 Published Work 增加子标题功能。即在 Published Work 下面扩展一级分类标题。比如，Dazz cam 的七种武器页面中会包含 “S Classic” 或 “Classic U” 相机的发布文章汇总，这样便于了解自己使用（喜欢）哪种风格更多。又比如，即将推出柯达胶卷的七种武器页面中，会再细分到 Gold 200 / ultra 400 等。

同样我把想法交给 ChatGPT 后，让他为我制定了规范指令，再交给 Codex 添加进技能执行。以下是规范备忘。

> 请修改 Heima Photo 网站的 Gear / 七种武器 Published Work 生成逻辑，增加一个非常轻量的二级分类机制。
> 
> 【一、目标】
> 
> 目前文章和 Photo Work 可以通过以下字段关联到 Gear 页面：
> 
> camera:
> lens:
> film:
> 
> Gear 页面中的 `### Published Work` 会自动列出相关作品。
> 
> 现在希望在不增加新的 front matter 字段、不引入数据库、不改变现有网站结构的前提下，让 Gear metadata 支持可选的二级分类。
> 
> 采用一个简单约定：
> 
> :::
> 
> 作为一级 Gear 和二级分类之间的分隔符。
> 
> 例如：
> 
> film: kodak ::: Gold 200
> 
> 表示：
> 
> Gear = kodak
> Sub Gear = Gold 200
> 
> 另一个例子：
> 
> film: kodak ::: Portra 400
> 
> 表示：
> 
> Gear = kodak
> Sub Gear = Portra 400
> 
> 
> 【二、必须保持向后兼容】
> 
> 这是最重要的要求。
> 
> 现有 metadata：
> 
> film: kodak
> 
> 必须继续按照现在的逻辑工作，不需要修改已有文章。
> 
> 只有 metadata 中出现 `:::` 时才启用二级分类：
> 
> film: kodak ::: Gold 200
> 
> 规则：
> 
> 没有 :::  → 保持现有 Published Work 行为
> 有 :::    → 解析为一级 Gear + 二级分类
> 
> 不要要求用户修改现有文章。
> 
> 不要增加新的 front matter 字段，例如：
> 
> gear_group:
> gear_subgroup:
> 
> 也不要创建数据库、JSON 数据文件或新的 CMS 结构。
> 
> 
> 【三、解析规则】
> 
> 对 camera、lens、film 三个字段统一支持：
> 
> <gear-slug> ::: <sub-title>
> 
> 例如：
> 
> camera: canon ::: EOS 5D
> lens: zeiss ::: Planar 50mm F1.4
> film: kodak ::: Gold 200
> 
> 解析时：
> 
> 1. `:::` 左侧是原有 Gear slug。
> 2. `:::` 右侧是二级分类显示名称。
> 3. 二级分类名称允许包含空格、大小写和数字。
> 4. 对 `:::` 两侧进行 trim，避免因为空格导致匹配问题。
> 5. Gear 的一级匹配规则继续遵守现有规则：按照 Gear slug 做 case-insensitive exact match。
> 6. 不要把整个 `kodak ::: Gold 200` 当成 Gear slug 去匹配。
> 7. 如果 `:::` 右侧为空，则不要生成空的二级标题，应按普通 Gear metadata 处理。
> 8. 如果 metadata 中没有 `:::`，保持现有逻辑。
> 
> 
> 【四、Gear 页面 Published Work 的生成方式】
> 
> 当 Gear 页面发现相关作品包含二级分类时，在 `### Published Work` 下按照二级分类分组。
> 
> 例如：
> 
> film: kodak ::: Gold 200
> 
> 最终 Kodak Gear 页面可以生成：
> 
> ### Published Work
> 
> #### Gold 200
> 
> [2026-09-18 Article A](../article/example-a.html)
> [2026-09-15 Article B](../article/example-b.html)
> 
> #### Portra 400
> 
> [2026-08-20 Article C](../article/example-c.html)
> [2026-08-12 Photo Work D](../photo/example-d.html)
> 
> 要求：
> 
> - 二级标题使用 metadata 中 `:::` 右侧的原始显示名称。
> - 不要强制把显示名称转换成 slug。
> - 不要把 `Gold 200` 转换成 `gold-200` 作为显示文字。
> - URL slug 逻辑保持现有系统不变。
> - Published Work 仍然按照日期 newest-first 排序。
> - 同一个二级分类下的 Article 和 Photo Work 继续混合按照日期排序。
> - 不要改变现有 Published Work 的链接格式。
> 
> 
> 【五、没有二级分类的 Published Work 怎么处理】
> 
> 同一个 Gear 页面可能同时存在普通 metadata 和带二级分类的 metadata。
> 
> 例如：
> 
> film: kodak
> film: kodak ::: Gold 200
> film: kodak ::: Portra 400
> 
> 结果应类似：
> 
> ### Published Work
> 
> [2026-09-10 普通作品](../article/example.html)
> 
> #### Gold 200
> 
> [2026-09-18 Article A](../article/example-a.html)
> [2026-09-15 Article B](../article/example-b.html)
> 
> #### Portra 400
> 
> [2026-08-20 Article C](../article/example-c.html)
> 
> 规则：
> 
> - 没有二级分类的作品保留在 Published Work 顶层。
> - 有二级分类的作品放入对应二级标题。
> - 不要为了容纳未分类作品而自动创建 `Other`。
> - 不要创建 `Unclassified`。
> - 不要给没有二级分类的作品人为增加分类。
> 
> 
> 【六、同一个二级分类必须自动合并】
> 
> 例如：
> 
> kodak ::: Gold 200
> kodak ::: Gold 200
> kodak ::: Gold 200
> 
> 只能生成一个：
> 
> #### Gold 200
> 
> 下面列出所有相关作品。
> 
> 不能生成：
> 
> #### Gold 200
> ...
> 
> #### Gold 200
> ...
> 
> 如果出现：
> 
> Gold 200
> gold 200
> GOLD 200
> 
> 应视为同一个二级分类，避免生成重复标题。
> 
> 最终显示名称优先使用第一次出现的原始显示名称。
> 
> 
> 【七、保持现有 Gear 匹配逻辑】
> 
> 现有 Skill 已经规定：
> 
> - 只通过 camera、lens、film 匹配 Gear；
> - Gear slug 必须 exact match；
> - 不通过 title、body、image name 等内容猜测；
> - Gear slug 来自 Gear article source filename。
> 
> 这些规则全部保留。
> 
> 这次只是把 metadata 从：
> 
> kodak
> 
> 扩展为：
> 
> kodak ::: Gold 200
> 
> 解析后实际参与 Gear 匹配的仍然只是：
> 
> kodak
> 
> 不能影响现有 article/photo detail page 上 metadata 回链到 Gear 页面的逻辑。
> 
> 例如：
> 
> film: kodak ::: Gold 200
> 
> 文章页面可以继续显示用户填写的完整值：
> 
> Film: kodak ::: Gold 200
> 
> 但 Gear 回链必须指向 kodak 对应的 Gear 页面，而不是寻找：
> 
> kodak ::: Gold 200
> 
> 对应的 Gear 页面。
> 
> 
> 【八、Article Publisher 和 Photo Publisher 必须统一】
> 
> 这个功能同时适用于：
> 
> 1. 普通 Article
> 2. Photo Work
> 
> Article Publisher 和 Photo Publisher 目前共享 Gear Published Work maintenance，因此请优先修改共享的 Gear 处理逻辑，而不是复制两套实现。
> 
> Photo Publisher 的 camera / lens / film 也必须使用完全相同的 `:::` 解析规则。
> 
> 
> 【九、不要破坏手工内容】
> 
> 现有规则要求保留 Gear 页面 Published Work 区域中的手工内容。
> 
> 必须继续遵守。
> 
> 不要粗暴删除整个 Gear 页面中的：
> 
> ### Published Work
> 
> 不要覆盖用户手工维护的内容。
> 
> 如果当前实现已经存在明确的自动生成区域或 marker，请沿用现有机制。
> 
> 这次改动只增加二级分类能力，不要重新设计 Gear 页面。
> 
> 
> 【十、二级分类只属于 Gear Published Work】
> 
> 本次功能只解决：
> 
> Gear
> └── Published Work
>     ├── 普通作品
>     ├── Gold 200
>     └── Portra 400
> 
> 不要把这个机制扩展为：
> 
> - category 二级分类
> - article category hierarchy
> - site navigation hierarchy
> - 新的 URL hierarchy
> - 新的 Gear 页面
> - 数据库
> - JSON 数据文件
> - runtime dependency
> 
> 
> 【十一、更新规则文件和 Skill】
> 
> 这是一次发布行为的改变，因此必须按照 Heima Photo 现有规则处理。
> 
> 请：
> 
> 1. 先修改 repository 中的 Skill source。
> 2. 更新：
> 
> skills/site-rules.md
> 
> 3. 更新 Article Publisher Skill。
> 4. 更新 Photo Publisher Skill。
> 5. 然后运行：
> 
> python3 tools/install_skills.py
> 
> 6. 确认 repository skill 与 installed skill 已同步。
> 7. 使用：
> 
> diff -rq
> 
> 验证 repository 与 installed copies。
> 
> 
> 不要只修改 ~/.codex/skills/ 下的 runtime copy。
> 
> 
> 【十二、在 Skill 文档中加入简短说明】
> 
> 请加入类似下面的说明：
> 
> 普通 Gear：
> 
> film: kodak
> 
> 表示直接关联 Kodak Gear。
> 
> 带二级分类：
> 
> film: kodak ::: Gold 200
> 
> 表示：
> 
> Kodak
> └── Gold 200
> 
> Gear 页面：
> 
> ### Published Work
> 
> 普通作品……
> 
> #### Gold 200
> 
> 相关作品……
> 
> 
> 【十三、测试要求】
> 
> 修改完成后必须实际测试。
> 
> 至少验证以下情况。
> 
> Test 1：普通 metadata
> 
> film: kodak
> 
> 确认：
> 
> - Kodak Gear 页面仍然能正确显示 Published Work。
> - 行为与修改前一致。
> 
> 
> Test 2：带二级分类
> 
> film: kodak ::: Gold 200
> 
> 确认：
> 
> - 正确匹配 Kodak Gear。
> - Published Work 中进入 Gold 200。
> - 不会创建 `kodak ::: Gold 200` 这样的 Gear。
> - Article / Photo 页面上的 Gear link 仍然指向 Kodak Gear。
> 
> 
> Test 3：同一分类多个作品
> 
> kodak ::: Gold 200
> kodak ::: Gold 200
> kodak ::: Gold 200
> 
> 确认：
> 
> 只产生一个：
> 
> #### Gold 200
> 
> 下面有多个 Published Work。
> 
> 
> Test 4：多个分类
> 
> kodak ::: Gold 200
> kodak ::: Portra 400
> kodak ::: Tri-X 400
> 
> 确认生成：
> 
> #### Gold 200
> 
> ...
> 
> #### Portra 400
> 
> ...
> 
> #### Tri-X 400
> 
> ...
> 
> 
> Test 5：混合普通和分类
> 
> kodak
> kodak ::: Gold 200
> kodak ::: Portra 400
> 
> 确认：
> 
> ### Published Work
> 
> 普通作品……
> 
> #### Gold 200
> 
> ……
> 
> #### Portra 400
> 
> ……
> 
> 不要产生：
> 
> #### Other
> 
> 或：
> 
> #### Unclassified
> 
> 
> Test 6：Article + Photo Work
> 
> 确认普通 Article 和 Photo Work 都能正确进入对应二级分类。
> 
> 
> Test 7：旧文章
> 
> 确认现有没有 `:::` 的文章全部保持正常。
> 
> 
> Test 8：camera / lens
> 
> 除了 film 之外，也测试：
> 
> camera: canon ::: EOS 5D
> 
> lens: zeiss ::: Planar 50mm F1.4
> 
> 确认 camera、lens、film 三个字段的行为完全一致。
> 
> 
> 【十四、排序】
> 
> Published Work 的现有 newest-first 排序必须保留。
> 
> 对于：
> 
> #### Gold 200
> 
> 下面的作品按照日期 newest-first。
> 
> 不同二级分类之间不要求按照日期排序，分类顺序可以采用首次出现顺序或当前实现能够稳定保持的顺序。
> 
> 重点是：
> 
> 同一分类内部必须保持现有 newest-first。
> 
> 
> 【十五、最终验证】
> 
> 完成后请检查：
> 
> - Article Publisher 可以正常发布。
> - Photo Publisher 可以正常发布。
> - Gear Published Work 正确进行二级分类。
> - 普通 Gear metadata 不受影响。
> - Article metadata 回链不受影响。
> - Photo metadata 回链不受影响。
> - Published Work 日期排序仍然 newest-first。
> - 同一个二级分类不会产生重复标题。
> - 普通作品仍然位于 Published Work 顶层。
> - 不会自动产生 Other / Unclassified。
> - 手工 Published Work 内容没有被删除。
> - 没有创建新的 category hierarchy。
> - 没有创建数据库或额外 runtime dependency。
> - 没有修改 homepage manual blocks。
> - 没有修改旧 portfolio 文件。
> - site-rules.md 已更新。
> - Article Publisher Skill 已更新。
> - Photo Publisher Skill 已更新。
> - repository skills 已同步到 installed skills。
> - `diff -rq` 验证通过。
> 
> 
> 【十六、最小改动原则】
> 
> 这是一个小功能，请严格采用最小改动原则。
> 
> 不要重构整个发布系统。
> 
> 不要顺便修改网站其他部分。
> 
> 不要改变现有 Gear 页面视觉设计。
> 
> 不要改变现有 metadata 字段。
> 
> 不要增加新的数据存储机制。
> 
> 核心只是：
> 
> 读取 metadata
> → 如果存在 `:::`，拆分为 Gear + Sub Gear
> → 用 Gear 左侧部分进行现有 Gear 匹配
> → 按 Sub Gear 分组 Published Work
> → 没有 `:::` 的作品继续放在顶层
> → 保持现有链接、排序和手工内容机制。
> 
> 完成后请向我汇报：
> 
> 1. 修改了哪些文件；
> 2. 具体修改了什么；
> 3. `:::` 的解析方式；
> 4. Article 和 Photo 是否共用同一套逻辑；
> 5. 是否保持完全向后兼容；
> 6. 实际测试了哪些情况；
> 7. `diff -rq` 是否通过；
> 8. 是否有任何现有数据需要我手工修改。
> 
> 如果实现过程中发现当前代码的 Published Work 自动生成机制与以上描述存在差异，请先遵循现有代码结构，采用最小修改方式实现，不要擅自重构。
