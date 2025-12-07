const http = require("http");
const fs = require("fs");
const path = require("path");

const PORT = process.env.PORT || 4173;
const PUBLIC_DIR = __dirname;

const mimeTypes = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "application/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".gif": "image/gif",
  ".ico": "image/x-icon",
};

function sanitizeUrl(urlPath) {
  const normalized = path.normalize(urlPath.split("?")[0]);
  if (normalized.startsWith("..")) return "/";
  return normalized;
}

function getFilePath(urlPath) {
  const sanitized = sanitizeUrl(urlPath);
  const joined = path.join(PUBLIC_DIR, sanitized);

  if (fs.existsSync(joined) && fs.statSync(joined).isDirectory()) {
    return path.join(joined, "index.html");
  }

  return joined;
}

function serveFile(filePath, res) {
  fs.readFile(filePath, (err, data) => {
    if (err) {
      if (err.code === "ENOENT") {
        // Fall back to index.html for unknown routes (SPA behavior)
        if (!filePath.endsWith("index.html")) {
          return serveFile(path.join(PUBLIC_DIR, "index.html"), res);
        }
      }
      res.writeHead(500, { "Content-Type": "text/plain" });
      res.end("Internal server error");
      return;
    }

    const ext = path.extname(filePath).toLowerCase();
    const contentType = mimeTypes[ext] || "application/octet-stream";
    res.writeHead(200, { "Content-Type": contentType });
    res.end(data);
  });
}

const server = http.createServer((req, res) => {
  const filePath = getFilePath(req.url);
  serveFile(filePath, res);
});

server.listen(PORT, () => {
  console.log(`Rooted preview server running at http://localhost:${PORT}`);
});
