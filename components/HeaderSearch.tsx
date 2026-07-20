"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import type { SearchItem } from "./SearchBox";

// 模块级缓存：索引只在第一次聚焦时拉取一次，跨页面导航复用（layout 不重挂载）
let _indexPromise: Promise<SearchItem[]> | null = null;
function loadIndex(): Promise<SearchItem[]> {
  if (!_indexPromise) {
    _indexPromise = fetch("/search-index.json")
      .then((r) => r.json())
      .catch(() => {
        _indexPromise = null; // 失败允许重试
        return [];
      });
  }
  return _indexPromise;
}

export default function HeaderSearch() {
  const pathname = usePathname();
  const [q, setQ] = useState("");
  const [open, setOpen] = useState(false);
  const [items, setItems] = useState<SearchItem[] | null>(null);

  // 首页正文自带大搜索框，顶栏不重复显示
  if (pathname === "/") return null;

  const query = q.trim().toLowerCase();
  const results =
    query && items
      ? items
          .filter(
            (it) =>
              it.id.toLowerCase().includes(query) ||
              it.title.toLowerCase().includes(query) ||
              String(it.year).includes(query) ||
              it.themes.some((t) => t.toLowerCase().includes(query)) ||
              it.names.some((n) => n.toLowerCase().includes(query))
          )
          .slice(0, 10)
      : [];

  return (
    <div
      className="relative ml-auto w-40 sm:w-56"
      onFocus={() => {
        setOpen(true);
        if (!items) loadIndex().then(setItems);
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
          if (!items) loadIndex().then(setItems);
        }}
        placeholder="搜索志号 / 名称 / 主题…"
        className="w-full rounded-sm border border-ink/25 bg-white px-3 py-1.5 text-sm outline-none placeholder:text-faded/60 focus:border-seal"
      />
      {open && query && (
        <ul className="absolute right-0 z-20 mt-1 max-h-96 w-80 max-w-[90vw] overflow-y-auto rounded-sm border border-ink/15 bg-cream shadow-lg">
          {!items && (
            <li className="px-4 py-3 text-sm text-faded">加载索引中…</li>
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
        </ul>
      )}
    </div>
  );
}
