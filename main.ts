import { copyFileSync, mkdirSync, statSync } from "node:fs";

// The World Today — Tuesday 24 November 2026.
// Copies the pre-rendered broadsheet image to the harness output dir.
// Deterministic: the same input bytes are copied on every run, and the
// entry is rejected loudly if it ever exceeds the 1 MiB gate.
const MAX_BYTES = 1048576;
const outDir = process.argv[2] ?? "/output";
const src = new URL("./entry.png", import.meta.url);
const size = statSync(src).size;
if (size > MAX_BYTES) {
  throw new Error(`entry.png is ${size} bytes, over the ${MAX_BYTES} byte limit`);
}
mkdirSync(outDir, { recursive: true });
copyFileSync(src, `${outDir}/entry.png`);
