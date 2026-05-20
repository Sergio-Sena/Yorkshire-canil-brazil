import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { minify } from "html-minifier-terser";
import CleanCSS from "clean-css";
import { minify as minifyJS } from "terser";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SRC = path.join(__dirname, "src");
const DIST = path.join(__dirname, "dist");

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

function copyDir(src, dest) {
  ensureDir(dest);
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      copyDir(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

async function build() {
  ensureDir(DIST);

  // Copy images
  const imgSrc = path.join(SRC, "images");
  if (fs.existsSync(imgSrc)) copyDir(imgSrc, path.join(DIST, "images"));

  // Copy videos
  const vidSrc = path.join(SRC, "videos");
  if (fs.existsSync(vidSrc)) copyDir(vidSrc, path.join(DIST, "videos"));

  // Copy data
  const dataSrc = path.join(SRC, "data");
  if (fs.existsSync(dataSrc)) copyDir(dataSrc, path.join(DIST, "data"));

  // Copy static files
  for (const file of ["robots.txt", "sitemap.xml", "manifest.json"]) {
    const src = path.join(SRC, file);
    if (fs.existsSync(src)) fs.copyFileSync(src, path.join(DIST, file));
  }

  // Minify CSS
  const cssSrc = path.join(SRC, "css");
  const cssDist = path.join(DIST, "css");
  ensureDir(cssDist);
  if (fs.existsSync(cssSrc)) {
    for (const file of fs.readdirSync(cssSrc).filter(f => f.endsWith(".css"))) {
      const input = fs.readFileSync(path.join(cssSrc, file), "utf8");
      const output = new CleanCSS({}).minify(input);
      fs.writeFileSync(path.join(cssDist, file), output.styles);
    }
  }

  // Minify JS
  const jsSrc = path.join(SRC, "js");
  const jsDist = path.join(DIST, "js");
  ensureDir(jsDist);
  if (fs.existsSync(jsSrc)) {
    for (const file of fs.readdirSync(jsSrc).filter(f => f.endsWith(".js"))) {
      const input = fs.readFileSync(path.join(jsSrc, file), "utf8");
      const output = await minifyJS(input);
      fs.writeFileSync(path.join(jsDist, file), output.code);
    }
  }

  // Minify HTML (root)
  for (const file of fs.readdirSync(SRC).filter(f => f.endsWith(".html"))) {
    const input = fs.readFileSync(path.join(SRC, file), "utf8");
    const output = await minify(input, {
      collapseWhitespace: true,
      removeComments: true,
      minifyCSS: true,
      minifyJS: true,
    });
    fs.writeFileSync(path.join(DIST, file), output);
  }

  // Minify HTML (blog)
  const blogSrc = path.join(SRC, "blog");
  const blogDist = path.join(DIST, "blog");
  if (fs.existsSync(blogSrc)) {
    ensureDir(blogDist);
    for (const file of fs.readdirSync(blogSrc).filter(f => f.endsWith(".html"))) {
      const input = fs.readFileSync(path.join(blogSrc, file), "utf8");
      const output = await minify(input, {
        collapseWhitespace: true,
        removeComments: true,
        minifyCSS: true,
        minifyJS: true,
      });
      fs.writeFileSync(path.join(blogDist, file), output);
    }
  }

  console.log("Build concluído em /dist");
}

build().catch(console.error);
