"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useRef, useState } from "react";

type Props = {
  image: string;
  title: string;
  index: number;
  total: number;
  previousHref?: string;
  nextHref?: string;
};

export default function AlbumViewer({ image, title, index, total, previousHref, nextHref }: Props) {
  const router = useRouter();
  const [open, setOpen] = useState(false);
  const [zoom, setZoom] = useState(1);
  const viewportRef = useRef<HTMLDivElement>(null);
  const dragRef = useRef<{ x: number; y: number; left: number; top: number } | undefined>(undefined);
  const swipeRef = useRef<{ x: number; y: number } | undefined>(undefined);

  useEffect(() => {
    if (!open) return;
    const oldOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") setOpen(false);
      if (event.key === "+" || event.key === "=") setZoom((value) => Math.min(4, value + 0.5));
      if (event.key === "-") setZoom((value) => Math.max(1, value - 0.5));
    };
    window.addEventListener("keydown", onKeyDown);
    return () => {
      document.body.style.overflow = oldOverflow;
      window.removeEventListener("keydown", onKeyDown);
    };
  }, [open]);

  useEffect(() => {
    const onPageKeyDown = (event: KeyboardEvent) => {
      const target = event.target as HTMLElement | null;
      if (
        event.repeat ||
        event.altKey ||
        event.ctrlKey ||
        event.metaKey ||
        event.shiftKey ||
        target?.matches("input, textarea, select, [contenteditable='true']")
      ) {
        return;
      }

      if (event.key === "ArrowLeft" && previousHref) {
        event.preventDefault();
        router.push(previousHref);
      }
      if (event.key === "ArrowRight" && nextHref) {
        event.preventDefault();
        router.push(nextHref);
      }
    };

    window.addEventListener("keydown", onPageKeyDown);
    return () => window.removeEventListener("keydown", onPageKeyDown);
  }, [nextHref, previousHref, router]);

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
        if (deltaX < 0 && nextHref) router.push(nextHref);
        if (deltaX > 0 && previousHref) router.push(previousHref);
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
      <button type="button" onClick={() => { setZoom(1); setOpen(true); }} className="group relative block w-full cursor-zoom-in overflow-hidden border border-ink/14 bg-[#d6cfbf] text-left shadow-[0_22px_75px_rgba(31,29,24,0.14)]" aria-label={`放大查看${title}`}>
        <img src={image} alt={`${title}完整页`} width={5040} height={2160} className="block h-auto w-full" />
        <span className="absolute bottom-3 right-3 bg-black/62 px-3 py-2 text-xs tracking-[0.12em] text-white opacity-90 backdrop-blur-sm transition group-hover:bg-[#2c5f8a]">点击放大 · 可拖动查看</span>
      </button>

      {open && (
        <div className="fixed inset-0 z-[100] flex flex-col bg-[#111614]/96 text-white" role="dialog" aria-modal="true" aria-label={`${title}放大阅读`}>
          <div className="flex min-h-14 items-center justify-between gap-3 border-b border-white/12 px-3 md:px-5">
            <div className="min-w-0"><p className="truncate font-serif-cn text-sm font-bold md:text-base">{title}</p><p className="text-[11px] text-white/48">第 {index} 页 / 共 {total} 页</p></div>
            <div className="flex items-center gap-1.5 text-xs">
              <button type="button" onClick={() => changeZoom(zoom - 0.5)} disabled={zoom <= 1} className="h-9 min-w-9 border border-white/18 px-2 disabled:opacity-30" aria-label="缩小">−</button>
              <button type="button" onClick={() => changeZoom(zoom === 1 ? 2 : 1)} className="h-9 min-w-16 border border-white/18 px-2">{zoom === 1 ? "放大" : `${zoom.toFixed(1)}×`}</button>
              <button type="button" onClick={() => changeZoom(zoom + 0.5)} disabled={zoom >= 4} className="h-9 min-w-9 border border-white/18 px-2 disabled:opacity-30" aria-label="放大">＋</button>
              <button type="button" onClick={() => setOpen(false)} className="ml-1 h-9 border border-white/18 px-3 hover:bg-white/10">关闭</button>
            </div>
          </div>

          <div ref={viewportRef} className={`album-pan touch-none flex-1 overflow-auto ${zoom > 1 ? "cursor-grab active:cursor-grabbing" : ""}`} onPointerDown={startDrag} onPointerMove={drag} onPointerUp={stopDrag} onPointerCancel={cancelDrag}>
            <div className="flex min-h-full min-w-full items-center justify-center p-2 md:p-5" style={{ width: `${zoom * 100}%` }}>
              <img src={image} alt={`${title}完整页放大图`} width={5040} height={2160} draggable={false} className="block h-auto w-full max-w-none select-none" onDoubleClick={() => changeZoom(zoom === 1 ? 2 : 1)} />
            </div>
          </div>

          <div className="flex min-h-14 items-center justify-between border-t border-white/12 px-3 text-xs md:px-5">
            {previousHref ? <Link href={previousHref} onClick={() => setOpen(false)} className="px-3 py-2 hover:text-[#b8d4e8]">← 上一页</Link> : <span className="px-3 py-2 text-white/24">← 上一页</span>}
            <span className="hidden text-white/40 sm:inline">键盘 ← → 翻页 · 双击切换缩放 · 放大后拖动</span>
            <span className="text-[10px] text-white/40 sm:hidden">左右滑动翻页</span>
            {nextHref ? <Link href={nextHref} onClick={() => setOpen(false)} className="px-3 py-2 hover:text-[#b8d4e8]">下一页 →</Link> : <span className="px-3 py-2 text-white/24">下一页 →</span>}
          </div>
        </div>
      )}
    </>
  );
}
