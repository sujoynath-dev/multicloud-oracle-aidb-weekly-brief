import { C, setup, kicker, claim, node, arrow, pill } from "./theme.mjs";

export async function slide06(presentation, ctx) {
  const slide = presentation.slides.add();
  setup(slide, ctx, { page: 6, source: "Oracle Database@AWS, @Google Cloud, @Azure official docs" });
  kicker(slide, ctx, "Placement model");
  claim(slide, ctx, "The architecture choice is increasingly data-plane plus AI-control-plane placement.", 82, 980);

  const lanes = [
    ["AWS", C.aws, "EC2/EKS/Lambda", "Oracle Database@AWS", "Bedrock, Redshift, S3, EventBridge"],
    ["Google Cloud", C.google, "Cloud Run/GKE/Compute", "Oracle Database@Google Cloud", "Gemini Enterprise, GoldenGate, Database Center"],
    ["Azure", C.azure, "AKS/App Service/Functions", "Oracle AI Database@Azure", "Microsoft Foundry, policy, identity"],
  ];
  lanes.forEach((lane, i) => {
    const y = 222 + i * 118;
    pill(slide, ctx, 72, y + 37, lane[0], { w: 120, fill: C.white, color: C.charcoal });
    node(slide, ctx, 220, y, 220, 90, "Application tier", lane[2], { fill: C.white, bar: lane[1] });
    arrow(slide, ctx, 448, y + 45, 516, y + 45, { color: C.muted });
    node(slide, ctx, 532, y, 244, 90, "Oracle data plane", lane[3], { fill: "#eef5f5", bar: C.teal });
    arrow(slide, ctx, 784, y + 45, 852, y + 45, { color: C.muted });
    node(slide, ctx, 868, y, 300, 90, "AI and analytics plane", lane[4], { fill: C.warm2, bar: lane[1] });
  });
  return slide;
}
