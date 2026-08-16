import Link from "next/link";

export default function AlbumsLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="albums-root flex min-h-screen flex-col">
      <header className="border-b border-[#2c5f8a]/18 bg-[#eee8db]/92 backdrop-blur-sm">
        <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-5">
          <Link href="/albums" className="font-serif-cn text-xl font-bold tracking-[0.18em] text-[#234f74]">画册馆</Link>
          <nav className="flex items-center gap-5 text-sm text-faded">
            <Link href="/albums" className="hover:text-[#234f74]">馆藏</Link>
            <Link href="/" className="hover:text-[#234f74]">返回总馆</Link>
          </nav>
        </div>
      </header>
      {children}
    </div>
  );
}
