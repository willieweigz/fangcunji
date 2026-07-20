import { getAllSets } from "@/lib/stamps";

// 全站搜索索引，构建时静态生成。顶栏搜索框聚焦时才加载，避免每个页面都内嵌 ~300KB 数据
export const dynamic = "force-static";

export async function GET() {
  const items = getAllSets().map((s) => ({
    id: s.id,
    title: s.title,
    year: s.year,
    issueDate: s.issueDate,
    themes: s.themes,
    names: s.stamps.map((st) => st.name),
  }));
  return Response.json(items);
}
