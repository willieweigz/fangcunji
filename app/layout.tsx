import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "藏馆 — 邮票 · 名画 · 画册",
  description:
    "个人收藏与学习空间：方寸集邮票图鉴、中外名画、画册，三馆合一。",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="zh-CN">
      <body className="min-h-screen flex flex-col" suppressHydrationWarning>
        {children}
        <footer className="mt-16 border-t border-ink/15 bg-cream/60">
          <div className="mx-auto max-w-6xl px-4 py-6 text-xs leading-relaxed text-faded">
            <p>
              个人收藏学习交流网站，非商业用途。邮票图案版权归中国邮政及原设计者所有，画作版权归原作者所有，如有侵权请联系删除。
            </p>
            <p className="mt-1">由 <span className="font-bold text-[#2c5f8a]">力力</span> 制作维护</p>
          </div>
        </footer>
      </body>
    </html>
  );
}
