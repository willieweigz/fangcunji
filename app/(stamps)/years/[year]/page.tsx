import Link from "next/link";
import { notFound } from "next/navigation";
import { getAllSets, getYears } from "@/lib/stamps";
import StampCard from "@/components/StampCard";

export function generateStaticParams() {
  return getYears().map(({ year }) => ({ year: String(year) }));
}

export default async function YearPage({
  params,
}: {
  params: Promise<{ year: string }>;
}) {
  const { year } = await params;
  const sets = getAllSets().filter((s) => String(s.year) === year);
  if (sets.length === 0) notFound();

  return (
    <div>
      <div className="mb-6 flex items-baseline gap-4">
        <h1 className="font-serif-cn text-3xl font-bold">{year} 年</h1>
        <span className="text-sm text-faded">共 {sets.length} 套</span>
        <Link href="/years" className="ml-auto text-sm text-seal">
          ← 全部年份
        </Link>
      </div>
      <div className="grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-4">
        {sets.map((set) => (
          <StampCard key={set.id} set={set} />
        ))}
      </div>
    </div>
  );
}
