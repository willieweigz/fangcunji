import { getAllSets } from "@/lib/stamps";
import CollectionView from "@/components/CollectionView";

export const metadata = { title: "我的收藏 — 方寸集" };

export default function CollectionPage() {
  const sets = getAllSets().map((s) => ({
    id: s.id,
    title: s.title,
    issueDate: s.issueDate,
    year: s.year,
    totalStamps: s.totalStamps,
  }));

  return (
    <div>
      <h1 className="mb-6 font-serif-cn text-3xl font-bold">我的收藏</h1>
      <CollectionView sets={sets} />
    </div>
  );
}
