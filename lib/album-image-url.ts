// Server-side URL selection: development keeps local assets; production skips the redirect.
export const ALBUM_IMAGE_CDN_BASE = process.env.ALBUM_IMAGE_CDN_BASE ??
  "https://cdn.jsdelivr.net/gh/willieweigz/fangcunji-images@main/images/albums";

export function albumImageUrl(image: string): string {
  if (process.env.NODE_ENV === "development" || !image.startsWith("/album-assets/")) return image;
  return `${ALBUM_IMAGE_CDN_BASE.replace(/\/$/, "")}/${image.slice("/album-assets/".length)}`;
}
