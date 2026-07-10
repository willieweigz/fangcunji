import Link from "next/link";
import { notFound } from "next/navigation";
import {
  getAllSets,
  getPrimaryThemeNames,
  getThemes,
  getProvinces,
  getCountries,
  getProvinceCounts,
  getCountryCountsByContinent,
  getSetsForRegion,
  isProvince,
  isCountry,
} from "@/lib/stamps";
import StampCard from "@/components/StampCard";

// 两个"虚拟聚合"入口：不是一级主题、不进 themes.json，纯计算得出。
// sections：索引页的分组（省份不分组只有一节；国家按洲分节）
const REGION_GROUPS: Record<
  string,
  {
    subtitle: string;
    sections: () => {
      title?: string;
      items: { region: string; count: number }[];
    }[];
  }
> = {
  省份: {
    subtitle:
      "按地域浏览，含省 · 自治区 · 直辖市 · 港澳台（含标签及介绍中提及该地的邮票）",
    sections: () => [{ items: getProvinceCounts() }],
  },
  国家: {
    subtitle: "按国家浏览，含建交纪念、联合发行及介绍中提及该国的邮票",
    sections: () =>
      getCountryCountsByContinent().map(({ continent, items }) => ({
        title: continent,
        items,
      })),
  },
};

export function generateStaticParams() {
  const names = new Set<string>(getThemes().map(({ theme }) => theme));
  for (const g of Object.keys(REGION_GROUPS)) names.add(g);
  for (const p of getProvinces()) names.add(p);
  for (const c of getCountries()) names.add(c);
  return [...names].map((theme) => ({ theme }));
}

export default async function ThemePage({
  params,
}: {
  params: Promise<{ theme: string }>;
}) {
  const { theme: raw } = await params;
  const theme = decodeURIComponent(raw);

  // 情况 1：「省份」/「国家」聚合索引页
  const group = REGION_GROUPS[theme];
  if (group) {
    const sections = group.sections();
    return (
      <div>
        <div className="mb-6 flex flex-wrap items-baseline gap-x-4 gap-y-1">
          <h1 className="font-serif-cn text-3xl font-bold">{theme}</h1>
          <span className="text-sm text-faded">{group.subtitle}</span>
          <Link href="/themes" className="ml-auto text-sm text-seal">
            ← 全部主题
          </Link>
        </div>
        {sections.map(({ title, items }) => (
          <div key={title ?? "_"} className="mb-6">
            {title && (
              <h2 className="mb-3 font-serif-cn text-lg font-bold">{title}</h2>
            )}
            <div className="flex flex-wrap gap-2">
              {items.map(({ region, count }) =>
                count > 0 ? (
                  <Link
                    key={region}
                    href={`/themes/${encodeURIComponent(region)}`}
                    className="rounded-full border border-postal/40 px-3 py-1 text-sm text-postal transition-colors hover:bg-postal hover:text-white"
                  >
                    {region}（{count}）
                  </Link>
                ) : (
                  <span
                    key={region}
                    className="rounded-full border border-faded/25 px-3 py-1 text-sm text-faded/60"
                    title="暂无相关邮票，敬请期待"
                  >
                    {region}
                  </span>
                )
              )}
            </div>
          </div>
        ))}
      </div>
    );
  }

  // 情况 2：单个省/国家——themes 含名 或 标题/介绍加粗块含名（空也不 404，显示占位）
  const regionGroup = isProvince(theme) ? "省份" : isCountry(theme) ? "国家" : null;
  if (regionGroup) {
    const sets = getSetsForRegion(theme);
    return (
      <div>
        <div className="mb-6 flex items-baseline gap-4">
          <h1 className="font-serif-cn text-3xl font-bold">{theme}</h1>
          <span className="text-sm text-faded">共 {sets.length} 套</span>
          <Link
            href={`/themes/${encodeURIComponent(regionGroup)}`}
            className="ml-auto text-sm text-seal"
          >
            ← {regionGroup}
          </Link>
        </div>
        {sets.length === 0 ? (
          <p className="rounded-sm border border-dashed border-faded/40 bg-cream/50 px-4 py-10 text-center text-faded">
            该地区暂无相关邮票，敬请期待。
          </p>
        ) : (
          <div className="grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-4">
            {sets.map((set) => (
              <StampCard key={set.id} set={set} />
            ))}
          </div>
        )}
      </div>
    );
  }

  // 情况 3：普通主题（一级或二级标签），维持原有逻辑
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
