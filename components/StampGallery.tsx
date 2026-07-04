"use client";

import { useCallback, useEffect, useState } from "react";

interface Stamp {
  sn: number;
  name: string;
  denomination: string;
  image: string;
  format?: string;
  hasImage: boolean;
}

export default function StampGallery({
  title,
  totalStamps,
  stamps,
}: {
  title: string;
  totalStamps: number;
  stamps: Stamp[];
}) {
  const [current, setCurrent] = useState<number | null>(null);
  const viewable = stamps.filter((s) => s.hasImage);

  const move = useCallback(
    (delta: number) => {
      setCurrent((c) =>
        c === null ? c : (c + delta + viewable.length) % viewable.length
      );
    },
    [viewable.length]
  );

  useEffect(() => {
    if (current === null) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") setCurrent(null);
      if (e.key === "ArrowLeft") move(-1);
      if (e.key === "ArrowRight") move(1);
    };
    window.addEventListener("keydown", onKey);
    document.body.style.overflow = "hidden";
    return () => {
      window.removeEventListener("keydown", onKey);
      document.body.style.overflow = "";
    };
  }, [current, move]);

  const active = current !== null ? viewable[current] : null;

  return (
    <>
      <section className="mb-8 grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-4">
        {stamps.map((stamp) => (
          <figure
            key={stamp.sn}
            className="rounded-sm border border-ink/15 bg-cream p-3 shadow-sm"
          >
            {stamp.hasImage ? (
              <button
                onClick={() => setCurrent(viewable.indexOf(stamp))}
                title="点击查看大图"
                className="flex aspect-square w-full cursor-zoom-in items-center justify-center overflow-hidden border border-dashed border-faded/40 p-2"
              >
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img
                  src={stamp.image}
                  alt={`${title} ${stamp.name}`}
                  className="max-h-full max-w-full object-contain"
                  loading="lazy"
                />
              </button>
            ) : (
              <div className="flex aspect-square items-center justify-center border border-dashed border-faded/40 p-2">
                <span className="text-xs text-faded">图片待录入</span>
              </div>
            )}
            <figcaption className="mt-2 text-sm">
              <span className="text-faded">
                {stamp.format ?? `(${totalStamps}-${stamp.sn})`}
              </span>{" "}
              <span className="font-serif-cn font-bold">{stamp.name}</span>
              {stamp.denomination && (
                <span className="ml-2 text-xs text-seal">
                  {stamp.denomination}
                </span>
              )}
            </figcaption>
          </figure>
        ))}
      </section>

      {active && (
        <div
          onClick={() => setCurrent(null)}
          className="fixed inset-0 z-50 flex flex-col items-center justify-center gap-3 bg-black/85 p-6"
        >
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={active.image}
            alt={`${title} ${active.name}`}
            onClick={(e) => e.stopPropagation()}
            className="max-h-[80vh] max-w-full object-contain shadow-2xl"
          />
          <p
            onClick={(e) => e.stopPropagation()}
            className="text-center text-sm text-white/85"
          >
            {active.format ?? `(${totalStamps}-${active.sn})`} {active.name}
            {active.denomination && ` · ${active.denomination}`}
            <span className="ml-3 text-white/60">
              {current! + 1} / {viewable.length}
            </span>
            <br />
            <span className="text-xs text-white/50">
              ← → 键或两侧箭头切换 · Esc 或点击空白处关闭
            </span>
          </p>

          {viewable.length > 1 && (
            <>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  move(-1);
                }}
                aria-label="上一枚"
                className="absolute left-3 top-1/2 -translate-y-1/2 rounded-full bg-white/15 px-4 py-2 text-3xl leading-none text-white transition-colors hover:bg-white/35"
              >
                ‹
              </button>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  move(1);
                }}
                aria-label="下一枚"
                className="absolute right-3 top-1/2 -translate-y-1/2 rounded-full bg-white/15 px-4 py-2 text-3xl leading-none text-white transition-colors hover:bg-white/35"
              >
                ›
              </button>
            </>
          )}
          <button
            onClick={() => setCurrent(null)}
            aria-label="关闭"
            className="absolute right-4 top-4 rounded-full bg-white/15 px-3 py-1.5 text-lg leading-none text-white transition-colors hover:bg-white/35"
          >
            ✕
          </button>
        </div>
      )}
    </>
  );
}
