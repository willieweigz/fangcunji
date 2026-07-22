import Link from "next/link";
import type { Metadata } from "next";
import HeaderSearch from "@/components/HeaderSearch";

export const metadata: Metadata = {
  title: "方寸集 — 中国邮票图鉴",
  description:
    "方寸之间见中国：按年份与主题浏览中华人民共和国邮票目录，管理个人集邮收藏。",
};

export default function StampsLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <>
      <header className="sticky top-0 z-10 border-b border-ink/15 bg-cream/90 backdrop-blur">
        <div className="mx-auto flex max-w-6xl flex-wrap items-baseline gap-x-8 gap-y-2 px-4 py-4">
          <Link
            href="/stamps"
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
            <Link href="/" className="text-faded hover:text-seal">
              ⌂ 总馆
            </Link>
          </nav>
          <HeaderSearch />
        </div>
      </header>
      <main className="mx-auto w-full max-w-6xl flex-1 px-4 py-8">
        {children}
      </main>
    </>
  );
}
