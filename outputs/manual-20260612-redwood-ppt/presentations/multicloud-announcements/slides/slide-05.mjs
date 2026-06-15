import { C, setup, kicker, claim, node, arrow, metric } from "./theme.mjs";

export async function slide05(presentation, ctx) {
  const slide = presentation.slides.add();
  setup(slide, ctx, { page: 5, source: "Oracle AI Database@Azure docs; Microsoft Foundry docs" });
  kicker(slide, ctx, "Azure platform stance");
  claim(slide, ctx, "Azure remains a broad landing zone for Oracle AI Database plus Microsoft Foundry.", 82, 970);

  node(slide, ctx, 72, 230, 210, 128, "Azure apps", "AKS, App Service, Functions, VM workloads, and enterprise network controls.", {
    fill: C.white,
    bar: C.azure,
  });
  arrow(slide, ctx, 292, 292, 370, 292, { color: C.azure });
  node(slide, ctx, 386, 218, 250, 152, "Delegated subnet", "Oracle docs describe Azure VNet plus delegated subnet for direct, secure, low-latency connectivity.", {
    fill: C.warm2,
    bar: C.line,
  });
  arrow(slide, ctx, 648, 292, 726, 292, { color: C.azure });
  node(slide, ctx, 742, 218, 250, 152, "Oracle AI Database@Azure", "Exadata Database Service and Autonomous AI Database provisioned from the Azure console.", {
    fill: "#eef5f5",
    bar: C.teal,
  });
  arrow(slide, ctx, 870, 380, 870, 452, { color: C.muted });
  node(slide, ctx, 704, 468, 334, 112, "Microsoft Foundry", "Agents, model routing, evaluations, monitoring, policies, and enterprise AI operations.", {
    fill: C.white,
    bar: C.azure,
  });
  metric(slide, ctx, 1060, 230, "33", "live Oracle AI Database@Azure regions in official availability page", {
    w: 150,
    color: C.azure,
  });
  return slide;
}
