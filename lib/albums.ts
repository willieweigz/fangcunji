import albumData from "@/data/albums/sanshisan-jianke-tu.json";

export type AlbumEntryKind = "cover" | "plate" | "end";
export type AlbumEntry = { number: string; title: string; image: string; kind: AlbumEntryKind };
export type Album = Omit<typeof albumData, "entries"> & { entries: AlbumEntry[] };
type RawAlbumEntry = { number: string; title: string; kind?: AlbumEntryKind };

const albums: Album[] = [{
  ...albumData,
  entries: (albumData.entries as RawAlbumEntry[]).map((entry) => ({
    ...entry,
    kind: entry.kind ?? "plate",
    image: `/album-assets/${albumData.slug}/${entry.number}.webp`,
  })),
}];

export function getAlbums(): Album[] {
  return albums;
}

export function getAlbum(slug: string): Album | undefined {
  return albums.find((album) => album.slug === slug);
}

export function getAlbumEntry(slug: string, number: string) {
  const album = getAlbum(slug);
  if (!album) return undefined;
  const index = album.entries.findIndex((entry) => entry.number === number);
  if (index < 0) return undefined;
  return { album, entry: album.entries[index], index };
}
