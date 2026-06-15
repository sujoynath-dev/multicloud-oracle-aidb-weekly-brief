import fs from "node:fs";
import path from "node:path";

import playwright from "/Users/sujoynath/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.js";

const { chromium } = playwright;

const assetDir = path.join(
  process.cwd(),
  "outputs/manual-20260612-redwood-ppt/presentations/multicloud-announcements/assets",
);

fs.mkdirSync(assetDir, { recursive: true });

async function pageFor(browser, url) {
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 3 });
  await page.goto(url, { waitUntil: "domcontentloaded", timeout: 45000 }).catch(() => {});
  await page.waitForTimeout(3500);
  return page;
}

const browser = await chromium.launch({
  headless: true,
  executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
});

let page = await pageFor(browser, "https://www.oracle.com/cloud/");
await page.screenshot({
  path: path.join(assetDir, "oracle-wordmark-official.png"),
  clip: { x: 112, y: 35, width: 144, height: 26 },
  omitBackground: true,
});
await page.close();

page = await pageFor(browser, "https://cloud.google.com/");
await page.screenshot({
  path: path.join(assetDir, "google-cloud-official.png"),
  clip: { x: 16, y: 20, width: 128, height: 30 },
  omitBackground: true,
});
await page.close();

page = await pageFor(browser, "https://aws.amazon.com/");
await page.screenshot({
  path: path.join(assetDir, "aws-official.png"),
  clip: { x: 32, y: 62, width: 72, height: 50 },
  omitBackground: true,
});
await page.close();

page = await pageFor(browser, "https://azure.microsoft.com/");
await page.screenshot({
  path: path.join(assetDir, "azure-official.png"),
  clip: { x: 72, y: 0, width: 218, height: 54 },
  omitBackground: true,
});
await page.close();

await browser.close();

console.log(
  ["oracle-wordmark-official.png", "google-cloud-official.png", "aws-official.png", "azure-official.png"]
    .map((file) => path.join(assetDir, file))
    .join("\n"),
);
