// 图片实际托管在 GitHub（经 jsDelivr 加速），不再随 Vercel 构建打包，
// 避免 public/ 里几千张图把构建容器磁盘写满（2026-08 曾因此 ENOSPC 构建失败）。
// jsDelivr 对 @main 分支内容有缓存（通常几小时到一天量级），新增图片上线后
// 可能有短暂延迟，紧急时可用 https://www.jsdelivr.com/tools/purge 手动刷新。
// 不依赖 fs/path，客户端组件（"use client"）也能安全引入。
const IMAGE_CDN_BASE =
  "https://cdn.jsdelivr.net/gh/willieweigz/fangcunji@main/image-store";

export function imageUrl(image: string): string {
  return `${IMAGE_CDN_BASE}${image}`;
}
