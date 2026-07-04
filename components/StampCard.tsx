import Link from "next/link";
import type { StampSet } from "@/lib/stamps";

export default function StampCard({ set }: { set: StampSet }) {
  const cover = set.stamps.find((s) => s.hasImage);
  return (
    <Link
      href={`/stamps/${set.id}`}
      className="group block rounded-sm border border-ink/15 bg-cream shadow-sm transition-shadow hover:shadow-md"
    >
      <div className="p-3">
        <div className="flex aspect-[4/3] items-center justify-center overflow-hidden border border-dashed border-faded/40 p-2">
          {cover ? (
            /* eslint-disable-next-line @next/next/no-img-element */
            <img
              src={cover.image}
              alt={`${set.title} ${cover.name}`}
              className="max-h-full max-w-full object-contain transition-transform group-hover:scale-[1.03]"
              loading="lazy"
            />
          ) : (
            <div className="px-2 text-center text-faded">
              <div className="font-serif-cn text-lg leading-snug">
                {set.title}
              </div>
              <div className="mt-1 text-xs">图片待录入</div>
            </div>
          )}
        </div>
        <div className="mt-3 flex items-baseline justify-between gap-2">
          <span className="truncate font-serif-cn font-bold group-hover:text-seal">
            {set.title}
          </span>
          <span className="shrink-0 font-mono text-xs text-seal">{set.id}</span>
        </div>
        <div className="mt-1 text-xs text-faded">
          {set.issueDate} ·{" "}
          {set.totalStamps > 0 ? `${set.totalStamps}枚` : "小型张"} · {set.type}
        </div>
      </div>
    </Link>
  );
}
