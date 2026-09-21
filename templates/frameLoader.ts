export function createFrameLoader(
  count: number,
  source: (index: number) => string,
  onReady: () => void,
) {
  const frames = new Map<number, HTMLImageElement>();

  const load = (index: number) => {
    if (index < 0 || index >= count || frames.has(index)) return;
    const image = new Image();
    image.decoding = "async";
    image.onload = onReady;
    image.src = source(index);
    frames.set(index, image);
  };

  const prime = (target: number, direction: number) => {
    load(target);
    for (let step = 1; step <= 12; step += 1) {
      load(target + step * direction);
    }
    for (let step = 1; step <= 5; step += 1) {
      load(target - step * direction);
    }
    for (const [index, image] of frames) {
      if (Math.abs(index - target) <= 28) continue;
      image.src = "";
      frames.delete(index);
    }
  };

  const clear = () => {
    for (const image of frames.values()) image.src = "";
    frames.clear();
  };

  return { clear, get: (index: number) => frames.get(index), prime };
}
