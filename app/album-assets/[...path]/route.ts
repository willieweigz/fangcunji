import { readFile } from "node:fs/promises";
import path from "node:path";
import { NextResponse } from "next/server";

const CDN_BASE = process.env.ALBUM_IMAGE_CDN_BASE ?? "https://cdn.jsdelivr.net/gh/willieweigz/fangcunji-images@main/images/albums";

export async function GET(_request: Request, { params }: { params: Promise<{ path: string[] }> }) {
  const { path: parts } = await params;
  if (!parts.length || parts.some((part) => !/^[a-z0-9.-]+$/.test(part))) {
    return new NextResponse("Not found", { status: 404 });
  }

  if (process.env.NODE_ENV === "development") {
    const root = path.resolve(process.cwd(), "image-store", "images", "albums");
    const localPath = path.resolve(root, ...parts);
    if (localPath.startsWith(`${root}${path.sep}`)) {
      try {
        const body = await readFile(localPath);
        return new NextResponse(body, { headers: { "Content-Type": "image/webp", "Cache-Control": "no-store" } });
      } catch {
        // 本地没有图片时，继续回退到独立图片仓库。
      }
    }
  }

  return NextResponse.redirect(`${CDN_BASE}/${parts.map(encodeURIComponent).join("/")}`, 307);
}
