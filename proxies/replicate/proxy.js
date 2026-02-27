const http = require("http");
const https = require("https");

const PORT = process.env.PROXY_PORT || 9877;
const GATEAI_TOKEN = process.env.GATEAI_API_TOKEN || "";
const REPLICATE_TOKEN = process.env.REPLICATE_API_TOKEN || "";
const GATEAI_BASE = "api.gateai.app";
const REPLICATE_BASE = "api.replicate.com";

function isPredictionRoute(method, path) {
  if (path.match(/\/v1\/predictions/)) return true;
  if (method === "POST" && path.match(/\/v1\/models\/.+\/predictions/)) return true;
  if (path.match(/\/v1\/deployments\/.+\/predictions/)) return true;
  if (path.match(/\/v1\/trainings/)) return true;
  return false;
}

const server = http.createServer((req, res) => {
  const useGateAI = isPredictionRoute(req.method, req.url);
  const targetHost = useGateAI ? GATEAI_BASE : REPLICATE_BASE;
  const token = useGateAI ? GATEAI_TOKEN : REPLICATE_TOKEN;

  const tag = useGateAI ? "GATE" : "REPL";
  console.log(`[${tag}] ${req.method} ${req.url} -> ${targetHost}`);

  if (!token) {
    const missing = useGateAI ? "GATEAI_API_TOKEN" : "REPLICATE_API_TOKEN";
    res.writeHead(500, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ error: `${missing} not set` }));
    return;
  }

  let body = [];
  req.on("data", (chunk) => body.push(chunk));
  req.on("end", () => {
    const bodyBuf = Buffer.concat(body);

    const headers = {
      host: targetHost,
      authorization: `Bearer ${token}`,
      "content-type": req.headers["content-type"] || "application/json",
      accept: "application/json",
      prefer: req.headers["prefer"] || "",
    };
    if (bodyBuf.length > 0) {
      headers["content-length"] = bodyBuf.length;
    }
    if (!headers.prefer) delete headers.prefer;

    const proxyReq = https.request(
      { hostname: targetHost, port: 443, path: req.url, method: req.method, headers },
      (proxyRes) => {
        res.writeHead(proxyRes.statusCode, proxyRes.headers);
        proxyRes.pipe(res);
      }
    );

    proxyReq.on("error", (err) => {
      console.error(`[ERR] ${err.message}`);
      res.writeHead(502, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: err.message }));
    });

    if (bodyBuf.length > 0) proxyReq.write(bodyBuf);
    proxyReq.end();
  });
});

server.listen(PORT, () => {
  console.log(`Replicate split proxy on :${PORT}`);
  console.log(`  Predictions -> ${GATEAI_BASE} (GATEAI_API_TOKEN)`);
  console.log(`  Metadata    -> ${REPLICATE_BASE} (REPLICATE_API_TOKEN)`);
  console.log(`  REPLICATE_API_TOKEN: ${REPLICATE_TOKEN ? "set" : "NOT SET"}`);
  console.log(`  GATEAI_API_TOKEN:    ${GATEAI_TOKEN ? "set" : "NOT SET"}`);
});
