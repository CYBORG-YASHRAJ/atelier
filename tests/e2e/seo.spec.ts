import { expect, test } from "@playwright/test";
import { open } from "./helpers";

test("publishes complete, truthful search and share metadata", async ({ page }) => {
  await open(page);
  const title = await page.title();
  expect(title.length).toBeGreaterThanOrEqual(15);
  expect(title.length).toBeLessThanOrEqual(65);
  const description = page.locator('meta[name="description"]');
  await expect(description).toHaveAttribute("content", /^.{70,170}$/);
  await expect(page.locator('link[rel="canonical"]')).toHaveAttribute("href", /^https?:\/\//);
  await expect(page.locator('meta[name="robots"]')).toHaveAttribute("content", /index/);
  await expect(page.locator('meta[property="og:title"]')).toHaveAttribute("content", /\S/);
  await expect(page.locator('meta[property="og:description"]')).toHaveAttribute("content", /\S/);
  await expect(page.locator('meta[property="og:image"]')).toHaveAttribute("content", /^https?:\/\//);
  await expect(page.locator('meta[name="twitter:card"]')).toHaveAttribute("content", /summary/);
  await expect(page.locator("html")).toHaveAttribute("lang", /^[a-z]{2}/);
  await expect(page.locator('meta[name="viewport"]')).toHaveCount(1);
  await expect(page.locator("h1")).toHaveCount(1);
  await expect(page.locator("main")).toHaveCount(1);
  const structured = await page.locator('script[type="application/ld+json"]').allTextContents();
  expect(structured.length).toBeGreaterThan(0);
  for (const value of structured) expect(() => JSON.parse(value)).not.toThrow();
});

test("keeps indexable content semantic", async ({ page }) => {
  await open(page);
  await expect(page.locator("nav")).toHaveCount(1);
  await expect(page.locator("footer")).toHaveCount(1);
  const emptyLinks = await page.locator("a").evaluateAll(links =>
    links.filter(link => !(link.textContent?.trim() || link.getAttribute("aria-label"))).length);
  expect(emptyLinks).toBe(0);
  const missingAlt = await page.locator("img").evaluateAll(images =>
    images.filter(image => !image.hasAttribute("alt") || !image.hasAttribute("width") ||
      !image.hasAttribute("height")).length);
  expect(missingAlt).toBe(0);
});
