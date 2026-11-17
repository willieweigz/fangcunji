"use client";

import { useEffect, useRef, useState, type ImgHTMLAttributes } from "react";
import { imageUrl } from "@/lib/image-url";

type Props = Omit<ImgHTMLAttributes<HTMLImageElement>, "src" | "srcSet" | "onError"> & {
  image: string;
};

export default function StampImage(props: Props) {
  return <ImageWithFallback key={props.image} {...props} />;
}

function ImageWithFallback({ image, alt, ...props }: Props) {
  const [fallback, setFallback] = useState(false);
  const ref = useRef<HTMLImageElement>(null);

  // 服务端输出的图片可能在 React 接管之前已经加载失败。
  useEffect(() => {
    const img = ref.current;
    if (img?.complete && img.naturalWidth === 0) setFallback(true);
  }, []);

  return (
    // eslint-disable-next-line @next/next/no-img-element
    <img
      {...props}
      ref={ref}
      alt={alt}
      src={imageUrl(image, fallback)}
      onError={fallback ? undefined : () => setFallback(true)}
    />
  );
}
