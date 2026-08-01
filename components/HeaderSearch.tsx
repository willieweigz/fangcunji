"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { searchItems, type SearchItem } from "@/lib/search";

// 模块级缓存：索引只在第一次聚焦时拉取一次，跨页面导航复用（layout 不重挂载）
let _indexPromise: Promise<SearchItem[]> | null = null;
function loadIndex(): Promise<SearchItem[]> {
  if (!_indexPromise) {
    _indexPromise = fetch("/search-index.json")
      .then((response) => {
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return response.json();
      })
      .then((value: unknown) => {
        if (!Array.isArray(value)) throw new Error("搜索索引格式不正确");
        return value as SearchItem[];
      });
    _indexPromise.catch(() => {
      _indexPromise = null;
    });
  }
  return _indexPromise;
}

export default function HeaderSearch() {
  const pathname = usePathname();
  const [q, setQ] = useState("");
  const [open, setOpen] = useState(false);
  const [items, setItems] = useState<SearchItem[] | null>(null);
  const [loadError, setLoadError] = useState(false);

  // 邮票馆首页正文自带大搜索框，顶栏不重复显示
  if (pathname === "/stamps") return null;

  const query = q.trim().toLowerCase();
  const allResults = items ? searchItems(items, query) : [];
  const results = allResults.slice(0, 10);

  const requestIndex = () => {
    if (items) return;
    setLoadError(false);
    loadIndex()
      .then(setItems)
      .catch(() => {
        setItems(null);
        setLoadError(true);
      });
  };

  return (
    <div
      className="relative ml-auto w-40 sm:w-56"
      onFocus={() => {
        setOpen(true);
        requestIndex();
      }}
      onBlur={(e) => {
        if (!e.currentTarget.contains(e.relatedTarget)) setOpen(false);
      }}
    >
      <input
        value={q}
        onChange={(e) => {
          setQ(e.target.value);
          setOpen(true);
          requestIndex();
        }}
        placeholder="搜索志号 / 名称 / 主题…"
        className="w-full rounded-sm border border-ink/25 bg-white px-3 py-1.5 text-sm outline-none placeholder:text-faded/60 focus:border-seal"
      />
      {open && query && (
        <ul className="absolute right-0 z-20 mt-1 max-h-96 w-80 max-w-[90vw] overflow-y-auto rounded-sm border border-ink/15 bg-cream shadow-lg">
          {!items && !loadError && (
            <li className="px-4 py-3 text-sm text-faded">加载索引中…</li>
          )}
          {loadError && (
            <li className="px-4 py-3 text-sm text-faded">
              索引加载失败。
              <button
                type="button"
                onClick={requestIndex}
                className="ml-2 font-bold text-seal hover:underline"
              >
                重新加载
              </button>
            </li>
          )}
          {items && results.length === 0 && (
            <li className="px-4 py-3 text-sm text-faded">没有找到匹配的邮票</li>
          )}
          {results.map((r) => (
            <li key={r.id} className="border-b border-ink/10 last:border-0">
              <Link
                href={`/stamps/${r.id}`}
                onClick={() => {
                  setQ("");
                  setOpen(false);
                }}
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
          {items && allResults.length > 10 && (
            <li className="border-t border-ink/15">
              <Link
                href={`/search?q=${encodeURIComponent(q.trim())}`}
                onClick={() => setOpen(false)}
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
