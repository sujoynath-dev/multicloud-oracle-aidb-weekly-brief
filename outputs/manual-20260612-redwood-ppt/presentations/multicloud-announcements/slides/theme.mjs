import path from "node:path";

export const C = {
  paper: "#fbf9f8",
  warm: "#efebe6",
  warm2: "#f6f2ee",
  ink: "#161513",
  charcoal: "#312d2a",
  muted: "#6f625b",
  line: "#d7d0c8",
  red: "#c74634",
  redDark: "#8f3328",
  teal: "#4e7c78",
  tealDark: "#315f5b",
  blue: "#d8eaf0",
  azure: "#0078d4",
  aws: "#ff9900",
  google: "#4285f4",
  green: "#6f7f63",
  amber: "#f3b15b",
  white: "#ffffff",
};

export function asset(ctx, name) {
  return path.join(ctx.assetDir, name);
}

export function setup(slide, ctx, opts = {}) {
  const bg = opts.dark ? C.charcoal : C.paper;
  ctx.addShape(slide, { x: 0, y: 0, w: 1280, h: 720, fill: bg });
  ctx.addShape(slide, { x: 0, y: 0, w: 1280, h: 6, fill: opts.dark ? C.red : "#4b4540" });
  if (!opts.noFooter) {
    footer(slide, ctx, opts.source || "Official sources only", opts.page || "");
  }
}

export function footer(slide, ctx, source, page) {
  ctx.addShape(slide, { x: 64, y: 674, w: 1040, h: 1, fill: C.line });
  ctx.addText(slide, {
    x: 64,
    y: 686,
    w: 820,
    h: 16,
    text: source,
    fontSize: 10,
    color: C.muted,
  });
  ctx.addText(slide, {
    x: 1140,
    y: 686,
    w: 76,
    h: 16,
    text: page ? String(page).padStart(2, "0") : "",
    fontSize: 10,
    color: C.muted,
    align: "right",
  });
}

export function kicker(slide, ctx, text, y = 52, dark = false) {
  ctx.addShape(slide, { x: 64, y: y + 2, w: 8, h: 8, fill: dark ? C.red : C.redDark });
  ctx.addText(slide, {
    x: 82,
    y,
    w: 520,
    h: 16,
    text: text.toUpperCase(),
    fontSize: 11,
    color: dark ? "#e7ddd5" : C.muted,
    bold: true,
  });
}

export function claim(slide, ctx, text, y = 82, w = 950, dark = false) {
  ctx.addText(slide, {
    x: 64,
    y,
    w,
    h: 98,
    text,
    fontSize: 36,
    color: dark ? C.white : C.ink,
    bold: true,
    typeface: "Arial",
  });
}

export function subline(slide, ctx, text, x, y, w, color = C.muted) {
  ctx.addText(slide, { x, y, w, h: 42, text, fontSize: 17, color, typeface: "Arial" });
}

export function panel(slide, ctx, x, y, w, h, opts = {}) {
  return ctx.addShape(slide, {
    x,
    y,
    w,
    h,
    fill: opts.fill || C.warm2,
    line: { style: "solid", fill: opts.line || C.line, width: opts.lineWidth ?? 1 },
  });
}

export function pill(slide, ctx, x, y, text, opts = {}) {
  const w = opts.w || Math.max(72, text.length * 7.5 + 24);
  panel(slide, ctx, x, y, w, 24, { fill: opts.fill || C.warm, line: opts.line || C.line });
  ctx.addText(slide, {
    x: x + 10,
    y: y + 5,
    w: w - 20,
    h: 14,
    text,
    fontSize: 10,
    color: opts.color || C.charcoal,
    bold: true,
    align: "center",
  });
}

export function bullet(slide, ctx, x, y, text, opts = {}) {
  ctx.addShape(slide, { x, y: y + 7, w: 5, h: 5, geometry: "ellipse", fill: opts.dot || C.red });
  ctx.addText(slide, {
    x: x + 16,
    y,
    w: opts.w || 480,
    h: opts.h || 44,
    text,
    fontSize: opts.size || 16,
    color: opts.color || C.charcoal,
  });
}

export function metric(slide, ctx, x, y, value, label, opts = {}) {
  panel(slide, ctx, x, y, opts.w || 180, opts.h || 96, { fill: opts.fill || C.white, line: opts.line || C.line });
  ctx.addText(slide, {
    x: x + 18,
    y: y + 14,
    w: (opts.w || 180) - 36,
    h: 30,
    text: value,
    fontSize: opts.valueSize || 28,
    color: opts.color || C.redDark,
    bold: true,
  });
  ctx.addText(slide, {
    x: x + 18,
    y: y + 50,
    w: (opts.w || 180) - 36,
    h: 32,
    text: label,
    fontSize: 12,
    color: C.muted,
  });
}

export function node(slide, ctx, x, y, w, h, title, body, opts = {}) {
  panel(slide, ctx, x, y, w, h, { fill: opts.fill || C.white, line: opts.line || C.line });
  if (opts.bar) ctx.addShape(slide, { x, y, w, h: 5, fill: opts.bar });
  const titleH = opts.titleH || 32;
  const bodyY = y + 48;
  ctx.addText(slide, {
    x: x + 14,
    y: y + 14,
    w: w - 28,
    h: titleH,
    text: title,
    fontSize: opts.titleSize || 16,
    color: opts.titleColor || C.ink,
    bold: true,
  });
  ctx.addText(slide, {
    x: x + 14,
    y: bodyY,
    w: w - 28,
    h: Math.max(12, h - 64),
    text: body,
    fontSize: opts.bodySize || 12.5,
    color: opts.bodyColor || C.muted,
  });
}

export function arrow(slide, ctx, x1, y1, x2, y2, opts = {}) {
  const horizontal = Math.abs(x2 - x1) >= Math.abs(y2 - y1);
  const color = opts.color || C.muted;
  const thickness = opts.width || 2;
  if (horizontal) {
    const left = Math.min(x1, x2);
    const width = Math.max(24, Math.abs(x2 - x1));
    ctx.addShape(slide, {
      x: left,
      y: y1 - Math.max(4, thickness * 2),
      w: width,
      h: Math.max(10, thickness * 5),
      geometry: x2 >= x1 ? "rightArrow" : "leftArrow",
      fill: color,
      line: { style: "solid", fill: color, width: 0 },
    });
  } else {
    const top = Math.min(y1, y2);
    const height = Math.max(24, Math.abs(y2 - y1));
    ctx.addShape(slide, {
      x: x1 - Math.max(4, thickness * 2),
      y: top,
      w: Math.max(10, thickness * 5),
      h: height,
      geometry: y2 >= y1 ? "downArrow" : "upArrow",
      fill: color,
      line: { style: "solid", fill: color, width: 0 },
    });
  }
}

export function sourceUrl(slide, ctx, x, y, label, url, opts = {}) {
  panel(slide, ctx, x, y, opts.w || 520, opts.h || 52, { fill: opts.fill || C.white, line: C.line });
  ctx.addText(slide, {
    x: x + 12,
    y: y + 8,
    w: (opts.w || 520) - 24,
    h: 16,
    text: label,
    fontSize: 10.5,
    color: C.ink,
    bold: true,
  });
  ctx.addText(slide, {
    x: x + 12,
    y: y + 27,
    w: (opts.w || 520) - 24,
    h: 16,
    text: url,
    fontSize: opts.urlSize || 8.6,
    color: C.redDark,
  });
}

export async function logoStrip(slide, ctx, x = 64, y = 360) {
  const logos = [
    ["oracle-wordmark-official.png", "Oracle"],
    ["google-cloud-official.png", "Google Cloud"],
    ["aws-official.png", "AWS"],
    ["azure-official.png", "Microsoft Azure"],
  ];
  const cellW = 184;
  const gap = 14;
  for (let i = 0; i < logos.length; i += 1) {
    const cellX = x + i * (cellW + gap);
    panel(slide, ctx, cellX, y, cellW, 74, { fill: C.white, line: C.line });
    await ctx.addImage(slide, {
      path: asset(ctx, logos[i][0]),
      x: cellX + 18,
      y: y + 20,
      w: cellW - 36,
      h: 34,
      fit: "contain",
      alt: logos[i][1],
    });
  }
}
