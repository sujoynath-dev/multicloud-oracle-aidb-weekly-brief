import { C, setup, kicker, claim, node, pill } from "./theme.mjs";

export async function slide04(presentation, ctx) {
  const slide = presentation.slides.add();
  setup(slide, ctx, { page: 4, source: "Google Cloud Oracle Database@Google Cloud release notes" });
  kicker(slide, ctx, "Google Cloud watchlist");
  claim(slide, ctx, "Google Cloud shows a recent expansion pattern, not a current-week spike.", 82, 940);

  const items = [
    ["20 Apr", "Database Center integration GA", "Fleet insights, alerts, and recommendations for Exadata and Autonomous Database."],
    ["19 May", "Autonomous Data Guard local peers GA", "Improves local continuity for Autonomous Database in Google Cloud."],
    ["20 May", "OCI GoldenGate support GA", "Strengthens migration, replication, and data-product feeds."],
    ["27 May", "Melbourne and Milan zones", "Adds placement options for Exascale, Base Database, and GoldenGate."],
    ["9 Jun", "Release notes page updated", "No new dated Oracle Database enhancement inside 6-12 June."],
  ];
  ctx.addShape(slide, { x: 118, y: 275, w: 986, h: 2, fill: C.line });
  items.forEach((item, i) => {
    const x = 118 + i * 246;
    ctx.addShape(slide, { x: x - 9, y: 266, w: 20, h: 20, geometry: "ellipse", fill: i === 4 ? C.warm : C.teal });
    pill(slide, ctx, x - 35, 214, item[0], { w: 70, fill: i === 4 ? C.warm2 : "#e4efed", color: C.charcoal });
    node(slide, ctx, x - 88, 322, 176, 158, item[1], item[2], {
      fill: i === 4 ? C.warm2 : C.white,
      bar: i === 4 ? C.line : C.teal,
      titleSize: 14,
      bodySize: 11.5,
    });
  });
  return slide;
}
