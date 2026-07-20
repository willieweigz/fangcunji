import "./globals.css";
import Link from "next/link";
import type { Metadata } from "next";
import HeaderSearch from "@/components/HeaderSearch";

export const metadata: Metadata = {
  title: "方寸集 — 中国邮票图鉴",
  description:
    "方寸之间见中国：按年份与主题浏览中华人民共和国邮票目录，管理个人集邮收藏。",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="zh-CN">
      <body className="min-h-screen flex flex-col" suppressHydrationWarning>
        <header className="sticky top-0 z-10 border-b border-ink/15 bg-cream/90 backdrop-blur">
          <div className="mx-auto flex max-w-6xl flex-wrap items-baseline gap-x-8 gap-y-2 px-4 py-4">
            <Link
              href="/"
              className="font-serif-cn text-2xl font-bold tracking-[0.3em] text-seal"
            >
              方寸集
            </Link>
            <nav className="flex gap-6 text-sm">
              <Link href="/years" className="hover:text-seal">
                按年份
              </Link>
              <Link href="/themes" className="hover:text-seal">
                按主题
              </Link>
              <Link href="/collection" className="hover:text-seal">
                我的收藏
              </Link>
            </nav>
            <HeaderSearch />
          </div>
        </header>
        <main className="mx-auto w-full max-w-6xl flex-1 px-4 py-8">
          {children}
        </main>
        <footer className="mt-16 border-t border-ink/15 bg-cream/60">
          <div className="mx-auto max-w-6xl px-4 py-6 text-xs leading-relaxed text-faded">
            <p>
              方寸集 · 个人集邮学习交流网站，非商业用途。邮票图案版权归中国邮政及原设计者所有，如有侵权请联系删除。
            </p>
            <p className="mt-1">由 <span className="font-bold text-[#2c5f8a]">力力</span> 制作维护</p>
          </div>
        </footer>
      </body>
    </html>
  );
}
