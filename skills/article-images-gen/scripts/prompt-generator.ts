#!/usr/bin/env bun
/**
 * article-images-gen - 文案插图提示词生成器
 *
 * 专业的文章配图提示词生成工具，专注于生成高质量的手绘风格插图提示词
 * 提示词可直接供 opencli-assistant 使用 opencli gemini/chatgpt/grok 生成图片
 */

import path from "node:path";
import process from "node:process";
import { readFile, writeFile, mkdir, access } from "node:fs/promises";
import { generateOutline, generatePromptFiles } from "./article-analyzer";

type CliArgs = {
  articlePath: string | null;
  prompt: string | null;
  promptFiles: string | null;
  density: "minimal" | "balanced" | "per-section" | "rich" | null;
  outputDir: string | null;
  help: boolean;
};

const DENSITY_OPTIONS = ["minimal", "balanced", "per-section", "rich"] as const;

function printUsage(): void {
  console.log(`Usage:
  bun scripts/prompt-generator.ts path/to/article.md
  bun scripts/prompt-generator.ts path/to/article.md --density balanced
  bun scripts/prompt-generator.ts --prompt "your description"
  bun scripts/prompt-generator.ts --promptfiles prompt1.md,prompt2.md
  bun scripts/prompt-generator.ts --help

Options:
  --density <level>    Image density: minimal (1-2), balanced (3-4), per-section, rich (5+)
  --prompt <text>      Direct description for single prompt generation
  --promptfiles <files> Comma-separated list of prompt files to read
  --output-dir <path>  Override output directory
  -h, --help           Show help

Density Levels:
  minimal      Core concepts only (1-2 images)
  balanced     Major sections (3-4 images)
  per-section  At least 1 per section (recommended)
  rich         Comprehensive coverage (5+ images)
`);
}

function parseArgs(argv: string[]): CliArgs {
  const args: CliArgs = {
    articlePath: null,
    prompt: null,
    promptFiles: null,
    density: null,
    outputDir: null,
    help: false,
  };

  for (let i = 0; i < argv.length; i++) {
    const current = argv[i]!;
    if (current === "--density") {
      args.density = argv[++i] as CliArgs["density"];
    } else if (current === "--prompt") {
      args.prompt = argv[++i] ?? null;
    } else if (current === "--promptfiles") {
      args.promptFiles = argv[++i] ?? null;
    } else if (current === "--output-dir") {
      args.outputDir = argv[++i] ?? null;
    } else if (current === "--help" || current === "-h") {
      args.help = true;
    } else if (!current.startsWith("-") && !args.articlePath) {
      args.articlePath = current;
    }
  }

  return args;
}

async function fileExists(filePath: string): Promise<boolean> {
  try {
    await access(filePath);
    return true;
  } catch {
    return false;
  }
}

function determineOutputDir(articlePath: string | null, overrideDir: string | null): string {
  if (overrideDir) {
    return overrideDir;
  }
  const today = new Date().toISOString().slice(0, 10).replace(/-/g, "");
  const articleName = articlePath
    ? path.basename(articlePath, path.extname(articlePath))
    : "single-prompt";
  return `/tmp/imageGen/${today}/${articleName}`;
}

async function generatePromptsForArticle(
  articlePath: string,
  articleContent: string,
  density: string,
  outputDir: string
): Promise<void> {
  console.log(`\n📄 Analyzing article: ${articlePath}`);
  console.log(`📊 Density: ${density}`);
  console.log(`📁 Output: ${outputDir}\n`);

  // Step 1: Generate outline
  console.log("Step 1: Generating outline...");
  const outline = await generateOutline(articlePath, articleContent, density, outputDir);
  console.log(`  ✓ Outline saved to ${outputDir}/outline.md`);
  console.log(`  ✓ ${outline.image_count} illustration prompts planned\n`);

  // Step 2: Generate prompt files
  console.log("Step 2: Generating prompt files...");
  const promptFiles = await generatePromptFiles(outline, articleContent, outputDir);
  console.log(`  ✓ ${promptFiles.length} prompt files saved to ${outputDir}/prompts/\n`);

  // Step 3: Output summary for opencli-assistant
  console.log("Step 3: Generating execution summary...");
  await generateExecutionSummary(outline, promptFiles, outputDir);
  console.log(`  ✓ Execution summary saved to ${outputDir}/EXECUTE.md\n`);

  // Summary
  console.log("=".repeat(50));
  console.log("Article Prompt Generation Complete!");
  console.log(`Article: ${articlePath}`);
  console.log(`Style: Hand-drawn Minimalist`);
  console.log(`Density: ${density}`);
  console.log(`Location: ${outputDir}`);
  console.log(`Prompts: ${outline.image_count} generated`);
  console.log("\n📋 Next step: Pass prompt files to @opencli-assistant for image generation");
  console.log(`   opencli gemini image "$(cat ${outputDir}/prompts/*.md)" --rt 16:9`);
}

async function generateSinglePrompt(
  description: string,
  outputDir: string
): Promise<void> {
  console.log(`\n📝 Generating single prompt...`);
  console.log(`Description: ${description}`);
  console.log(`Output: ${outputDir}\n`);

  const promptsDir = path.join(outputDir, "prompts");
  await mkdir(promptsDir, { recursive: true });

  const { primaryColor, accentColor, elements } = extractKeyTerms(description);

  const promptContent = buildStandardizedPrompt({
    illustrationId: 1,
    section: "Single Image",
    purpose: "Custom illustration",
    visualContent: description,
    primaryColor,
    accentColor,
    elements,
  });

  const filePath = path.join(promptsDir, "01-hand-drawn-single.md");
  await writeFile(filePath, promptContent);

  console.log(`  ✓ Prompt saved to ${filePath}\n`);
  console.log("=".repeat(50));
  console.log("Single Prompt Generation Complete!");
  console.log(`Location: ${outputDir}`);
  console.log(`\n📋 Next step: Pass prompt file to @opencli-assistant`);
  console.log(`   opencli gemini image "$(cat ${filePath})" --rt 16:9`);
}

async function generateBatchPrompts(
  promptFiles: string[],
  outputDir: string
): Promise<void> {
  console.log(`\n📚 Processing ${promptFiles.length} prompt files...\n`);

  const promptsDir = path.join(outputDir, "prompts");
  await mkdir(promptsDir, { recursive: true });

  const generatedFiles: string[] = [];

  for (let i = 0; i < promptFiles.length; i++) {
    const file = promptFiles[i]!;
    const content = await readFile(file.trim(), "utf8");
    const description = content.replace(/^---\n[\s\S]*?\n---\n/, "").trim();

    const { primaryColor, accentColor, elements } = extractKeyTerms(description);

    const promptContent = buildStandardizedPrompt({
      illustrationId: i + 1,
      section: path.basename(file, path.extname(file)),
      purpose: "Batch illustration",
      visualContent: description,
      primaryColor,
      accentColor,
      elements,
    });

    const outputFile = path.join(
      promptsDir,
      `${String(i + 1).padStart(2, "0")}-hand-drawn-${path.basename(file, path.extname(file))}.md`
    );
    await writeFile(outputFile, promptContent);
    generatedFiles.push(outputFile);

    console.log(`  ✓ Prompt ${i + 1}: ${outputFile}`);
  }

  console.log(`\n${"=".repeat(50)}`);
  console.log("Batch Prompt Generation Complete!");
  console.log(`Location: ${outputDir}`);
  console.log(`Prompts: ${generatedFiles.length} generated`);
  console.log("\n📋 Next step: Pass prompt files to @opencli-assistant");
}

async function generateExecutionSummary(
  outline: any,
  promptFiles: string[],
  outputDir: string
): Promise<void> {
  const summary = `# Execution Summary for @opencli-assistant

## Overview
- **Article**: ${outline.articlePath || "N/A"}
- **Style**: Hand-drawn Minimalist
- **Density**: ${outline.density}
- **Total Prompts**: ${outline.image_count}

## Prompt Files

${promptFiles.map((f, i) => `- Prompt ${i + 1}: \`${f}\``).join("\n")}

## Quick Commands

### Generate all images (Gemini)
\`\`\`bash
${promptFiles.map((f) => `opencli gemini image "$(cat ${f} | sed -n '/## 提示词/,/## 生成参数/p' | grep -v '^##' | head -1)" --rt 16:9 --op ${outputDir} -f json --timeout 300`).join("\n")}
\`\`\`

### Fallback (ChatGPT)
\`\`\`bash
${promptFiles.map((f) => `opencli chatgpt image "$(cat ${f} | sed -n '/## 提示词/,/## 生成参数/p' | grep -v '^##' | head -1)" --rt 16:9 --op ${outputDir} -f json --timeout 300`).join("\n")}
\`\`\`

### Fallback (Grok)
\`\`\`bash
${promptFiles.map((f) => `opencli grok image "$(cat ${f} | sed -n '/## 提示词/,/## 生成参数/p' | grep -v '^##' | head -1)" --out ${outputDir} -f json --timeout 300 --count 1`).join("\n")}
\`\`\`

## Notes
- All prompts use 16:9 aspect ratio
- Style: hand-drawn, minimalist, no text
- Wait 15s between requests to avoid rate limiting
`;

  await writeFile(path.join(outputDir, "EXECUTE.md"), summary);
}

function buildStandardizedPrompt(params: {
  illustrationId: number;
  section: string;
  purpose: string;
  visualContent: string;
  primaryColor: string;
  accentColor: string;
  elements: string[];
}): string {
  const { illustrationId, section, purpose, visualContent, primaryColor, accentColor, elements } = params;

  const promptText = `Hand-drawn minimalist illustration: ${visualContent}. Simple, clean, lots of white space, balanced composition, unified color tone, no text, no words, no letters.`;

  return `---
illustration_id: ${illustrationId}
style: hand-drawn
article_section: "${section}"
purpose: "${purpose}"
---

## 提示词（Prompt）

${promptText}

## 生成参数

| 参数 | 值 |
|------|-----|
| 服务 | gemini（主）/ chatgpt（备选）/ grok（兜底） |
| 比例 | 16:9 |
| 风格 | 手绘、简约、留白 |
| 主色调 | ${primaryColor} |
| 辅助色 | ${accentColor} |

## 核心元素

${elements.map((e) => `- ${e}`).join("\n") || "- 抽象概念可视化"}

## 执行命令

\`\`\`bash
# 主方案：Gemini
opencli gemini image "${promptText.replace(/"/g, '\\"')}" --rt 16:9 --op /tmp/imageGen/output -f json --timeout 300

# 备选方案：ChatGPT
opencli chatgpt image "${promptText.replace(/"/g, '\\"')}" --rt 16:9 --op /tmp/imageGen/output -f json --timeout 300

# 兜底方案：Grok
opencli grok image "${promptText.replace(/"/g, '\\"')}" --out /tmp/imageGen/output -f json --timeout 300 --count 1
\`\`\`
`;
}

function extractKeyTerms(content: string): {
  primaryColor: string;
  accentColor: string;
  elements: string[];
} {
  const elements: string[] = [];
  const lowerContent = content.toLowerCase();

  const quoteMatches = content.match(/[""](.*?)[""]/g) || [];
  for (const quote of quoteMatches.slice(0, 5)) {
    const text = quote.replace(/[""']/g, "").trim();
    if (text.length > 1 && text.length < 30) {
      elements.push(text);
    }
  }

  let primaryColor = "蓝色/青色系";
  let accentColor = "橙色/黄色系";

  if (lowerContent.includes("科技") || lowerContent.includes("tech") || lowerContent.includes("ai") || lowerContent.includes("代码")) {
    primaryColor = "蓝色/紫色系";
    accentColor = "青色/绿色系";
  } else if (lowerContent.includes("温暖") || lowerContent.includes("warm") || lowerContent.includes("story")) {
    primaryColor = "橙色/黄色系";
    accentColor = "红色/粉色调";
  } else if (lowerContent.includes("自然") || lowerContent.includes("nature") || lowerContent.includes("green")) {
    primaryColor = "绿色/青色系";
    accentColor = "黄色/橙色调";
  } else if (lowerContent.includes("商业") || lowerContent.includes("business") || lowerContent.includes("金融")) {
    primaryColor = "深蓝/灰色系";
    accentColor = "金色/橙色调";
  }

  return { primaryColor, accentColor, elements };
}

async function main(): Promise<void> {
  const args = parseArgs(process.argv.slice(2));

  if (args.help) {
    printUsage();
    return;
  }

  // Single prompt mode
  if (args.prompt) {
    const outputDir = determineOutputDir(null, args.outputDir);
    await mkdir(outputDir, { recursive: true });
    await generateSinglePrompt(args.prompt, outputDir);
    return;
  }

  // Batch prompt files mode
  if (args.promptFiles) {
    const outputDir = determineOutputDir(null, args.outputDir);
    await mkdir(outputDir, { recursive: true });
    const files = args.promptFiles.split(",");
    await generateBatchPrompts(files, outputDir);
    return;
  }

  // Article mode
  if (!args.articlePath) {
    printUsage();
    process.exit(1);
  }

  if (!(await fileExists(args.articlePath))) {
    console.error(`Error: Article not found: ${args.articlePath}`);
    process.exit(1);
  }

  const density = args.density || "per-section";
  if (!DENSITY_OPTIONS.includes(density)) {
    console.error(`Error: Invalid density "${density}". Options: ${DENSITY_OPTIONS.join(", ")}`);
    process.exit(1);
  }

  const outputDir = determineOutputDir(args.articlePath, args.outputDir);
  const articleContent = await readFile(args.articlePath, "utf8");

  await generatePromptsForArticle(args.articlePath, articleContent, density, outputDir);
}

main().catch((error) => {
  console.error("Fatal error:", error instanceof Error ? error.message : String(error));
  process.exit(1);
});
