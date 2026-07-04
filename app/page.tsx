import Link from "next/link";
import { getAllSets, getPrimaryThemes, getYears } from "@/lib/stamps";
import StampCard from "@/components/StampCard";
import SearchBox from "@/components/SearchBox";

export default function Home() {
  const sets = getAllSets();
  const years = getYears();
  const themes = getPrimaryThemes();
  const totalStamps = sets.reduce((n, s) => n + s.totalStamps, 0);
  const latest = [...sets].reverse().slice(0, 8);

  return (
    <div>
      <section className="py-10 text-center">
        <h1 className="font-serif-cn text-5xl font-bold tracking-[0.25em] text-ink">
          方寸集
        </h1>
        <p className="mt-4 text-faded">方寸之间，见中国。</p>
        <p className="mx-auto mt-6 max-w-xl text-sm leading-relaxed text-faded">
          已收录邮票 <span className="font-bold text-seal">{sets.length}</span>{" "}
          套、共 <span className="font-bold text-seal">{totalStamps}</span>{" "}
          枚，覆盖 {years[years.length - 1]?.year}–{years[0]?.year} 年。
        </p>
        <SearchBox
          items={sets.map((s) => ({
            id: s.id,
            title: s.title,
            year: s.year,
            issueDate: s.issueDate,
            themes: s.themes,
            names: s.stamps.map((st) => st.name),
          }))}
        />
      </section>

      <section className="mb-10 grid gap-4 sm:grid-cols-2">
        <Link
          href="/years"
          className="rounded-sm border border-ink/15 bg-cream p-6 shadow-sm transition-shadow hover:shadow-md"
        >
          <h2 className="font-serif-cn text-xl font-bold">按年份浏览 →</h2>
          <p className="mt-2 text-sm text-faded">
            沿发行时间轴，逐年翻阅每一套邮票。
          </p>
        </Link>
        <Link
          href="/themes"
          className="rounded-sm border border-ink/15 bg-cream p-6 shadow-sm transition-shadow hover:shadow-md"
        >
          <h2 className="font-serif-cn text-xl font-bold">按主题浏览 →</h2>
          <p className="mt-2 text-sm text-faded">
            {themes
              .slice(0, 5)
              .map((t) => t.theme)
              .join(" · ")}{" "}
            等 {themes.length} 个主题。
          </p>
        </Link>
      </section>

      <section>
        <h2 className="mb-4 font-serif-cn text-2xl font-bold">最新发行</h2>
        <div className="grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-4">
          {latest.map((set) => (
            <StampCard key={set.id} set={set} />
          ))}
        </div>
      </section>
    </div>
  );
}
