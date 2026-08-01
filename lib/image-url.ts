// 图片托管在独立仓库 willieweigz/fangcunji-images（经 jsDelivr 加速读取），
// 不放进 Vercel 构建的主仓库 —— 否则几千张图（约 1.4GB）会随 git 一起被 clone，
// 把构建容器磁盘写满（2026-08 曾因此 ENOSPC 反复构建失败，教训见 PRD.md）。
// image 字段形如 /images/stamps/2026/2026-11-1.jpg，图片仓库根目录下就是 images/。
// jsDelivr 对 @main 分支内容有缓存（通常几小时到一天量级），新增图片上线后
// 可能有短暂延迟，紧急时可用 https://www.jsdelivr.com/tools/purge 手动刷新。
// 不依赖 fs/path，客户端组件（"use client"）也能安全引入。
const IMAGE_CDN_BASE =
  "https://cdn.jsdelivr.net/gh/willieweigz/fangcunji-images@main";

export function imageUrl(image: string): string {
  return `${IMAGE_CDN_BASE}${image}`;
}
