import Link from "next/link";
import { notFound } from "next/navigation";
import AlbumViewer from "@/components/AlbumViewer";
import { getAlbumEntry, getAlbums } from "@/lib/albums";

export function generateStaticParams() {
  return getAlbums().flatMap((album) => album.entries.map((entry) => ({ slug: album.slug, number: entry.number })));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string; number: string }> }) {
  const { slug, number } = await params;
  const result = getAlbumEntry(slug, number);
  return result ? { title: `${result.entry.title}｜${result.album.title} — 画册馆` } : { title: "册页未找到" };
}

export default async function AlbumEntryPage({ params }: { params: Promise<{ slug: string; number: string }> }) {
  const { slug, number } = await params;
  const result = getAlbumEntry(slug, number);
  if (!result) notFound();
  const { album, entry, index } = result;
  const previous = album.entries[index - 1];
  const next = album.entries[index + 1];
  const previousHref = previous ? `/albums/${album.slug}/${previous.number}` : undefined;
  const nextHref = next ? `/albums/${album.slug}/${next.number}` : undefined;
  const sectionLabel = entry.kind === "cover" ? "画册封面" : entry.kind === "end" ? "群像结页" : `第 ${Number(entry.number)} 图`;

  return (
    <main className="albums-root flex-1 px-3 py-7 md:px-5 md:py-10">
      <div className="mx-auto max-w-[1580px]">
        <div className="mb-5 flex flex-wrap items-end justify-between gap-4">
          <div>
            <Link href={`/albums/${album.slug}`} className="text-xs tracking-[0.12em] text-[#2c5f8a] hover:underline">← 返回《{album.title}》目录</Link>
            <div className="mt-3 flex items-baseline gap-4"><span className="font-serif-cn text-sm text-[#a74735]">{sectionLabel}</span><h1 className="font-serif-cn text-3xl font-bold tracking-[0.08em] md:text-4xl">{entry.title}</h1></div>
          </div>
          <p className="text-xs text-faded"><span className="hidden sm:inline">点击画面进入全屏；键盘 ← → 翻页</span><span className="sm:hidden">点击画面进入全屏；左右滑动翻页</span></p>
        </div>

        <AlbumViewer image={entry.image} title={entry.title} index={index + 1} total={album.entries.length} previousHref={previousHref} nextHref={nextHref} />

        <nav className="mt-6 grid grid-cols-3 items-center border-y border-ink/12 py-4 text-sm">
          <div>{previousHref ? <Link href={previousHref} className="text-[#2c5f8a] hover:underline">← {previous.title}</Link> : null}</div>
          <Link href={`/albums/${album.slug}`} className="text-center text-faded hover:text-[#2c5f8a]">全册目录</Link>
          <div className="text-right">{nextHref ? <Link href={nextHref} className="text-[#2c5f8a] hover:underline">{next.title} →</Link> : null}</div>
        </nav>
        {entry.kind === "plate" ? (
          <div className="mt-5 flex flex-wrap gap-x-5 gap-y-1 text-[11px] leading-5 text-faded"><span>原图：据清任渭长原图等比设色</span><span>故事场景与页面文字：本站整理、重绘</span></div>
        ) : (
          <p className="mt-5 text-[11px] leading-5 text-faded">封面与群像结页：本站据画册主题及原作人物整理、重绘。</p>
        )}
      </div>
    </main>
  );
}
