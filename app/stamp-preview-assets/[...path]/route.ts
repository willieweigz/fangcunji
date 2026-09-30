import { readFile } from "node:fs/promises";
import path from "node:path";
import { NextResponse } from "next/server";
import { imageUrl } from "@/lib/image-url";

export async function GET(_request: Request, { params }: { params: Promise<{ path: string[] }> }) {
  const { path: parts } = await params;
  if (!parts.length || parts.some(part => part === "." || part === ".." || /[\\/\0]/.test(part))) {
    return new NextResponse("Not found", { status: 404 });
  }
  if (process.env.NODE_ENV !== "development") {
    return NextResponse.redirect(imageUrl(`/images/stamp-previews/${parts.map(encodeURIComponent).join("/")}`));
  }
  const root = path.resolve(process.cwd(), "image-store/images/stamp-previews");
  const file = path.resolve(root, ...parts);
  if (!file.startsWith(`${root}${path.sep}`) || !file.endsWith(".webp")) return new NextResponse("Not found", { status: 404 });
  try {
    const body = await readFile(file);
    return new NextResponse(body, { headers: { "Content-Type": "image/webp", "Cache-Control": "public, max-age=31536000, immutable" } });
  } catch {
    return new NextResponse("Not found", { status: 404 });
  }
}
