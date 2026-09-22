import { defineConfig, devices } from "@playwright/test";

const external = process.env.ATELIER_SITE_URL;

export default defineConfig({
  testDir: "tests/e2e",
  outputDir: "test-results/playwright",
  reporter: [["line"], ["html", { outputFolder: "playwright-report", open: "never" }]],
  retries: process.env.CI ? 1 : 0,
  use: {
    baseURL: external || "http://127.0.0.1:4173",
    trace: "retain-on-failure",
    screenshot: "only-on-failure",
    video: "retain-on-failure",
  },
  webServer: external ? undefined : {
    command: "python -m http.server 4173 --directory tests/e2e/fixture",
    url: "http://127.0.0.1:4173",
    reuseExistingServer: !process.env.CI,
  },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
});
