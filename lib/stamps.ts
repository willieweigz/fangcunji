import fs from "fs";
import path from "path";

export interface Stamp {
  sn: number;
  name: string;
  denomination: string;
  image: string;
  hasImage: boolean;
}

export interface StampSet {
  id: string;
  series: string;
  type: string;
  title: string;
  issueDate: string;
  year: number;
  themes: string[];
  designer: string;
  totalStamps: number;
  extras: string[];
  description: string;
  quantity?: string;
  source?: string;
  needsReview?: boolean;
  localImageFolder?: string;
  stamps: Stamp[];
}

const dataDir = path.join(process.cwd(), "data", "stamps");
const publicDir = path.join(process.cwd(), "public");

// 模块级缓存：避免每次请求都同步读取 20+ JSON + 数千次 fs.existsSync
let _allSetsCache: StampSet[] | null = null;
let _primaryThemeNamesCache: string[] | null = null;

export function getAllSets(): StampSet[] {
  if (_allSetsCache) return _allSetsCache;
  const files = fs.readdirSync(dataDir).filter((f) => f.endsWith(".json"));
  const sets: StampSet[] = [];
  for (const f of files) {
    const arr = JSON.parse(
      fs.readFileSync(path.join(dataDir, f), "utf-8")
    ) as StampSet[];
    sets.push(...arr);
  }
  for (const set of sets) {
    for (const stamp of set.stamps) {
      stamp.hasImage = fs.existsSync(path.join(publicDir, stamp.image));
    }
  }
  _allSetsCache = sets.sort(
    (a, b) => a.issueDate.localeCompare(b.issueDate) || a.id.localeCompare(b.id)
  );
  return _allSetsCache;
}

export function getSetById(id: string): StampSet | undefined {
  return getAllSets().find((s) => s.id === id);
}

export function getYears(): { year: number; count: number }[] {
  const map = new Map<number, number>();
  for (const s of getAllSets()) map.set(s.year, (map.get(s.year) ?? 0) + 1);
  return [...map.entries()]
    .map(([year, count]) => ({ year, count }))
    .sort((a, b) => b.year - a.year);
}

export function getThemes(): { theme: string; count: number }[] {
  const map = new Map<string, number>();
  for (const s of getAllSets())
    for (const t of s.themes) map.set(t, (map.get(t) ?? 0) + 1);
  return [...map.entries()]
    .map(([theme, count]) => ({ theme, count }))
    .sort((a, b) => b.count - a.count);
}

// 一级主题（主题总览页只展示这些，顺序即展示顺序），由 data/themes.json 维护；
// 其余标签作为细分标签，通过主题页内的"细分浏览"进入
export function getPrimaryThemeNames(): string[] {
  if (_primaryThemeNamesCache) return _primaryThemeNamesCache;
  _primaryThemeNamesCache = JSON.parse(
    fs.readFileSync(path.join(process.cwd(), "data", "themes.json"), "utf-8")
  ) as string[];
  return _primaryThemeNamesCache;
}

export function getPrimaryThemes(): { theme: string; count: number }[] {
  const counts = new Map(getThemes().map((t) => [t.theme, t.count]));
  return getPrimaryThemeNames()
    .filter((t) => (counts.get(t) ?? 0) > 0)
    .map((t) => ({ theme: t, count: counts.get(t)! }));
}

export function getPrevNext(id: string): {
  prev?: StampSet;
  next?: StampSet;
} {
  const sets = getAllSets();
  const i = sets.findIndex((s) => s.id === id);
  return {
    prev: i > 0 ? sets[i - 1] : undefined,
    next: i >= 0 && i < sets.length - 1 ? sets[i + 1] : undefined,
  };
}
