import AxeBuilder from "@axe-core/playwright";
import { expect, test } from "@playwright/test";
import { contrast, open } from "./helpers";

for (const viewport of [{ width: 360, height: 800 }, { width: 768, height: 900 },
  { width: 1280, height: 800 }]) {
  test(`has no horizontal overflow at ${viewport.width}px`, async ({ page }) => {
    await page.setViewportSize(viewport);
    await open(page);
    const dimensions = await page.evaluate(() => ({
      document: document.documentElement.scrollWidth,
      viewport: document.documentElement.clientWidth,
    }));
    expect(dimensions.document).toBeLessThanOrEqual(dimensions.viewport + 1);
    await expect(page.locator("main")).toBeVisible();
  });
}

test("passes automated accessibility checks", async ({ page }) => {
  await open(page);
  const results = await new AxeBuilder({ page }).analyze();
  expect(results.violations).toEqual([]);
  await page.keyboard.press("Tab");
  const focus = page.locator(":focus-visible");
  await expect(focus).toBeVisible();
  const outline = await focus.evaluate(element => getComputedStyle(element).outlineStyle);
  expect(outline).not.toBe("none");
});

test("supports dark, light, contrast and reduced motion", async ({ page }) => {
  await page.emulateMedia({ colorScheme: "dark" });
  await open(page);
  const dark = await page.locator("body").evaluate(element => getComputedStyle(element).backgroundColor);
  expect(await contrast(page, "body")).toBeGreaterThanOrEqual(4.5);
  expect(await contrast(page, ".primary-action")).toBeGreaterThanOrEqual(4.5);
  await page.emulateMedia({ colorScheme: "light", reducedMotion: "reduce" });
  await page.reload({ waitUntil: "networkidle" });
  const light = await page.locator("body").evaluate(element => getComputedStyle(element).backgroundColor);
  expect(light).not.toBe(dark);
  const durations = await page.evaluate(() => document.getAnimations()
    .map(animation => Number(animation.effect?.getTiming().duration) || 0));
  expect(durations.every(duration => duration <= 100)).toBeTruthy();
});
