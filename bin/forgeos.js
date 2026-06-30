#!/usr/bin/env node
/**
 * Forge OS npm CLI wrapper.
 * Requires Python 3.10+ with project dependencies installed.
 */
const { spawn } = require("child_process");
const path = require("path");
const fs = require("fs");

const ROOT = path.resolve(__dirname, "..");
const CLI = path.join(ROOT, "cli.py");

function findPython() {
  if (process.env.FORGEOS_PYTHON && fs.existsSync(process.env.FORGEOS_PYTHON)) {
    return process.env.FORGEOS_PYTHON;
  }
  const venvPython = path.join(
    ROOT,
    ".venv",
    process.platform === "win32" ? "Scripts/python.exe" : "bin/python"
  );
  if (fs.existsSync(venvPython)) {
    return venvPython;
  }
  return process.platform === "win32" ? "python" : "python3";
}

const python = findPython();
const args = process.argv.slice(2);
const cliArgs = args.length ? args : ["login"];

const child = spawn(python, [CLI, ...cliArgs], {
  cwd: ROOT,
  stdio: "inherit",
  env: { ...process.env, PYTHONIOENCODING: "utf-8" },
});

child.on("exit", (code) => process.exit(code ?? 1));
child.on("error", (err) => {
  console.error("Failed to start Forge OS:", err.message);
  console.error("Install Python 3.10+ and run: pip install -r requirements.txt");
  process.exit(1);
});
