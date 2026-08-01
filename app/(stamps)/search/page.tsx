import StampCard from "@/components/StampCard";
import { searchItems, type SearchItem } from "@/lib/search";
import { getAllSets } from "@/lib/stamps";

export const metadata = { title: "搜索邮票 — 方寸集" };

export default async function SearchPage({
  searchParams,
}: {
  searchParams: Promise<{ q?: string | string[] }>;
}) {
  const params = await searchParams;
  const rawQuery = Array.isArray(params.q) ? params.q[0] : params.q;
  const query = rawQuery?.trim() ?? "";
  const sets = getAllSets();
  const items: SearchItem[] = sets.map((set) => ({
    id: set.id,
    title: set.title,
    year: set.year,
    issueDate: set.issueDate,
    themes: set.themes,
    names: set.stamps.map((stamp) => stamp.name),
  }));
  const resultIds = new Set(searchItems(items, query).map((item) => item.id));
  const results = query ? sets.filter((set) => resultIds.has(set.id)) : [];

  return (
    <div>
      <div className="mb-8 flex flex-wrap items-baseline gap-x-4 gap-y-2">
        <h1 className="font-serif-cn text-3xl font-bold">搜索邮票</h1>
        {query && (
          <span className="text-sm text-faded">
            “{query}”共找到 {results.length} 套
          </span>
        )}
      </div>

      <form action="/search" className="mb-10 flex max-w-2xl gap-3">
        <input
          type="search"
          name="q"
          defaultValue={query}
          autoFocus
          placeholder="名称 / 志号 / 主题 / 单枚图名 / 年份"
          className="min-w-0 flex-1 rounded-sm border border-ink/25 bg-white px-4 py-3 text-sm shadow-sm outline-none placeholder:text-faded/70 focus:border-seal"
        />
        <button
          type="submit"
          className="shrink-0 rounded-sm bg-seal px-5 py-3 text-sm font-bold text-white hover:bg-seal/90"
        >
          搜索
        </button>
      </form>

      {!query ? (
        <p className="border-l-4 border-postal/40 bg-cream/70 px-5 py-4 text-sm text-faded">
          输入邮票名称、志号、年份、主题或单枚图名开始查找。
        </p>
      ) : results.length === 0 ? (
        <p className="rounded-sm border border-dashed border-faded/40 bg-cream/50 px-4 py-10 text-center text-faded">
          没有找到匹配的邮票，请尝试更短的关键词。
        </p>
      ) : (
        <div className="grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-4">
          {results.map((set) => (
            <StampCard key={set.id} set={set} />
          ))}
        </div>
      )}
    </div>
  );
}
