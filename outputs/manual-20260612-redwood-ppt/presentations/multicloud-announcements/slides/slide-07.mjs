import { C, setup, kicker, claim, node, arrow, bullet } from "./theme.mjs";

export async function slide07(presentation, ctx) {
  const slide = presentation.slides.add();
  setup(slide, ctx, { page: 7, source: "Oracle AI Vector Search; Bedrock; Gemini Enterprise; Microsoft Foundry docs" });
  kicker(slide, ctx, "Governed RAG");
  claim(slide, ctx, "Autonomous AI Database can anchor RAG while hyperscaler AI handles reasoning and workflow.", 82, 980);

  node(slide, ctx, 82, 228, 220, 120, "Oracle operational data", "Transactions, documents, metadata, policies, lineage, and entitlements stay governed in Oracle.", {
    fill: C.white,
    bar: C.teal,
  });
  arrow(slide, ctx, 312, 288, 384, 288, { color: C.teal });
  node(slide, ctx, 400, 228, 220, 120, "AI Vector Search", "Embeddings stored beside business data; semantic search runs close to the governed records.", {
    fill: "#eef5f5",
    bar: C.teal,
  });
  arrow(slide, ctx, 630, 288, 702, 288, { color: C.muted });
  node(slide, ctx, 718, 228, 220, 120, "Model platform", "Bedrock, Gemini Enterprise, Microsoft Foundry, or OCI Generative AI selected by use case.", {
    fill: C.warm2,
    bar: C.red,
  });
  arrow(slide, ctx, 948, 288, 1020, 288, { color: C.muted });
  node(slide, ctx, 1036, 228, 160, 120, "Agent action", "Answer, summarize, route, write back, or escalate with controls.", {
    fill: C.white,
    bar: C.amber,
  });
  bullet(slide, ctx, 112, 420, "Use Oracle as the governed retrieval and data-quality boundary.", { w: 470, dot: C.teal });
  bullet(slide, ctx, 112, 482, "Expose only approved views, APIs, summaries, or vector search results to the model layer.", {
    w: 470,
    dot: C.red,
  });
  bullet(slide, ctx, 664, 420, "Choose the AI platform by domain fit, model governance, latency, cost, and enterprise channel.", {
    w: 470,
    dot: C.amber,
  });
  bullet(slide, ctx, 664, 502, "Log prompts, retrieval context, output, and user action for auditability.", { w: 470, dot: C.blue });
  return slide;
}
