import fs from "fs";
import path from "path";

export interface Stamp {
  sn: number;
  name: string;
  denomination: string;
  image: string;
  hasImage: boolean;
  format?: string;
  /** 列表卡片封面优先用此条目（构建时计算：小全张且长宽比适合卡片） */
  coverPreferred?: boolean;
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
let _provincesCache: string[] | null = null;
let _countriesCache: string[] | null = null;

// 读 JPEG 头部拿宽高（仅用于封面比例判断；解析失败返回 null 即回退默认封面）
function jpegSize(file: string): { w: number; h: number } | null {
  try {
    const buf = fs.readFileSync(file);
    if (buf[0] !== 0xff || buf[1] !== 0xd8) return null;
    let i = 2;
    while (i < buf.length - 9) {
      if (buf[i] !== 0xff) {
        i++;
        continue;
      }
      const marker = buf[i + 1];
      if (
        marker >= 0xc0 &&
        marker <= 0xcf &&
        marker !== 0xc4 &&
        marker !== 0xc8 &&
        marker !== 0xcc
      ) {
        return { h: buf.readUInt16BE(i + 5), w: buf.readUInt16BE(i + 7) };
      }
      i += 2 + buf.readUInt16BE(i + 2);
    }
  } catch {
    /* 解析失败按无尺寸处理 */
  }
  return null;
}

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
    // 封面优选：小全张一张图能看全套，但过于细长的（如四枚横连印）塞进 4:3
    // 卡片会缩成一条细带反而看不清，只有长宽比 ≤3:1 的小全张才标记为优选封面
    const sqz = set.stamps.find((s) => s.format === "小全张" && s.hasImage);
    if (sqz) {
      const size = jpegSize(path.join(publicDir, sqz.image));
      if (size && size.h > 0) {
        const aspect = size.w / size.h;
        if (aspect <= 3 && aspect >= 1 / 3) sqz.coverPreferred = true;
      }
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

// ---- "省份"/"国家"虚拟聚合 ----
// 这两组都不是一级主题、不进 themes.json，也不给邮票补标签，纯计算得出。
// 一套票属于某地区 = themes 含地区名 OR 标题/介绍的 **加粗块** 内含地区名（或其别名，且不踩排除词）。

// 别名：这些词出现也算该地区（如"粤港澳大湾区"题材算广东）
const REGION_ALIASES: Record<string, string[]> = {
  广东: ["大湾区", "粤港澳"],
};
// 排除：文字里出现这些更长的词时，不算对应地区（防子串误伤）
const REGION_EXCLUSIONS: Record<string, string[]> = {
  蒙古: ["内蒙古"],
  印度: ["印度尼西亚"],
};

export function getProvinces(): string[] {
  if (_provincesCache) return _provincesCache;
  _provincesCache = JSON.parse(
    fs.readFileSync(path.join(process.cwd(), "data", "provinces.json"), "utf-8")
  ) as string[];
  return _provincesCache;
}

// countries.json 按洲分组：{ "亚洲": [...], "欧洲": [...], ... }
let _countriesByContinentCache: Record<string, string[]> | null = null;

export function getCountriesByContinent(): Record<string, string[]> {
  if (_countriesByContinentCache) return _countriesByContinentCache;
  _countriesByContinentCache = JSON.parse(
    fs.readFileSync(path.join(process.cwd(), "data", "countries.json"), "utf-8")
  ) as Record<string, string[]>;
  return _countriesByContinentCache;
}

export function getCountries(): string[] {
  if (_countriesCache) return _countriesCache;
  _countriesCache = Object.values(getCountriesByContinent()).flat();
  return _countriesCache;
}

export function isProvince(name: string): boolean {
  return getProvinces().includes(name);
}

export function isCountry(name: string): boolean {
  return getCountries().includes(name);
}

// 取出介绍里所有 **...** 加粗块的内容
function boldTokens(desc: string): string[] {
  const tokens: string[] = [];
  const re = /\*\*(.+?)\*\*/g;
  let m: RegExpExecArray | null;
  while ((m = re.exec(desc)) !== null) tokens.push(m[1]);
  return tokens;
}

function matchesRegion(s: StampSet, name: string): boolean {
  if (s.themes.includes(name)) return true;
  const keys = [name, ...(REGION_ALIASES[name] ?? [])];
  const excl = REGION_EXCLUSIONS[name] ?? [];
  const texts = [s.title, ...boldTokens(s.description)];
  return texts.some(
    (t) => keys.some((k) => t.includes(k)) && !excl.some((e) => t.includes(e))
  );
}

export function getSetsForRegion(name: string): StampSet[] {
  return getAllSets().filter((s) => matchesRegion(s, name));
}

export function getProvinceCounts(): { region: string; count: number }[] {
  return getProvinces().map((region) => ({
    region,
    count: getSetsForRegion(region).length,
  }));
}

export function getCountryCounts(): { region: string; count: number }[] {
  return getCountries().map((region) => ({
    region,
    count: getSetsForRegion(region).length,
  }));
}

export function getCountryCountsByContinent(): {
  continent: string;
  items: { region: string; count: number }[];
}[] {
  return Object.entries(getCountriesByContinent()).map(
    ([continent, countries]) => ({
      continent,
      items: countries.map((region) => ({
        region,
        count: getSetsForRegion(region).length,
      })),
    })
  );
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
