import previews from "@/data/stamp-preview-manifest.json";
// Used only by server-rendered list cards; do not ship the manifest to the browser.
const manifest = previews as Record<string, { preview: string }>;
export function stampPreviewImage(image: string): string {
  return manifest[image]?.preview ?? image;
}
