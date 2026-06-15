import { C, setup, kicker, claim, subline, bullet, metric, logoStrip } from "./theme.mjs";

export async function slide01(presentation, ctx) {
  const slide = presentation.slides.add();
  setup(slide, ctx, { noFooter: true });
  kicker(slide, ctx, "Official-source weekly brief", 54);
  claim(slide, ctx, "Weekly Multicloud Announcements and Innovations", 92, 760);
  subline(
    slide,
    ctx,
    "Oracle Database on Exadata and Autonomous AI Database across Oracle Cloud, AWS, Google Cloud, and Azure",
    64,
    250,
    720,
  );
  await logoStrip(slide, ctx, 64, 336);
  metric(slide, ctx, 920, 92, "9-15 Jun", "coverage window, Australia/Melbourne", { w: 230, color: C.charcoal });
  metric(slide, ctx, 920, 210, "AWS", "strongest weekly signal: ADB-S in Oracle Database@AWS", {
    w: 230,
    color: C.redDark,
  });
  bullet(slide, ctx, 920, 352, "OCI had adjacent data and AI platform updates: GoldenGate Veridata and Generative AI model import.", { w: 245 });
  bullet(slide, ctx, 920, 450, "Google Cloud and Azure had no new dated Oracle Database items inside the week.", {
    w: 245,
    dot: C.teal,
  });
  bullet(slide, ctx, 920, 548, "Deck theme follows the official Redwood reference page supplied by the user.", {
    w: 245,
    dot: C.amber,
  });
  return slide;
}
