import Image from "next/image";
import Link from "next/link";
import { notFound } from "next/navigation";
import { getAlbum, getAlbums } from "@/lib/albums";

export function generateStaticParams() {
  return getAlbums().map((album) => ({ slug: album.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const album = getAlbum(slug);
  return album ? { title: `${album.title} — 画册馆`, description: album.description } : { title: "画册未找到" };
}

export default async function AlbumDetailPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const album = getAlbum(slug);
  if (!album) notFound();
  const plateCount = album.entries.filter((entry) => entry.kind === "plate").length;

  return (
    <main className="albums-root flex-1">
      <section className="album-cloth text-[#f3eedf]">
        <div className="mx-auto grid max-w-6xl gap-10 px-5 py-10 md:grid-cols-[1.05fr_0.95fr] md:items-center md:py-16">
          <div className="relative aspect-[4/3] overflow-hidden border border-white/15 shadow-2xl">
            <Image src={album.coverImage} alt={`${album.title}封面场景`} fill priority unoptimized sizes="(max-width: 768px) 100vw, 52vw" className="object-cover" />
          </div>
          <div className="album-reveal md:pl-5">
            <p className="text-xs tracking-[0.3em] text-white/55">{album.category}</p>
            <h1 className="mt-4 font-serif-cn text-5xl font-bold tracking-[0.09em] md:text-6xl">{album.title}</h1>
            <p className="mt-4 text-sm tracking-[0.15em] text-white/62">{album.period} · {album.creditShort}</p>
            <p className="mt-7 font-serif-cn text-base leading-8 text-white/78">{album.description}</p>
            <div className="mt-9 flex flex-wrap items-center gap-4">
              <Link href={`/albums/${album.slug}/${album.entries[0].number}`} className="bg-[#f3eedf] px-6 py-3 text-sm tracking-[0.14em] text-[#234f74] transition hover:bg-white">从封面开始</Link>
              <span className="text-xs text-white/52">全册 {album.entries.length} 页 · 人物图 {plateCount} 幅</span>
            </div>
          </div>
        </div>
      </section>

      <section className="mx-auto grid max-w-6xl gap-10 px-5 py-12 lg:grid-cols-[0.68fr_0.32fr] md:py-16">
        <div>
          <div className="mb-6 flex items-end justify-between border-b border-[#2c5f8a]/20 pb-4">
            <div><p className="text-xs tracking-[0.28em] text-[#2c5f8a]">全册目录</p><h2 className="mt-2 font-serif-cn text-2xl font-bold">封面 · 三十三图 · 群像结页</h2></div>
            <span className="text-xs text-faded">点击页名翻阅</span>
          </div>
          <ol className="grid border-l border-t border-ink/12 sm:grid-cols-2 lg:grid-cols-4">
            {album.entries.map((entry) => {
              const marker = entry.kind === "cover" ? "封" : entry.kind === "end" ? "终" : entry.number;
              return (
              <li key={entry.number}>
                <Link href={`/albums/${album.slug}/${entry.number}`} className={`group flex min-h-24 items-center gap-4 border-b border-r border-ink/12 px-4 py-4 transition hover:bg-[#f7f2e6] ${entry.kind === "plate" ? "bg-[#f3eedf]/60" : "bg-[#e9e0cd]/70"}`}>
                  <span className="font-serif-cn text-2xl text-[#2c5f8a]/48">{marker}</span>
                  <span className="font-serif-cn text-base font-bold tracking-[0.05em] group-hover:text-[#2c5f8a]">{entry.title}</span>
                </Link>
              </li>
              );
            })}
          </ol>
        </div>

        <aside className="space-y-6">
          <div className="album-paper border border-ink/12 p-6">
            <p className="text-xs tracking-[0.24em] text-[#a74735]">为什么收录</p>
            <p className="mt-4 text-sm leading-7 text-ink/75">《三十三剑客图》把三十三位人物与各自的奇闻收在一册之中，在晚清版画和武侠图像史中也有自己的位置，正好体现“有趣的中国古代图册”这一馆藏方向。</p>
          </div>
          <div className="border-l-2 border-[#2c5f8a]/35 pl-5 text-xs leading-6 text-faded">
            <p className="font-bold text-ink/70">来源与整理</p>
            <p className="mt-2">原作：清任熊（字渭长）绘，蔡照初刻。</p>
            <p>人物图：据任渭长原图等比设色。</p>
            <p>故事场景与页面文字：本站据古籍故事及相关评介整理、重绘。</p>
            <p className="mt-3">本馆不直接转载金庸文章全文，可通过合法电子书入口阅读或借阅。</p>
            <div className="mt-4 flex flex-col gap-1">
              <a href="https://nlb.overdrive.com/media/12857847" target="_blank" rel="noreferrer" className="text-[#2c5f8a] hover:underline">金庸《卅三剑客图》电子书 · 新加坡国家图书馆 ↗</a>
              <a href="https://www.shanghaimuseum.net/mu/frontend/pg/article/id/CI00004997" target="_blank" rel="noreferrer" className="text-[#2c5f8a] hover:underline">任熊生平与画艺 · 上海博物馆 ↗</a>
              <a href="https://www.sbksc.zcxn.com/html/zlhd/0505_167.html" target="_blank" rel="noreferrer" className="text-[#2c5f8a] hover:underline">《三十三剑客图》书影与著录 ↗</a>
            </div>
          </div>
        </aside>
      </section>
    </main>
  );
}
