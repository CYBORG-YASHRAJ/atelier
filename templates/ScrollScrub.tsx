"use client";

import { useEffect, useRef } from "react";
import { startFrameScrub } from "./scrollFrames";

type Props = {
  dir: string;
  count: number;
  poster: string;
  alt: string;
  pad?: number;
  className?: string;
};

export function ScrollScrub({ dir, count, poster, alt, pad = 4, className = "" }: Props) {
  const host = useRef<HTMLDivElement>(null);
  const canvas = useRef<HTMLCanvasElement>(null);

  useEffect(() => startFrameScrub(host.current!, canvas.current!, { dir, count, pad }),
            [count, dir, pad]);

  return (
    <div ref={host} className={className}>
      <img src={poster} alt={alt} className="sticky top-0 h-screen w-full object-cover" />
      <canvas ref={canvas} aria-hidden
              className="sticky top-0 -mt-[100vh] h-screen w-full motion-reduce:hidden" />
    </div>
  );
}
