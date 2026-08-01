# 方寸集 — 中国邮票图鉴网站

- 产品需求见 `PRD.md`；架构：Next.js 15 + Tailwind v4，无数据库，数据在 `data/stamps/*.json`（按年份分文件），收藏状态存 localStorage。
- **总站路由与视觉边界**：`/` 是“纸上山河”总门厅，`/stamps` 是方寸集邮票馆；修改门厅、画册馆、名画馆或路由前先读 `三馆架构说明.md`。`PRD.md` 目前主要描述邮票馆。
- **添加/修改邮票数据**：严格按照 `数据录入手册.md` 执行（含标签 SOP），禁止编造图名/面值，没把握就标 `needsReview: true`。交付前必须运行 `python scripts/check_data.py --images` 做到 0 ERROR。
- **extras 字段规则**：只填"小型张"和"小全张"（含变体统一写"小全张"），其他版式（小版张、小本票、版式二等）一律不填。
- 本地邮票图库：`新中国邮票图片全集（1949年-2026年最新）/`（项目根目录下，约24GB，已在 .gitignore 排除，绝不提交/部署）；导入图片用 `python scripts/import_year_images.py <年份>`。
- **网站用图片放在独立仓库 `willieweigz/fangcunji-images`（经 jsDelivr 读取），主仓库一张图都不放**（2026-08 图片托管方案变更，见 `PRD.md` 同名章节 + `部署上线指南.md`；起因是图片 1.4GB 把 Vercel 构建磁盘撑爆 ENOSPC）。本地 `image-store/`（已在 .gitignore）是图片仓库的检出，自带 `.git`。`lib/image-url.ts` 的 `imageUrl()` 是拼图片 URL 的唯一入口；构建时靠 `data/image-manifest.json` 判断有图/封面比例，不读图片本体。**加图后要：① `cd image-store` 提交推送图片仓库；② `python scripts/build_image_manifest.py` 重生成清单再提交主仓库。**
- 启动: `npm run dev`（端口 3000）。项目在微云同步文件夹内，npm install 很慢属正常。
- 视觉风格是"典雅集邮册风"（米色纸纹 + 印章红 #b23a2a + 邮政绿 #1f6b50），改样式时保持此基调。
- **上线部署**：已上线，线上地址 https://fangcunji.vercel.app 。push 到 GitHub 后 Vercel 自动构建（1–2 分钟）。账号/授权类步骤（注册 GitHub/Vercel、浏览器登录）必须站长本人做，AI 只做技术操作（git 命令、检查构建日志），详见 `部署上线指南.md`。
- **⚠️ 提交并推送到 GitHub（默认不做，必须站长同意或要求才执行）**：
  - **不要顺手 push**：录完数据 / 改完代码 / 打完标签后，正常收尾是"跑体检 → 写交付说明"然后**停下**。**绝不因为"完成了一项工作"就自动 `git push`**。只有站长明确说"可以 push / 推一下 / 上线 / 同步一下"时，才做提交推送这个动作。
  - 仓库位置：`G:\微云同步文件夹\邮票网站`（项目根目录本身就是 git 仓库，无需另找路径）。
  - 远程与分支：`origin` → `https://github.com/willieweigz/fangcunji.git`，分支 `main`。
  - push 前**必须先 `git status --short`** 看清楚将提交哪些文件——多 AI / 多会话共用同一文件夹，历史上出过 24GB 图库、`.workbuddy/` 缓存、`nul` 文件被误加入暂存区的情况（这些已在 .gitignore，但仍要人工核一眼）。
  - 标准动作：`git status --short` →（优先精确 add，不要无脑 `git add -A`）`git add <文件>` → `git commit -m "说明"` → `git push`。
  - push 成功后 Vercel 自动构建，1–2 分钟线上生效；不需要手动登录或在 Vercel 后台操作。
  - **push 后必须查一次公开图片仓库的下载量并报给站长**：`gh api repos/willieweigz/fangcunji-images/traffic/clones`（看 `count`/`uniques`，近14天）。图片仓库是 Public，站长在意版权曝光——**发现下载量异常上涨要主动提示，并问是否把仓库转私有**（转私有线上图会挂，是站长明确接受的取舍）。基线 2026-08-01 为 0。
