export function drawCover(canvas: HTMLCanvasElement, image: HTMLImageElement) {
  const context = canvas.getContext("2d", { alpha: true })!;
  const box = canvas.getBoundingClientRect();
  const dpr = Math.min(devicePixelRatio, 2);
  const width = Math.round(box.width * dpr);
  const height = Math.round(box.height * dpr);
  if (canvas.width !== width || canvas.height !== height) {
    canvas.width = width;
    canvas.height = height;
  }
  const scale = Math.max(width / image.naturalWidth, height / image.naturalHeight);
  const drawWidth = image.naturalWidth * scale;
  const drawHeight = image.naturalHeight * scale;
  context.clearRect(0, 0, width, height);
  context.drawImage(image, (width - drawWidth) / 2, (height - drawHeight) / 2,
                    drawWidth, drawHeight);
}
