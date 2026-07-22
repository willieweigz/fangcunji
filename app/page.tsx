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
      {/* 传统三字印排布：右列一字、左列两字，自右向左读"观复斋" */}
      <text
        x="69"
        y="61"
        textAnchor="middle"
        fill="#fbf7ec"
        fontSize="36"
        fontWeight="bold"
        style={{ fontFamily: '"Noto Serif SC","Songti SC","SimSun",serif' }}
      >
        观
      </text>
      <text
        x="29"
        y="43"
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
        y="79"
        textAnchor="middle"
        fill="#fbf7ec"
        fontSize="30"
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

// 总门厅：三馆入口
export default function Portal() {
  const sets = getAllSets();
  const years = getYears();
  const totalStamps = sets.reduce((n, s) => n + s.totalStamps, 0);

  return (
    <div
      className="flex-1"
      style={{
        // 门厅用"山水青"——与邮票馆的米黄纸色完全错开色相，扣"纸上山河"的山水意象
        backgroundColor: "#dde6e0",
        backgroundImage:
          "radial-gradient(rgba(31,59,47,0.05) 1px, transparent 1px)",
        backgroundSize: "16px 16px",
      }}
    >
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

        <section className="mx-auto grid max-w-5xl gap-6 pb-10 md:grid-cols-3">
          {/* 邮票馆（已开放） */}
          <Link
            href="/stamps"
            className="group border-2 border-ink/20 bg-cream p-8 text-center shadow-sm transition-shadow hover:shadow-lg"
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

          {/* 画册馆（筹备中） */}
          <Link
            href="/albums"
            className="group border-2 border-ink/20 bg-cream/60 p-8 text-center shadow-sm transition-shadow hover:shadow-lg"
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

          {/* 名画馆（筹备中） */}
          <Link
            href="/gallery"
            className="group border-2 border-ink/20 bg-cream/60 p-8 text-center shadow-sm transition-shadow hover:shadow-lg"
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
        </section>
      </main>
    </div>
  );
}
