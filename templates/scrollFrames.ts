import { drawCover } from "./canvasFrame";
import { createFrameLoader } from "./frameLoader";

type Options = { dir: string; count: number; pad: number };
type NetworkNavigator = Navigator & {
  connection?: { saveData?: boolean };
  deviceMemory?: number;
};

export function startFrameScrub(host: HTMLElement, canvas: HTMLCanvasElement, options: Options) {
  const device = navigator as NetworkNavigator;
  if (matchMedia("(prefers-reduced-motion: reduce)").matches ||
      device.connection?.saveData || (device.deviceMemory && device.deviceMemory <= 2)) return () => {};

  let target = 0;
  let drawn = -1;
  let direction = 1;
  let raf = 0;
  let scrollRaf = 0;
  const source = (index: number) =>
    `${options.dir}/frame_${String(index + 1).padStart(options.pad, "0")}.webp`;

  const paint = () => {
    raf = 0;
    const image = loader.get(target);
    if (!image?.complete || !image.naturalWidth || drawn === target) return;
    drawCover(canvas, image);
    drawn = target;
  };
  const schedule = () => { if (!raf) raf = requestAnimationFrame(paint); };
  const loader = createFrameLoader(options.count, source, schedule);
  const update = () => {
    const rect = host.getBoundingClientRect();
    const progress = Math.min(1, Math.max(0, -rect.top / Math.max(1, rect.height - innerHeight)));
    const next = Math.round(progress * (options.count - 1));
    direction = next >= target ? 1 : -1;
    target = next;
    loader.prime(target, direction);
    schedule();
  };
  const requestUpdate = () => {
    if (scrollRaf) return;
    scrollRaf = requestAnimationFrame(() => {
      scrollRaf = 0;
      update();
    });
  };
  const resize = new ResizeObserver(() => { drawn = -1; schedule(); });
  resize.observe(canvas);
  addEventListener("scroll", requestUpdate, { passive: true });
  loader.prime(0, 1);
  update();
  return () => {
    removeEventListener("scroll", requestUpdate);
    resize.disconnect();
    cancelAnimationFrame(raf);
    cancelAnimationFrame(scrollRaf);
    loader.clear();
  };
}
