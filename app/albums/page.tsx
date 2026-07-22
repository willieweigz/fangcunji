import Link from "next/link";

export const metadata = { title: "画册 — 筹备中" };

// 画册馆占位页：书籍翻页风格待启动后实现
export default function AlbumsPlaceholder() {
  return (
    <main className="mx-auto flex w-full max-w-6xl flex-1 flex-col items-center justify-center px-4 py-24 text-center">
      <h1 className="font-serif-cn text-4xl font-bold tracking-[0.25em] text-ink">
        画 册
      </h1>
      <p className="mt-6 max-w-md text-sm leading-relaxed text-faded">
        书页装帧中——清代彩绘原稿与自制工笔画册，以图辅文、伴读经典，
        敬请期待。
      </p>
      <Link href="/" className="mt-10 text-sm text-seal hover:underline">
        ← 返回总馆
      </Link>
    </main>
  );
}
