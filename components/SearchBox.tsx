"use client";

import { useState } from "react";
import Link from "next/link";
import { searchItems, type SearchItem } from "@/lib/search";

export default function SearchBox({ items }: { items: SearchItem[] }) {
  const [q, setQ] = useState("");
  const query = q.trim().toLowerCase();
  const allResults = searchItems(items, query);
  const results = allResults.slice(0, 10);

  return (
    <div className="relative mx-auto mt-8 w-full max-w-lg">
      <input
        value={q}
        onChange={(e) => setQ(e.target.value)}
        placeholder="搜索邮票：名称 / 志号 / 主题 / 单枚图名 / 年份…"
        className="w-full rounded-sm border border-ink/25 bg-white px-4 py-3 text-sm shadow-sm outline-none placeholder:text-faded/70 focus:border-seal"
      />
      {query && (
        <ul className="absolute z-20 mt-1 max-h-96 w-full overflow-y-auto rounded-sm border border-ink/15 bg-cream shadow-lg">
          {results.length === 0 && (
            <li className="px-4 py-3 text-sm text-faded">
              没有找到匹配的邮票
            </li>
          )}
          {results.map((r) => (
            <li key={r.id} className="border-b border-ink/10 last:border-0">
              <Link
                href={`/stamps/${r.id}`}
                className="flex items-baseline gap-3 px-4 py-2.5 text-sm hover:bg-ink/5"
              >
                <span className="shrink-0 font-mono text-xs text-seal">
                  {r.id}
                </span>
                <span className="truncate font-serif-cn font-bold">
                  {r.title}
                </span>
                <span className="ml-auto shrink-0 text-xs text-faded">
                  {r.issueDate}
                </span>
              </Link>
            </li>
          ))}
          {allResults.length > 10 && (
            <li className="border-t border-ink/15">
              <Link
                href={`/search?q=${encodeURIComponent(q.trim())}`}
                className="block px-4 py-3 text-center text-sm font-bold text-seal hover:bg-ink/5"
              >
                查看全部 {allResults.length} 条结果 →
              </Link>
            </li>
          )}
        </ul>
      )}
    </div>
  );
}
