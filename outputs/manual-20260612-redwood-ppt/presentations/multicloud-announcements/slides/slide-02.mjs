import { C, setup, kicker, claim, node, pill } from "./theme.mjs";

export async function slide02(presentation, ctx) {
  const slide = presentation.slides.add();
  setup(slide, ctx, { page: 2, source: "AWS doc history; Google release notes; Oracle Azure docs; OCI release notes" });
  kicker(slide, ctx, "Weekly signal");
  claim(slide, ctx, "The weekly signal is narrow, but the AWS change is strategically important.", 82, 920);

  const rows = [
    ["AWS", "10 Jun 2026", "Oracle Database@AWS supports Autonomous Database Serverless.", "High", C.red],
    ["Oracle", "9 Jun 2026", "OCI Generative AI adds import support for a Whisper-compatible model.", "Adjacent", C.amber],
    ["Google Cloud", "6-12 Jun", "No new dated Oracle Database@Google Cloud item found in official release notes.", "Watch", C.teal],
    ["Azure", "6-12 Jun", "No new official Oracle Database@Azure item found inside the week.", "Steady", C.blue],
  ];
  const x = 72;
  const y = 220;
  const widths = [150, 145, 610, 145];
  ["Provider", "Date", "Official update", "Signal"].forEach((h, i) => {
    node(slide, ctx, x + widths.slice(0, i).reduce((a, b) => a + b, 0), y, widths[i], 48, h, "", {
      fill: C.warm,
      titleSize: 13,
      bodySize: 1,
    });
  });
  rows.forEach((r, idx) => {
    const yy = y + 54 + idx * 78;
    node(slide, ctx, x, yy, widths[0], 68, r[0], "", { fill: C.white, bar: r[4], titleSize: 15 });
    node(slide, ctx, x + widths[0], yy, widths[1], 68, r[1], "", { fill: C.white, titleSize: 14 });
    node(slide, ctx, x + widths[0] + widths[1], yy, widths[2], 68, r[2], "", {
      fill: C.white,
      titleSize: 14,
      bodySize: 1,
    });
    pill(slide, ctx, x + widths[0] + widths[1] + widths[2] + 24, yy + 22, r[3], {
      w: 86,
      fill: idx === 0 ? "#f6ded8" : C.warm2,
      color: idx === 0 ? C.redDark : C.charcoal,
    });
  });
  return slide;
}
