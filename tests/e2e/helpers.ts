import { expect, Page } from "@playwright/test";

export async function open(page: Page) {
  const failures: string[] = [];
  page.on("requestfailed", request => failures.push(request.url()));
  const target = process.env.ATELIER_SITE_URL || "/";
  const response = await page.goto(target, { waitUntil: "networkidle" });
  expect(response?.ok()).toBeTruthy();
  expect(failures).toEqual([]);
}

export async function contrast(page: Page, selector: string) {
  return page.locator(selector).evaluate(element => {
    const parse = (value: string) => value.match(/[\d.]+/g)!.slice(0, 3).map(Number);
    const luminance = (rgb: number[]) => {
      const values = rgb.map(value => {
        const channel = value / 255;
        return channel <= .04045 ? channel / 12.92 : ((channel + .055) / 1.055) ** 2.4;
      });
      return .2126 * values[0] + .7152 * values[1] + .0722 * values[2];
    };
    const style = getComputedStyle(element);
    const foreground = luminance(parse(style.color));
    const background = luminance(parse(style.backgroundColor));
    return (Math.max(foreground, background) + .05) /
      (Math.min(foreground, background) + .05);
  });
}
