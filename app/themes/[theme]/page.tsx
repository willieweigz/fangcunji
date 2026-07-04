import Link from "next/link";
import { notFound } from "next/navigation";
import { getAllSets, getPrimaryThemeNames, getThemes } from "@/lib/stamps";
import StampCard from "@/components/StampCard";

export function generateStaticParams() {
  return getThemes().map(({ theme }) => ({ theme }));
}

export default async function ThemePage({
  params,
}: {
  params: Promise<{ theme: string }>;
}) {
  const { theme: raw } = await params;
  const theme = decodeURIComponent(raw);
  const sets = getAllSets().filter((s) => s.themes.includes(theme));
  if (sets.length === 0) notFound();

  const primary = new Set(getPrimaryThemeNames());
  const related = new Map<string, number>();
  for (const s of sets)
    for (const t of s.themes)
      if (t !== theme) related.set(t, (related.get(t) ?? 0) + 1);
  const relatedTags = [...related.entries()].sort(
    (a, b) =>
      (primary.has(b[0]) ? 1 : 0) - (primary.has(a[0]) ? 1 : 0) || b[1] - a[1]
  );

  return (
    <div>
      <div className="mb-6 flex items-baseline gap-4">
        <h1 className="font-serif-cn text-3xl font-bold">{theme}</h1>
        <span className="text-sm text-faded">共 {sets.length} 套</span>
        <Link href="/themes" className="ml-auto text-sm text-seal">
          ← 全部主题
        </Link>
      </div>
      {relatedTags.length > 0 && (
        <div className="mb-6 flex flex-wrap items-center gap-2">
          <span className="text-sm text-faded">细分浏览：</span>
          {relatedTags.map(([t, count]) => (
            <Link
              key={t}
              href={`/themes/${encodeURIComponent(t)}`}
              className={
                primary.has(t)
                  ? "rounded-full border border-postal bg-postal px-3 py-1 text-xs text-white transition-colors hover:bg-postal/85"
                  : "rounded-full border border-postal/40 px-3 py-1 text-xs text-postal transition-colors hover:bg-postal hover:text-white"
              }
            >
              {t}（{count}）
            </Link>
          ))}
        </div>
      )}
      <div className="grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-4">
        {sets.map((set) => (
          <StampCard key={set.id} set={set} />
        ))}
      </div>
    </div>
  );
}
