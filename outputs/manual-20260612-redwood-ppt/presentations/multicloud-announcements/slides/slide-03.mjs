import { C, setup, kicker, claim, node, arrow, metric, bullet } from "./theme.mjs";

export async function slide03(presentation, ctx) {
  const slide = presentation.slides.add();
  setup(slide, ctx, { page: 3, source: "AWS Oracle Database@AWS document history and overview" });
  kicker(slide, ctx, "AWS update");
  claim(slide, ctx, "Autonomous Database Serverless lowers the entry path for Oracle data on AWS.", 82, 950);

  node(slide, ctx, 78, 238, 260, 120, "Before", "Most serious Oracle Database@AWS designs centered on dedicated Exadata infrastructure and VM cluster planning.", {
    fill: C.warm2,
  });
  arrow(slide, ctx, 356, 298, 454, 298, { color: C.red });
  node(slide, ctx, 470, 218, 318, 160, "Now", "AWS documentation says Oracle Database@AWS supports Autonomous Database Serverless with create and manage flows and a public AWS Marketplace offer.", {
    fill: C.white,
    bar: C.red,
    titleSize: 18,
  });
  arrow(slide, ctx, 804, 298, 902, 298, { color: C.red });
  node(slide, ctx, 918, 238, 260, 120, "Impact", "Elastic AI and app workloads can start without provisioning Exadata infrastructure or VM clusters.", {
    fill: "#fff7f2",
  });

  metric(slide, ctx, 98, 452, "ADB-S", "serverless Autonomous Database path", { w: 210, color: C.redDark });
  metric(slide, ctx, 340, 452, "Bedrock", "agent and generative AI adjacency", { w: 210, color: C.charcoal });
  metric(slide, ctx, 582, 452, "Redshift", "zero-ETL analytics watch pattern", { w: 210, color: C.tealDark });
  metric(slide, ctx, 824, 452, "S3", "backup and data integration surface", { w: 210, color: C.aws });

  bullet(slide, ctx, 98, 584, "Best pilot lane: AI-enabled apps that need Oracle transactional integrity with AWS-native model and analytics services.", {
    w: 930,
    dot: C.red,
  });
  return slide;
}
