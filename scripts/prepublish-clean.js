#!/usr/bin/env node
/** Remove Python cache before npm pack/publish (package.json "files" ignores .npmignore). */
const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");

function walk(dir, removeDirs) {
  if (!fs.existsSync(dir)) return;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (entry.name === "__pycache__") {
        removeDirs.push(full);
      } else if (entry.name !== "node_modules" && entry.name !== ".venv") {
        walk(full, removeDirs);
      }
    } else if (entry.name.endsWith(".pyc") || entry.name.endsWith(".pyo")) {
      fs.unlinkSync(full);
    }
  }
}

const dirs = [];
walk(ROOT, dirs);
for (const dir of dirs) {
  fs.rmSync(dir, { recursive: true, force: true });
}

console.log(`Cleaned ${dirs.length} __pycache__ folder(s) before publish.`);
