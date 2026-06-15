import { C, setup, kicker, claim, node } from "./theme.mjs";

export async function slide08(presentation, ctx) {
  const slide = presentation.slides.add();
  setup(slide, ctx, { page: 8, source: "Architecture ideas synthesized from official service docs" });
  kicker(slide, ctx, "Architecture moves");
  claim(slide, ctx, "Four multicloud moves are ready to evaluate.", 82, 880);

  const cards = [
    ["AWS operational AI", "Use Oracle Database@AWS ADB-S or Exadata with Bedrock agents, Redshift analytics, S3 integration, and CloudWatch/EventBridge operations.", C.aws],
    ["Gemini enterprise knowledge", "Ground Gemini Enterprise assistants on governed Oracle data, selected replicated views, GoldenGate feeds, and access-controlled search.", C.google],
    ["Azure regulated copilot", "Pair Oracle AI Database@Azure with Microsoft Foundry agents, model routing, evaluations, policy, identity, and Teams/M365 channels.", C.azure],
    ["Cross-cloud governed fabric", "Keep Oracle as system of record, replicate only selected data products, and route AI work to the best provider by risk and domain.", C.teal],
  ];
  cards.forEach((card, i) => {
    const x = 82 + (i % 2) * 555;
    const y = 230 + Math.floor(i / 2) * 170;
    node(slide, ctx, x, y, 500, 130, card[0], card[1], { fill: C.white, bar: card[2], titleSize: 19, bodySize: 14 });
  });
  return slide;
}
