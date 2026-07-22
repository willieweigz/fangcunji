import Link from "next/link";
import { getAllSets, getYears } from "@/lib/stamps";

// 总门厅：三馆入口。馆名"藏馆"为占位名，待站长定名
export default function Portal() {
  const sets = getAllSets();
  const years = getYears();
  const totalStamps = sets.reduce((n, s) => n + s.totalStamps, 0);

  return (
    <main className="mx-auto w-full max-w-6xl flex-1 px-4 py-8">
      <section className="py-14 text-center">
        <h1 className="font-serif-cn text-5xl font-bold tracking-[0.3em] text-ink">
          藏 馆
        </h1>
        <p className="mt-5 text-faded">收藏 · 学习 · 创作</p>
      </section>

      <section className="mx-auto grid max-w-5xl gap-6 pb-10 md:grid-cols-3">
        {/* 邮票馆（已开放） */}
        <Link
          href="/stamps"
          className="group rounded-sm border border-ink/15 bg-cream p-8 text-center shadow-sm transition-shadow hover:shadow-lg"
        >
          <div className="font-serif-cn text-3xl font-bold tracking-[0.2em] text-seal">
            方寸集
          </div>
          <div className="mt-2 text-sm text-faded">中国邮票图鉴</div>
          <p className="mt-6 text-sm leading-relaxed text-faded">
            已收录 <span className="font-bold text-seal">{sets.length}</span> 套、
            <span className="font-bold text-seal">{totalStamps}</span> 枚邮票，
            覆盖 {years[years.length - 1]?.year}–{years[0]?.year} 年。
          </p>
          <div className="mt-6 text-sm text-postal group-hover:underline">
            进入邮票馆 →
          </div>
        </Link>

        {/* 名画馆（筹备中） */}
        <Link
          href="/gallery"
          className="group rounded-sm border border-ink/15 bg-cream/60 p-8 text-center shadow-sm transition-shadow hover:shadow-lg"
        >
          <div className="font-serif-cn text-3xl font-bold tracking-[0.2em] text-ink/70">
            中外名画
          </div>
          <div className="mt-2 text-sm text-faded">画廊 · 中西对望</div>
          <p className="mt-6 text-sm leading-relaxed text-faded">
            从<span className="font-serif-cn">仇英、唐寅</span>到文艺复兴与浮世绘，
            如逛画展般欣赏中外名作。
          </p>
          <div className="mt-6 text-sm text-faded group-hover:underline">
            筹备中 →
          </div>
        </Link>

        {/* 画册馆（筹备中） */}
        <Link
          href="/albums"
          className="group rounded-sm border border-ink/15 bg-cream/60 p-8 text-center shadow-sm transition-shadow hover:shadow-lg"
        >
          <div className="font-serif-cn text-3xl font-bold tracking-[0.2em] text-ink/70">
            画 册
          </div>
          <div className="mt-2 text-sm text-faded">古籍原稿 · 自制图册</div>
          <p className="mt-6 text-sm leading-relaxed text-faded">
            清代彩绘原稿与自制工笔画册，
            以图辅文，读懂古典小说。
          </p>
          <div className="mt-6 text-sm text-faded group-hover:underline">
            筹备中 →
          </div>
        </Link>
      </section>
    </main>
  );
}
