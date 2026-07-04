import Link from "next/link";
import { getPrimaryThemes } from "@/lib/stamps";

export const metadata = { title: "按主题浏览 — 方寸集" };

export default function ThemesPage() {
  const themes = getPrimaryThemes();
  return (
    <div>
      <div className="mb-6 flex flex-wrap items-baseline gap-x-4 gap-y-1">
        <h1 className="font-serif-cn text-3xl font-bold">按主题浏览</h1>
        <span className="text-sm text-faded">
          进入主题后可通过"细分浏览"查看更细的分类（如文学名著 → 封神演义）
        </span>
      </div>
      <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
        {themes.map(({ theme, count }) => (
          <Link
            key={theme}
            href={`/themes/${encodeURIComponent(theme)}`}
            className="rounded-sm border border-ink/15 bg-cream p-5 text-center shadow-sm transition-shadow hover:shadow-md"
          >
            <div className="font-serif-cn text-xl font-bold hover:text-seal">
              {theme}
            </div>
            <div className="mt-1 text-xs text-faded">{count} 套</div>
          </Link>
        ))}
      </div>
    </div>
  );
}
