import Link from "next/link";
import { getYears } from "@/lib/stamps";

export const metadata = { title: "按年份浏览 — 方寸集" };

export default function YearsPage() {
  const years = getYears();
  const decades = new Map<number, typeof years>();
  for (const y of years) {
    const d = Math.floor(y.year / 10) * 10;
    if (!decades.has(d)) decades.set(d, []);
    decades.get(d)!.push(y);
  }

  return (
    <div>
      <h1 className="mb-6 font-serif-cn text-3xl font-bold">按年份浏览</h1>
      {[...decades.entries()]
        .sort((a, b) => b[0] - a[0])
        .map(([decade, list]) => (
          <section key={decade} className="mb-8">
            <h2 className="mb-3 font-serif-cn text-xl text-faded">
              {decade} 年代
            </h2>
            <div className="grid grid-cols-3 gap-3 sm:grid-cols-4 md:grid-cols-5 lg:grid-cols-6">
              {list.map(({ year, count }) => (
                <Link
                  key={year}
                  href={`/years/${year}`}
                  className="rounded-sm border border-ink/15 bg-cream px-3 py-3 text-center shadow-sm transition-shadow hover:shadow-md hover:text-seal"
                >
                  <div className="font-serif-cn text-lg font-bold leading-tight">
                    {year}
                  </div>
                  <div className="mt-0.5 text-xs text-faded">{count} 套</div>
                </Link>
              ))}
            </div>
          </section>
        ))}
    </div>
  );
}
