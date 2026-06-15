import fs from "node:fs/promises";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath, pathToFileURL } from "node:url";

const workspace = path.dirname(fileURLToPath(import.meta.url));
const slidesDir = path.join(workspace, "slides");
const previewDir = path.join(workspace, "preview");
const layoutDir = path.join(workspace, "layout", "final");
const outputDir = path.join(workspace, "output");
const finalPptx =
  process.argv[2] ||
  path.join(outputDir, "weekly-multicloud-announcements-and-innovations-2026-06-15-redwood.pptx");
const contactSheetPath = path.join(previewDir, "contact-sheet.png");
const defaultPresentationsSkillDir = path.join(
  process.env.HOME || "",
  ".codex/plugins/cache/openai-primary-runtime/presentations/26.614.11602/skills/presentations",
);
const presentationsSkillDir = process.env.PRESENTATIONS_SKILL_DIR || defaultPresentationsSkillDir;
const presentationsScriptsDir = process.env.PRESENTATIONS_SKILL_SCRIPTS_DIR || path.join(presentationsSkillDir, "scripts");
const artifactUtilsPath =
  process.env.ARTIFACT_TOOL_UTILS_PATH || path.join(presentationsScriptsDir, "artifact_tool_utils.mjs");
const {
  createSlideContext,
  ensureArtifactToolWorkspace,
  importArtifactTool,
  importModuleFresh,
  padSlideNumber,
  resolveSlideFunction,
  saveBlobToFile,
  slideNumberFromModuleName,
} = await import(pathToFileURL(artifactUtilsPath).href);

async function discoverSlideModules() {
  const entries = await fs.readdir(slidesDir);
  return entries
    .filter((entry) => /^slide[-_]?\d+\.mjs$/i.test(entry))
    .map((entry) => ({
      path: path.join(slidesDir, entry),
      slideNumber: slideNumberFromModuleName(entry),
    }))
    .sort((a, b) => a.slideNumber - b.slideNumber);
}

function makeContactSheet(previewPaths) {
  const scriptPath = process.env.MAKE_CONTACT_SHEET_PATH || path.join(presentationsScriptsDir, "make_contact_sheet.py");
  const python = process.env.PYTHON || "python3";
  const result = spawnSync(python, [scriptPath, "--output", contactSheetPath, ...previewPaths], {
    encoding: "utf8",
  });
  if (result.status !== 0) {
    throw new Error([result.stdout, result.stderr].filter(Boolean).join("\n"));
  }
}

async function main() {
  await ensureArtifactToolWorkspace(workspace);
  const artifact = await importArtifactTool(workspace);
  const { Presentation, PresentationFile } = artifact;
  const presentation = Presentation.create({ slideSize: { width: 1280, height: 720 } });
  const modules = await discoverSlideModules();
  if (modules.length !== 10) {
    throw new Error(`Expected 10 slide modules, found ${modules.length}`);
  }

  const records = [];
  for (const moduleInfo of modules) {
    const module = await importModuleFresh(moduleInfo.path);
    const { name: exportName, fn } = resolveSlideFunction(module, undefined, moduleInfo.slideNumber);
    const ctx = createSlideContext(artifact, {
      slideSize: { width: 1280, height: 720 },
      slideNumber: moduleInfo.slideNumber,
      outputDir,
      assetDir: path.join(workspace, "assets"),
      workspaceDir: workspace,
    });
    const before = presentation.slides.count;
    const slide = await fn(presentation, ctx);
    if (presentation.slides.count !== before + 1) {
      throw new Error(`${path.basename(moduleInfo.path)} must add exactly one slide.`);
    }
    records.push({
      slideNumber: moduleInfo.slideNumber,
      modulePath: moduleInfo.path,
      exportName,
      slide: slide || presentation.slides.getItem(presentation.slides.count - 1),
    });
  }

  await fs.mkdir(previewDir, { recursive: true });
  await fs.mkdir(layoutDir, { recursive: true });
  const previewPaths = [];
  for (let index = 0; index < records.length; index += 1) {
    const stem = `slide-${padSlideNumber(index + 1)}`;
    const previewPath = path.join(previewDir, `${stem}.png`);
    await saveBlobToFile(await presentation.export({ slide: records[index].slide, format: "png", scale: 1 }), previewPath);
    previewPaths.push(previewPath);
    await fs.writeFile(
      path.join(layoutDir, `${stem}.layout.json`),
      await (await records[index].slide.export({ format: "layout" })).text(),
      "utf8",
    );
  }

  makeContactSheet(previewPaths);
  await fs.mkdir(outputDir, { recursive: true });
  const pptx = await PresentationFile.exportPptx(presentation);
  await pptx.save(finalPptx);
  const outputStat = await fs.stat(finalPptx);
  const manifest = {
    output: finalPptx,
    outputBytes: outputStat.size,
    slideCount: presentation.slides.count,
    slideSize: { width: 1280, height: 720 },
    previewDir,
    previewPaths,
    layoutDir,
    contactSheet: contactSheetPath,
    slides: records.map((record, index) => ({
      index: index + 1,
      requestedSlideNumber: record.slideNumber,
      modulePath: record.modulePath,
      exportName: record.exportName,
    })),
  };
  await fs.writeFile(path.join(outputDir, "artifact-build-manifest.json"), `${JSON.stringify(manifest, null, 2)}\n`);
  console.log(JSON.stringify(manifest, null, 2));
}

main().catch((error) => {
  console.error(error.stack || error.message || String(error));
  process.exit(1);
});
