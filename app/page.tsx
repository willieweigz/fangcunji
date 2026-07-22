import Link from "next/link";
import { getAllSets, getYears } from "@/lib/stamps";

// "观复斋"白文印：取《道德经》"万物并作，吾以观复"，作为总站的斋号钤印
// 缩小为手卷末尾的落款尺寸，放在副标题行右端，不与主标题争视觉重心
function GuanFuSeal() {
  return (
    <svg
      viewBox="0 0 96 96"
      className="h-8 w-8 -rotate-3 opacity-90"
      aria-label="观复斋印"
    >
      <rect x="3" y="3" width="90" height="90" rx="7" fill="#b23a2a" />
      <rect
        x="9"
        y="9"
        width="78"
        height="78"
        rx="4"
        fill="none"
        stroke="#fbf7ec"
        strokeWidth="1.4"
        opacity="0.4"
      />
      {/* 三字两列印：右列自上而下"观""复"（先读），左列"斋"单字放大居中 */}
      <text
        x="67"
        y="44"
        textAnchor="middle"
        fill="#fbf7ec"
        fontSize="30"
        fontWeight="bold"
        style={{ fontFamily: '"Noto Serif SC","Songti SC","SimSun",serif' }}
      >
        观
      </text>
      <text
        x="67"
        y="80"
        textAnchor="middle"
        fill="#fbf7ec"
        fontSize="30"
        fontWeight="bold"
        style={{ fontFamily: '"Noto Serif SC","Songti SC","SimSun",serif' }}
      >
        复
      </text>
      <text
        x="29"
        y="63"
        textAnchor="middle"
        fill="#fbf7ec"
        fontSize="40"
        fontWeight="bold"
        style={{ fontFamily: '"Noto Serif SC","Songti SC","SimSun",serif' }}
      >
        斋
      </text>
    </svg>
  );
}

// 山峦剪影分隔线：呼应"纸上山河"，作标题与卡片区之间的过渡装饰
function MountainDivider() {
  return (
    <svg
      viewBox="0 0 400 28"
      preserveAspectRatio="none"
      className="mx-auto mt-6 h-6 w-64 text-ink/20"
    >
      <path
        d="M0 26 L45 10 L75 22 L120 4 L160 20 L200 8 L240 22 L280 6 L330 20 L365 12 L400 26"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

// 书签形入口：竖长方形，顶部彩色条 + 挂穗孔，内容竖排其中
function Bookmark({
  href,
  accent,
  name,
  subtitle,
  open,
  children,
}: {
  href: string;
  accent: string;
  name: string;
  subtitle: string;
  open?: boolean;
  children: React.ReactNode;
}) {
  return (
    <Link
      href={href}
      className="group flex w-60 flex-col overflow-hidden rounded-sm border border-ink/15 bg-cream shadow-sm transition-all hover:-translate-y-1 hover:shadow-lg"
    >
      {/* 书签天头：彩色条 + 挂穗孔 */}
      <div
        className="relative flex h-12 items-center justify-center"
        style={{ backgroundColor: accent }}
      >
        <span className="h-2.5 w-2.5 rounded-full border border-white/50 bg-cream/30" />
      </div>
      {/* 书签正文 */}
      <div className="flex flex-1 flex-col items-center px-6 pb-8 pt-7 text-center">
        <div
          className={`font-serif-cn text-3xl font-bold tracking-[0.2em] ${
            open ? "text-seal" : "text-ink/75"
          }`}
        >
          {name}
        </div>
        <div className="mt-2 text-sm text-faded">{subtitle}</div>
        <div className="mt-6 flex flex-1 flex-col">{children}</div>
      </div>
    </Link>
  );
}

// 总门厅：三馆入口
export default function Portal() {
  const sets = getAllSets();
  const years = getYears();
  const totalStamps = sets.reduce((n, s) => n + s.totalStamps, 0);

  return (
    // portal-root 触发 body 的"山水青"整屏背景（含页脚），见 globals.css
    <div className="portal-root flex-1">
      <main className="mx-auto w-full max-w-6xl px-4 py-8">
        <section className="py-14 text-center">
          <h1 className="font-serif-cn text-5xl font-bold tracking-[0.3em] text-ink">
            纸上山河
          </h1>
          <div className="mt-5 flex items-center justify-center gap-2">
            <p className="text-faded">收藏 · 学习 · 创作</p>
            <GuanFuSeal />
          </div>
          <MountainDivider />
        </section>

        <section className="flex flex-wrap items-stretch justify-center gap-8 pb-12">
          {/* 邮票馆（已开放） */}
          <Bookmark href="/stamps" accent="#b23a2a" open name="方寸集" subtitle="中国邮票图鉴">
            <p className="text-sm leading-relaxed text-faded">
              已收录 <span className="font-bold text-seal">{sets.length}</span> 套、
              <span className="font-bold text-seal">{totalStamps}</span> 枚邮票，
              覆盖 {years[years.length - 1]?.year}–{years[0]?.year} 年。
            </p>
            <div className="mt-auto pt-8 text-sm text-postal group-hover:underline">
              进入邮票馆 →
            </div>
          </Bookmark>

          {/* 画册馆（筹备中） */}
          <Bookmark href="/albums" accent="#2c5f8a" name="画 册" subtitle="古籍原稿 · 自制图册">
            <p className="text-sm leading-relaxed text-faded">
              清代彩绘原稿与自制工笔画册，以图辅文，读懂古典小说。
            </p>
            <div className="mt-auto pt-8 text-sm text-faded group-hover:underline">
              筹备中 →
            </div>
          </Bookmark>

          {/* 名画馆（筹备中） */}
          <Bookmark href="/gallery" accent="#c9a227" name="中外名画" subtitle="画廊 · 中西对望">
            <p className="text-sm leading-relaxed text-faded">
              从仇英、唐寅到文艺复兴与浮世绘，如逛画展般欣赏中外名作。
            </p>
            <div className="mt-auto pt-8 text-sm text-faded group-hover:underline">
              筹备中 →
            </div>
          </Bookmark>
        </section>
      </main>
    </div>
  );
}
