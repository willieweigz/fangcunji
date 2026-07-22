import Link from "next/link";
import { notFound } from "next/navigation";
import {
  getAllSets,
  getPrevNext,
  getPrimaryThemeNames,
  getSetById,
} from "@/lib/stamps";
import CollectButton from "@/components/CollectButton";
import StampGallery from "@/components/StampGallery";
import Highlight from "@/components/Highlight";

export function generateStaticParams() {
  return getAllSets().map((s) => ({ id: s.id }));
}

export default async function StampDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id: raw } = await params;
  const id = decodeURIComponent(raw);
  const set = getSetById(id);
  if (!set) notFound();
  const { prev, next } = getPrevNext(id);
  const primary = new Set(getPrimaryThemeNames());
  const themes = [...set.themes].sort(
    (a, b) => (primary.has(b) ? 1 : 0) - (primary.has(a) ? 1 : 0)
  );

  return (
    <div>
      <nav className="mb-6 text-sm text-faded">
        <Link href="/stamps" className="hover:text-seal">
          首页
        </Link>
        {" / "}
        <Link href={`/years/${set.year}`} className="hover:text-seal">
          {set.year} 年
        </Link>
        {" / "}
        <span>{set.title}</span>
      </nav>

      <header className="mb-8">
        <div className="flex flex-wrap items-baseline gap-x-4 gap-y-2">
          <h1 className="font-serif-cn text-3xl font-bold">{set.title}</h1>
          <span className="font-mono text-lg text-seal">{set.id}</span>
        </div>
        <div className="mt-3 flex flex-wrap gap-x-6 gap-y-1 text-sm text-faded">
          <span>{set.type}</span>
          <span>发行日期：{set.issueDate}</span>
          <span>
            {set.totalStamps > 0
              ? `全套 ${set.totalStamps} 枚`
              : "小型张发行"}
          </span>
          {set.extras.length > 0 && <span>附：{set.extras.join("、")}</span>}
          {set.designer && <span>设计：{set.designer}</span>}
          {set.quantity && <span>发行量：{set.quantity}</span>}
        </div>
        <div className="mt-3 flex flex-wrap items-center gap-2">
          {themes.map((t) =>
            primary.has(t) ? (
              <Link
                key={t}
                href={`/themes/${encodeURIComponent(t)}`}
                className="rounded-full border border-postal bg-postal px-3.5 py-1 text-sm text-white transition-colors hover:bg-postal/85"
              >
                {t}
              </Link>
            ) : (
              <Link
                key={t}
                href={`/themes/${encodeURIComponent(t)}`}
                className="rounded-full border border-[#d9a441]/70 bg-[#fff3c4] px-3 py-1 text-xs font-bold text-ink/85 transition-colors hover:border-[#b8871f] hover:bg-[#ffe8a3] hover:text-ink"
              >
                {t}
              </Link>
            )
          )}
        </div>
      </header>

      {set.description && (
        <div className="mb-8 border-l-4 border-postal/40 bg-cream/70 py-3 pl-5 pr-5">
          <p className="leading-loose text-[15px] text-ink/85">
            <Highlight text={set.description} />
          </p>
        </div>
      )}

      <StampGallery
        title={set.title}
        totalStamps={set.totalStamps}
        stamps={set.stamps}
      />

      <section className="mb-10">
        <CollectButton id={set.id} />
      </section>

      <nav className="flex justify-between border-t border-ink/15 pt-6 text-sm">
        {prev ? (
          <Link href={`/stamps/${prev.id}`} className="text-seal">
            ← {prev.id} {prev.title}
          </Link>
        ) : (
          <span />
        )}
        {next ? (
          <Link href={`/stamps/${next.id}`} className="text-right text-seal">
            {next.id} {next.title} →
          </Link>
        ) : (
          <span />
        )}
      </nav>
    </div>
  );
}
