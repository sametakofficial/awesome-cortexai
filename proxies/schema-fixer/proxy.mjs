#!/usr/bin/env node
// schema-fixer-proxy: opencode'un tool schema'larını strict validator'lar için düzeltir
// $schema/ref keyword'lerini siler ve additionalProperties false olduğunda
// tüm property'leri required'a ekler. codex.claude.gg, openai.vertexapis.com
// veya herhangi bir strict OpenAI-uyumlu endpoint için forward proxy.
//
// Kullanım: node schema-fixer-proxy.mjs
// Sonra opencode baseURL'yi http://localhost:4015/<hedef-host>/v1 olarak ayarla

import http from "node:http"
import https from "node:https"

const PORT = process.env.PORT || 4015

function sanitize(obj) {
  if (obj === null || typeof obj !== "object") return obj
  if (Array.isArray(obj)) return obj.map(sanitize)
  const result = {}
  for (const [key, value] of Object.entries(obj)) {
    if (key === "$schema" || key === "ref") continue
    result[key] = typeof value === "object" && value !== null ? sanitize(value) : value
  }
  if (result.type === "object" && result.additionalProperties === false && result.properties) {
    result.required = Object.keys(result.properties)
  }
  return result
}

function fixTools(body) {
  if (!body.tools) return body
  body.tools = body.tools.map((tool) => {
    if (tool.function?.parameters) {
      tool.function.parameters = sanitize(tool.function.parameters)
    }
    return tool
  })
  return body
}

const server = http.createServer((req, res) => {
  // Extract target host from URL: /codex.claude.gg/v1/chat/completions
  const match = req.url.match(/^\/([^/]+)(\/.*)$/)
  if (!match) {
    res.writeHead(400)
    res.end(JSON.stringify({ error: "URL format: /<target-host>/path" }))
    return
  }

  const [, targetHost, path] = match
  const chunks = []

  req.on("data", (c) => chunks.push(c))
  req.on("end", () => {
    let body = Buffer.concat(chunks)

    // Fix tool schemas in request body
    if (body.length > 0) {
      try {
        const parsed = JSON.parse(body.toString())
        const fixed = fixTools(parsed)
        body = Buffer.from(JSON.stringify(fixed))
      } catch {}
    }

    const headers = { ...req.headers, host: targetHost, "content-length": body.length }
    delete headers["transfer-encoding"]

    const proxyReq = https.request(
      { hostname: targetHost, port: 443, path, method: req.method, headers },
      (proxyRes) => {
        res.writeHead(proxyRes.statusCode, proxyRes.headers)
        proxyRes.pipe(res)
      }
    )

    proxyReq.on("error", (e) => {
      res.writeHead(502)
      res.end(JSON.stringify({ error: e.message }))
    })

    proxyReq.end(body)
  })
})

server.listen(PORT, () => console.log(`schema-fixer-proxy listening on :${PORT}`))
