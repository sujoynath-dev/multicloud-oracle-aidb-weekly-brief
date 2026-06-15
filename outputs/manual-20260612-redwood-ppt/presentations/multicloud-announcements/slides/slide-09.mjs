import { C, setup, kicker, claim, node, pill } from "./theme.mjs";

export async function slide09(presentation, ctx) {
  const slide = presentation.slides.add();
  setup(slide, ctx, { page: 9, source: "OCI release notes; AWS KMS/Data Guard release note; provider service docs" });
  kicker(slide, ctx, "Controls before models");
  claim(slide, ctx, "Governance, security, and DR should be designed before model routing.", 82, 980);

  const rows = [
    ["Key control", "Validate AWS KMS CMK support for Autonomous AI Database on Oracle Database@AWS cross-region Data Guard.", "Regulated AWS-resident DR"],
    ["Data movement", "Classify whether each dataset stays in Oracle, is replicated, summarized, embedded, or exposed through an API.", "Prevents uncontrolled AI data drift"],
    ["Identity", "Keep Oracle database entitlements authoritative; map provider IAM/RBAC to app and tool access.", "Consistent least privilege"],
    ["Operations", "Use provider observability for cloud-side services and Oracle controls for database health, backups, and patching.", "Clear ownership boundary"],
  ];
  const x = 82;
  const y = 226;
  const widths = [180, 620, 250];
  ["Control", "Required design decision", "Why it matters"].forEach((h, i) => {
    node(slide, ctx, x + widths.slice(0, i).reduce((a, b) => a + b, 0), y, widths[i], 48, h, "", {
      fill: C.warm,
      titleSize: 13,
      bodySize: 1,
    });
  });
  rows.forEach((row, i) => {
    const yy = y + 56 + i * 78;
    node(slide, ctx, x, yy, widths[0], 66, row[0], "", { fill: C.white, bar: i === 0 ? C.red : C.teal, titleSize: 15 });
    node(slide, ctx, x + widths[0], yy, widths[1], 66, row[1], "", { fill: C.white, titleSize: 13.5, bodySize: 1 });
    node(slide, ctx, x + widths[0] + widths[1], yy, widths[2], 66, row[2], "", { fill: C.warm2, titleSize: 13.5, bodySize: 1 });
  });
  pill(slide, ctx, 82, 604, "Design principle: move models to governed context, not governed data to every model.", {
    w: 650,
    fill: "#e4efed",
    color: C.tealDark,
  });
  return slide;
}
