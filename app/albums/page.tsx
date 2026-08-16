import Link from "next/link";
import AlbumPreviewCarousel from "@/components/AlbumPreviewCarousel";
import { getAlbums } from "@/lib/albums";

export const metadata = {
  title: "画册馆 — 纸上山河",
  description: "收录中国有趣的古代图册，从原作出发，逐册阅读。",
};

export default function AlbumsPage() {
  const albums = getAlbums();
  return (
    <main className="albums-root flex-1">
      <section className="album-cloth border-b border-white/10 text-[#f3eedf]">
        <div className="mx-auto grid max-w-6xl gap-10 px-5 py-14 md:grid-cols-[1fr_auto] md:items-end md:py-20">
          <div className="album-reveal">
            <p className="text-xs tracking-[0.34em] text-white/55">纸上山河 · 第二馆</p>
            <h1 className="mt-5 font-serif-cn text-5xl font-bold tracking-[0.2em] md:text-7xl">画册馆</h1>
            <p className="mt-6 max-w-2xl font-serif-cn text-base leading-8 text-white/76 md:text-lg">
              这里收录成套、有故事、值得从第一页翻到最后一页的中国古代图册。它们不只是单幅图像，也是一册可以慢慢读完的纸上故事。
            </p>
          </div>
          <div className="hidden border-l border-white/20 pl-7 text-right md:block">
            <p className="font-serif-cn text-4xl">壹</p>
            <p className="mt-1 text-xs tracking-[0.25em] text-white/48">已收一册</p>
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-5 py-12 md:py-16">
        <div className="mb-7 flex items-end justify-between border-b border-[#2c5f8a]/20 pb-4">
          <div><p className="text-xs tracking-[0.28em] text-[#2c5f8a]">馆藏目录</p><h2 className="mt-2 font-serif-cn text-2xl font-bold">从第一册开始</h2></div>
          <span className="text-xs text-faded">陆续增补</span>
        </div>
        <div className="grid gap-8">
          {albums.map((album) => (
            <article key={album.slug} className="album-paper group grid overflow-hidden border border-ink/15 shadow-[0_20px_70px_rgba(50,42,31,0.10)] md:grid-cols-[minmax(0,1.35fr)_minmax(300px,0.65fr)]">
              <AlbumPreviewCarousel
                albumTitle={album.title}
                slug={album.slug}
                slides={(album.featuredEntries ?? album.entries.slice(0, 5).map((entry) => entry.number))
                  .map((number) => album.entries.find((entry) => entry.number === number))
                  .filter((entry): entry is (typeof album.entries)[number] => Boolean(entry))}
              />
              <div className="relative flex flex-col justify-center px-7 py-9 md:px-10">
                <div className="absolute bottom-6 right-6 select-none font-serif-cn text-8xl text-[#2c5f8a]/[0.055]">卅三</div>
                <p className="text-xs tracking-[0.26em] text-[#2c5f8a]">{album.category}</p>
                <h3 className="mt-4 font-serif-cn text-4xl font-bold tracking-[0.08em] md:text-5xl">{album.title}</h3>
                <p className="mt-3 text-sm text-faded">{album.creditShort}</p>
                <p className="mt-6 text-sm leading-7 text-ink/75">{album.description}</p>
                <div className="mt-8 flex items-center gap-4">
                  <Link href={`/albums/${album.slug}`} className="bg-[#2c5f8a] px-5 py-3 text-sm tracking-[0.12em] text-white transition hover:bg-[#234b6e]">打开画册</Link>
                  <span className="text-xs text-faded">人物图 {album.entries.filter((entry) => entry.kind === "plate").length} 幅 · 另有封面与结页</span>
                </div>
              </div>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}
