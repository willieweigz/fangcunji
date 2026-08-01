export interface SearchItem {
  id: string;
  title: string;
  year: number;
  issueDate: string;
  themes: string[];
  names: string[];
}

export function searchItems(items: SearchItem[], rawQuery: string): SearchItem[] {
  const query = rawQuery.trim().toLowerCase();
  if (!query) return [];

  return items.filter(
    (item) =>
      item.id.toLowerCase().includes(query) ||
      item.title.toLowerCase().includes(query) ||
      String(item.year).includes(query) ||
      item.themes.some((theme) => theme.toLowerCase().includes(query)) ||
      item.names.some((name) => name.toLowerCase().includes(query))
  );
}
