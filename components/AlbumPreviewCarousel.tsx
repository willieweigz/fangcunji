"use client";

import Image from "next/image";
import Link from "next/link";
import { useCallback, useEffect, useRef, useState } from "react";

export type AlbumPreviewSlide = {
  number: string;
  title: string;
  image: string;
};

export default function AlbumPreviewCarousel({
  albumTitle,
  slug,
  slides,
}: {
  albumTitle: string;
  slug: string;
  slides: AlbumPreviewSlide[];
}) {
  const [current, setCurrent] = useState(0);
  const [hovered, setHovered] = useState(false);
  const [interacting, setInteracting] = useState(false);
  const [inView, setInView] = useState(true);
  const [pageVisible, setPageVisible] = useState(true);
  const rootRef = useRef<HTMLDivElement>(null);
  const touchRef = useRef<{ x: number; y: number } | undefined>(undefined);
  const draggedRef = useRef(false);

  const move = useCallback((delta: number) => {
    setCurrent((value) => (value + delta + slides.length) % slides.length);
  }, [slides.length]);

  useEffect(() => {
    const root = rootRef.current;
    if (!root) return;
    const observer = new IntersectionObserver(([entry]) => setInView(entry.isIntersecting), { threshold: 0.25 });
    observer.observe(root);
    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    const onVisibilityChange = () => setPageVisible(!document.hidden);
    onVisibilityChange();
    document.addEventListener("visibilitychange", onVisibilityChange);
    return () => document.removeEventListener("visibilitychange", onVisibilityChange);
  }, []);

  useEffect(() => {
    if (slides.length < 2 || hovered || interacting || !inView || !pageVisible) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const timer = window.setInterval(() => move(1), 7000);
    return () => window.clearInterval(timer);
  }, [hovered, inView, interacting, move, pageVisible, slides.length]);

  useEffect(() => {
    if (slides.length < 2) return;
    const nextImage = new window.Image();
    nextImage.src = slides[(current + 1) % slides.length].image;
  }, [current, slides]);

  if (slides.length === 0) return null;
  const slide = slides[current];

  function onPointerDown(event: React.PointerEvent<HTMLDivElement>) {
    if (event.pointerType !== "touch") return;
    event.currentTarget.setPointerCapture(event.pointerId);
    touchRef.current = { x: event.clientX, y: event.clientY };
    setInteracting(true);
  }

  function onPointerUp(event: React.PointerEvent<HTMLDivElement>) {
    const start = touchRef.current;
    if (!start) return;
    const deltaX = event.clientX - start.x;
    const deltaY = event.clientY - start.y;
    if (Math.abs(deltaX) >= 48 && Math.abs(deltaX) > Math.abs(deltaY) * 1.2) {
      draggedRef.current = true;
      move(deltaX < 0 ? 1 : -1);
      window.setTimeout(() => { draggedRef.current = false; }, 0);
    }
    touchRef.current = undefined;
    setInteracting(false);
  }

  function cancelPointer() {
    touchRef.current = undefined;
    setInteracting(false);
  }

  return (
    <div
      ref={rootRef}
      className="group/carousel relative min-h-[280px] touch-pan-y overflow-hidden bg-[#182c2b] md:min-h-[470px]"
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      onPointerDown={onPointerDown}
      onPointerUp={onPointerUp}
      onPointerCancel={cancelPointer}
      aria-roledescription="轮播图"
      aria-label={`${albumTitle}精选画面`}
    >
      <Link
        href={`/albums/${slug}/${slide.number}`}
        onClick={(event) => {
          if (draggedRef.current) event.preventDefault();
        }}
        className="absolute inset-0 block"
        aria-label={`打开第${Number(slide.number)}图 ${slide.title}`}
      >
        <div key={slide.image} className="album-carousel-reveal absolute inset-0 overflow-hidden">
          <div className="absolute inset-y-0 right-0 w-[176%] transition-transform duration-[1600ms] ease-out group-hover/carousel:scale-[1.018]">
            <Image
              src={slide.image}
              alt={`${albumTitle}第${Number(slide.number)}图 ${slide.title}`}
              fill
              priority={current === 0}
              unoptimized
              sizes="(max-width: 768px) 176vw, 115vw"
              className="object-cover object-right"
            />
          </div>
        </div>
        <div className="absolute inset-0 bg-gradient-to-t from-black/55 via-transparent to-black/10" />
      </Link>

      {slides.length > 1 && (
        <>
          <button type="button" onClick={() => move(-1)} className="absolute left-3 top-1/2 z-10 flex h-10 w-10 -translate-y-1/2 items-center justify-center border border-white/25 bg-[#162725]/55 text-2xl text-white/90 backdrop-blur-sm transition hover:bg-[#162725]/80 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white" aria-label="上一张精选画面">‹</button>
          <button type="button" onClick={() => move(1)} className="absolute right-3 top-1/2 z-10 flex h-10 w-10 -translate-y-1/2 items-center justify-center border border-white/25 bg-[#162725]/55 text-2xl text-white/90 backdrop-blur-sm transition hover:bg-[#162725]/80 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white" aria-label="下一张精选画面">›</button>
        </>
      )}

      <div className="pointer-events-none absolute inset-x-0 bottom-0 z-10 flex items-end justify-between gap-4 p-4 text-white">
        <div>
          <p className="text-[10px] tracking-[0.22em] text-white/62">册中一页</p>
          <p className="mt-1 font-serif-cn text-sm tracking-[0.08em]">第 {Number(slide.number)} 图 · {slide.title}</p>
        </div>
        <div className="flex items-center gap-2" aria-hidden="true">
          {slides.map((item, index) => (
            <span key={item.number} className={`h-px transition-all duration-500 ${index === current ? "w-7 bg-white" : "w-3 bg-white/38"}`} />
          ))}
          <span className="ml-1 font-mono text-[10px] text-white/65">{current + 1}/{slides.length}</span>
        </div>
      </div>
    </div>
  );
}
