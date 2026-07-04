"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import {
  loadCollection,
  saveCollection,
  type CollectStatus,
} from "@/components/CollectButton";

interface SetSummary {
  id: string;
  title: string;
  issueDate: string;
  year: number;
  totalStamps: number;
}

export default function CollectionView({ sets }: { sets: SetSummary[] }) {
  const [data, setData] = useState<Record<string, CollectStatus>>({});
  const [loaded, setLoaded] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    setData(loadCollection());
    setLoaded(true);
  }, []);

  const byId = new Map(sets.map((s) => [s.id, s]));
  const owned = Object.keys(data)
    .filter((id) => data[id] === "owned" && byId.has(id))
    .map((id) => byId.get(id)!);
  const wish = Object.keys(data)
    .filter((id) => data[id] === "wish" && byId.has(id))
    .map((id) => byId.get(id)!);

  const exportData = () => {
    const blob = new Blob([JSON.stringify(data, null, 2)], {
      type: "application/json",
    });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "方寸集-收藏备份.json";
    a.click();
    URL.revokeObjectURL(a.href);
  };

  const importData = (file: File) => {
    file.text().then((text) => {
      try {
        const imported = JSON.parse(text) as Record<string, CollectStatus>;
        saveCollection(imported);
        setData(imported);
      } catch {
        alert("文件格式不正确，导入失败。");
      }
    });
  };

  if (!loaded) return null;

  const List = ({ items }: { items: SetSummary[] }) => (
    <ul className="divide-y divide-ink/10 rounded-sm border border-ink/15 bg-cream">
      {items.map((s) => (
        <li key={s.id}>
          <Link
            href={`/stamps/${s.id}`}
            className="flex items-baseline gap-4 px-4 py-3 hover:text-seal"
          >
            <span className="font-mono text-xs text-seal">{s.id}</span>
            <span className="font-serif-cn font-bold">{s.title}</span>
            <span className="ml-auto text-xs text-faded">
              {s.issueDate} · {s.totalStamps}枚
            </span>
          </Link>
        </li>
      ))}
    </ul>
  );

  return (
    <div>
      <div className="mb-8 flex flex-wrap items-center gap-4">
        <p className="text-sm text-faded">
          已收藏 <span className="font-bold text-postal">{owned.length}</span>{" "}
          套 · 心愿单 <span className="font-bold text-seal">{wish.length}</span>{" "}
          套（共收录 {sets.length} 套）
        </p>
        <div className="ml-auto flex gap-3 text-xs">
          <button
            onClick={exportData}
            className="rounded-sm border border-ink/30 px-3 py-1.5 hover:bg-ink/5"
          >
            导出备份
          </button>
          <button
            onClick={() => fileRef.current?.click()}
            className="rounded-sm border border-ink/30 px-3 py-1.5 hover:bg-ink/5"
          >
            导入备份
          </button>
          <input
            ref={fileRef}
            type="file"
            accept=".json"
            className="hidden"
            onChange={(e) => {
              const f = e.target.files?.[0];
              if (f) importData(f);
              e.target.value = "";
            }}
          />
        </div>
      </div>

      <section className="mb-10">
        <h2 className="mb-3 font-serif-cn text-xl font-bold text-postal">
          已收藏
        </h2>
        {owned.length > 0 ? (
          <List items={owned} />
        ) : (
          <p className="text-sm text-faded">
            还没有收藏记录。浏览邮票时点击"标记为已收藏"即可记录。
          </p>
        )}
      </section>

      <section>
        <h2 className="mb-3 font-serif-cn text-xl font-bold text-seal">
          心愿单
        </h2>
        {wish.length > 0 ? (
          <List items={wish} />
        ) : (
          <p className="text-sm text-faded">心愿单还是空的。</p>
        )}
      </section>

      <p className="mt-10 text-xs leading-relaxed text-faded">
        收藏记录保存在当前浏览器中（localStorage），清除浏览器数据会丢失记录，建议定期"导出备份"。
      </p>
    </div>
  );
}
