"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { imageUrl } from "@/lib/image-url";

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
  const [zoom, setZoom] = useState(1);
  const viewportRef = useRef<HTMLDivElement>(null);
  const dragRef = useRef<{ x: number; y: number; left: number; top: number } | undefined>(undefined);
  const swipeRef = useRef<{ x: number; y: number } | undefined>(undefined);
  const viewable = stamps.filter((s) => s.hasImage);

  const move = useCallback(
    (delta: number) => {
      setZoom(1);
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

  function changeZoom(next: number) {
    setZoom(Math.min(4, Math.max(1, next)));
  }

  function startDrag(event: React.PointerEvent<HTMLDivElement>) {
    const viewport = viewportRef.current;
    if (!viewport) return;
    viewport.setPointerCapture(event.pointerId);
    if (zoom === 1) {
      swipeRef.current = { x: event.clientX, y: event.clientY };
      return;
    }
    dragRef.current = { x: event.clientX, y: event.clientY, left: viewport.scrollLeft, top: viewport.scrollTop };
  }

  function drag(event: React.PointerEvent<HTMLDivElement>) {
    const viewport = viewportRef.current;
    const start = dragRef.current;
    if (!viewport || !start) return;
    viewport.scrollLeft = start.left - (event.clientX - start.x);
    viewport.scrollTop = start.top - (event.clientY - start.y);
  }

  function stopDrag(event: React.PointerEvent<HTMLDivElement>) {
    const swipe = swipeRef.current;
    if (swipe && zoom === 1) {
      const deltaX = event.clientX - swipe.x;
      const deltaY = event.clientY - swipe.y;
      if (Math.abs(deltaX) >= 60 && Math.abs(deltaX) > Math.abs(deltaY) * 1.25) {
        if (deltaX < 0) move(1);
        if (deltaX > 0) move(-1);
      }
    }
    swipeRef.current = undefined;
    dragRef.current = undefined;
  }

  function cancelDrag() {
    swipeRef.current = undefined;
    dragRef.current = undefined;
  }

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
                onClick={() => { setZoom(1); setCurrent(viewable.indexOf(stamp)); }}
                title="点击查看大图"
                className="flex aspect-square w-full cursor-zoom-in items-center justify-center overflow-hidden border border-dashed border-faded/40 p-2"
              >
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img
                  src={imageUrl(stamp.image)}
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
          className="fixed inset-0 z-50 flex flex-col bg-black/90 text-white"
          role="dialog"
          aria-modal="true"
          aria-label={`${title} 邮票大图`}
        >
          <div onClick={(e) => e.stopPropagation()} className="flex min-h-14 items-center justify-between gap-3 border-b border-white/15 px-3 md:px-5">
            <p className="min-w-0 truncate text-sm text-white/85">
              {active.format ?? `(${totalStamps}-${active.sn})`} {active.name}
              {active.denomination && ` · ${active.denomination}`}
              <span className="ml-3 text-white/55">{current! + 1} / {viewable.length}</span>
            </p>
            <div className="flex shrink-0 items-center gap-1.5 text-xs">
              <button type="button" onClick={() => changeZoom(zoom - 0.5)} disabled={zoom <= 1} className="h-9 min-w-9 border border-white/20 px-2 disabled:opacity-30" aria-label="缩小">−</button>
              <button type="button" onClick={() => changeZoom(zoom === 1 ? 2 : 1)} className="h-9 min-w-16 border border-white/20 px-2">{zoom === 1 ? "放大" : `${zoom.toFixed(1)}×`}</button>
              <button type="button" onClick={() => changeZoom(zoom + 0.5)} disabled={zoom >= 4} className="h-9 min-w-9 border border-white/20 px-2 disabled:opacity-30" aria-label="放大">＋</button>
              <button type="button" onClick={() => setCurrent(null)} className="ml-1 h-9 border border-white/20 px-3 hover:bg-white/10">关闭</button>
            </div>
          </div>

          <div ref={viewportRef} className={`touch-none flex-1 overflow-auto ${zoom > 1 ? "cursor-grab active:cursor-grabbing" : ""}`} onPointerDown={startDrag} onPointerMove={drag} onPointerUp={stopDrag} onPointerCancel={cancelDrag}>
            <div className="flex min-h-full min-w-full items-center justify-center p-4 md:p-8" style={{ width: `${zoom * 100}%`, height: `${zoom * 100}%` }}>
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src={imageUrl(active.image)}
                alt={`${title} ${active.name}`}
                draggable={false}
                onClick={(e) => e.stopPropagation()}
                onDoubleClick={() => changeZoom(zoom === 1 ? 2 : 1)}
                className="max-h-full max-w-full select-none object-contain shadow-2xl"
              />
            </div>
          </div>

          <div onClick={(e) => e.stopPropagation()} className="flex min-h-12 items-center justify-center border-t border-white/15 px-4 text-center text-xs text-white/50">
            <span className="hidden sm:inline">键盘 ← → 或两侧按钮切换 · 双击缩放 · 放大后拖动 · Esc 关闭</span>
            <span className="sm:hidden">左右滑动切换 · 放大后拖动</span>
          </div>

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
        </div>
      )}
    </>
  );
}
