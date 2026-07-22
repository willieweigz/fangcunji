import Link from "next/link";

export const metadata = { title: "中外名画 — 筹备中" };

// 名画馆占位页：画廊展墙风格待素材到位后实现
export default function GalleryPlaceholder() {
  return (
    <main className="mx-auto flex w-full max-w-6xl flex-1 flex-col items-center justify-center px-4 py-24 text-center">
      <h1 className="font-serif-cn text-4xl font-bold tracking-[0.25em] text-ink">
        中外名画
      </h1>
      <p className="mt-6 max-w-md text-sm leading-relaxed text-faded">
        画廊正在布展中——从仇英、唐寅的笔墨，到文艺复兴与浮世绘的色彩，
        敬请期待。
      </p>
      <Link href="/" className="mt-10 text-sm text-seal hover:underline">
        ← 返回总馆
      </Link>
    </main>
  );
}
