import { C, setup, kicker, claim, panel } from "./theme.mjs";

const groups = [
  [
    "OCI",
    C.red,
    [
      "Oracle Cloud Infrastructure release notes",
      "Oracle AI Vector Search overview",
      "Official Design for Oracle Redwood",
    ],
  ],
  [
    "GCP",
    C.google,
    [
      "Google Cloud Oracle Database release notes",
      "Google Cloud Oracle Database docs",
      "Google Cloud Gemini Enterprise docs",
      "Oracle Database@Google Cloud",
    ],
  ],
  [
    "AWS",
    C.aws,
    [
      "AWS Oracle Database@AWS document history",
      "AWS Oracle Database@AWS overview",
      "AWS Oracle Database@AWS how it works",
      "AWS Amazon Bedrock User Guide",
      "Oracle AI Database@AWS",
    ],
  ],
  [
    "Azure",
    C.azure,
    [
      "Oracle AI Database@Azure overview",
      "Oracle AI Database@Azure regional availability",
      "Microsoft Foundry overview",
    ],
  ],
];

function sourceGroup(slide, ctx, x, y, title, accent, topics) {
  panel(slide, ctx, x, y, 535, 178, { fill: C.white, line: C.line });
  ctx.addShape(slide, { x, y, w: 535, h: 5, fill: accent });
  ctx.addText(slide, {
    x: x + 18,
    y: y + 18,
    w: 120,
    h: 28,
    text: title,
    fontSize: 18,
    color: C.ink,
    bold: true,
  });
  ctx.addText(slide, {
    x: x + 142,
    y: y + 22,
    w: 340,
    h: 18,
    text: "Click topic names to open official sources",
    fontSize: 10,
    color: C.muted,
  });
  topics.forEach((topic, index) => {
    const yy = y + 60 + index * 23;
    ctx.addShape(slide, { x: x + 20, y: yy + 6, w: 4, h: 4, geometry: "ellipse", fill: accent });
    ctx.addText(slide, {
      x: x + 34,
      y: yy,
      w: 470,
      h: 18,
      text: topic,
      fontSize: 10.8,
      color: C.redDark,
      bold: true,
    });
  });
}

export async function slide10(presentation, ctx) {
  const slide = presentation.slides.add();
  setup(slide, ctx, { page: 10, source: "Appendix: grouped clickable official source topics" });
  kicker(slide, ctx, "Appendix");
  claim(slide, ctx, "Official source topics grouped by cloud.", 82, 820);

  groups.forEach((group, index) => {
    const col = index % 2;
    const row = Math.floor(index / 2);
    sourceGroup(slide, ctx, 64 + col * 580, 214 + row * 200, group[0], group[1], group[2]);
  });
  return slide;
}
