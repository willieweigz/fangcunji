# 方寸集 — 中国邮票图鉴网站

- 产品需求见 `PRD.md`；架构：Next.js 15 + Tailwind v4，无数据库，数据在 `data/stamps/*.json`（按年份分文件），收藏状态存 localStorage。
- **添加/修改邮票数据**：严格按照 `数据录入手册.md` 执行（含标签 SOP），禁止编造图名/面值，没把握就标 `needsReview: true`。交付前必须运行 `python scripts/check_data.py --images` 做到 0 ERROR。
- **extras 字段规则**：只填"小型张"和"小全张"（含变体统一写"小全张"），其他版式（小版张、小本票、版式二等）一律不填。
- 本地邮票图库：`D:\BaiduNetdiskDownload\新中国邮票图片全集（1949年-2025年最新）\`；导入图片用 `python scripts/import_year_images.py <年份>`。
- 启动: `npm run dev`（端口 3000）。项目在微云同步文件夹内，npm install 很慢属正常。
- 视觉风格是"典雅集邮册风"（米色纸纹 + 印章红 #b23a2a + 邮政绿 #1f6b50），改样式时保持此基调。
- **上线部署**：还没部署（本地开发阶段，无 git 仓库）。需要部署时严格按 `部署上线指南.md` 执行——账号/授权类步骤（注册 GitHub/Vercel、浏览器登录）必须站长本人做，AI 只做技术操作（git 命令、检查构建日志）。部署后日常更新流程是"改数据→体检→git push"，Vercel 自动构建，不需要手动登录操作。
