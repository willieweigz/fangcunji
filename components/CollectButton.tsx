"use client";

import { useEffect, useState } from "react";

export type CollectStatus = "none" | "owned" | "wish";

const KEY = "fangcunji-collection";

export function normalizeCollection(
  value: unknown,
  validIds?: ReadonlySet<string>
): Record<string, CollectStatus> {
  if (value === null || typeof value !== "object" || Array.isArray(value)) {
    throw new Error("收藏备份的顶层必须是对象");
  }

  const result: Record<string, CollectStatus> = {};
  for (const [id, status] of Object.entries(value)) {
    if (status !== "owned" && status !== "wish") {
      throw new Error(`邮票 ${id} 的收藏状态不合法`);
    }
    if (!validIds || validIds.has(id)) result[id] = status;
  }
  return result;
}

export function loadCollection(): Record<string, CollectStatus> {
  try {
    return normalizeCollection(JSON.parse(localStorage.getItem(KEY) || "{}"));
  } catch {
    localStorage.removeItem(KEY);
    return {};
  }
}

export function saveCollection(data: Record<string, CollectStatus>) {
  localStorage.setItem(KEY, JSON.stringify(data));
}

const OPTIONS: { value: CollectStatus; label: string; activeCls: string }[] = [
  { value: "none", label: "未收藏", activeCls: "bg-faded text-white border-faded" },
  { value: "owned", label: "✓ 已收藏", activeCls: "bg-postal text-white border-postal" },
  { value: "wish", label: "♥ 心愿单", activeCls: "bg-seal text-white border-seal" },
];

export default function CollectButton({ id }: { id: string }) {
  const [status, setStatus] = useState<CollectStatus>("none");

  useEffect(() => {
    setStatus(loadCollection()[id] ?? "none");
  }, [id]);

  const select = (target: CollectStatus) => {
    const data = loadCollection();
    if (target === "none") delete data[id];
    else data[id] = target;
    saveCollection(data);
    setStatus(target);
  };

  return (
    <div className="flex items-center gap-3">
      <span className="text-sm text-faded">收藏状态（三选一）：</span>
      <div className="inline-flex overflow-hidden rounded-sm border border-ink/25">
        {OPTIONS.map((opt, i) => (
          <button
            key={opt.value}
            onClick={() => select(opt.value)}
            className={`px-4 py-2 text-sm transition-colors ${
              i > 0 ? "border-l border-ink/25" : ""
            } ${
              status === opt.value
                ? opt.activeCls
                : "bg-cream text-ink/70 hover:bg-ink/5"
            }`}
          >
            {opt.label}
          </button>
        ))}
      </div>
    </div>
  );
}
