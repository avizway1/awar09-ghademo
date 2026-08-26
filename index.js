/**
 * Aviz Academy - GitHub Actions demo app
 *
 * A dependency-free Node.js script used to verify that a GHA workflow
 * can check out the repo, set up Node and run our code on the runner.
 *
 * Usage: node index.js
 */

const BRAND = "Aviz Academy";
const APP_VERSION = "1.0.0";

function banner() {
  const line = "=".repeat(46);
  return [
    line,
    `  ${BRAND}  |  GitHub Actions + Node.js Demo`,
    line,
  ].join("\n");
}

function greet(name = "Learner") {
  return `Welcome to my ${BRAND}, ${name}!`;
}

function runnerInfo() {
  return {
    app: `${BRAND.toLowerCase().replace(/\s+/g, "-")}-gha-demo`,
    version: APP_VERSION,
    node: process.version,
    platform: `${process.platform}/${process.arch}`,
    ci: process.env.CI === "true",
    repository: process.env.GITHUB_REPOSITORY || "local",
    branch: process.env.GITHUB_REF_NAME || "local",
    workflow: process.env.GITHUB_WORKFLOW || "n/a",
    actor: process.env.GITHUB_ACTOR || "local-user",
  };
}

function main() {
  console.log(banner());
  console.log(greet(process.env.GITHUB_ACTOR || "Avinash"));
  console.log("\nBuild environment:");

  const info = runnerInfo();
  for (const [key, value] of Object.entries(info)) {
    console.log(`  ${key.padEnd(12)}: ${value}`);
  }

  // Simple sanity check so a broken runtime fails the workflow.
  if (!greet("Batch 9").includes(BRAND)) {
    console.error("\nSanity check failed: branding missing from greeting.");
    process.exit(1);
  }

  console.log(`\nBuild successful - happy learning from ${BRAND}!`);
}

if (require.main === module) {
  main();
}

module.exports = { greet, banner, runnerInfo, BRAND, APP_VERSION };
