# AI Incident Reporting Compliance MCP

**One AI incident → many mandatory notifications.** Classifies once, emits every regime's clock + authority + form in parallel.

By [MEOK AI Labs](https://meok.ai).

## Regimes covered

- **EU AI Act Article 73** — serious-incident reporting (high-risk AI + GPAI with systemic risk). 15-day initial notification to market-surveillance authority.
- **DORA Article 19** — major ICT incident reporting (financial entities + CTPPs). 4h / 72h / 1 month clocks.
- **NIS2 Article 23** — significant incident (essential/important entities). 24h early warning / 72h notification / 1 month final.
- **GDPR Article 33** — personal-data breach (controllers). 72h.
- **ISO/IEC 42001 clause 9** — AIMS monitoring + internal incident for AI management systems.
- **UK AI Safety Institute (AISI)** — voluntary frontier-model incident reporting.

## Why this MCP

A single incident — say, a bias-driven lending decision that materially harms a protected group — can simultaneously trigger:

- EU AI Act Art 73 (high-risk AI fundamental-rights incident — **15 days**)
- DORA Art 19 (if financial entity, €100k impact — **4 hours**)
- NIS2 Art 23 (if essential entity, significant disruption — **24 hours**)
- GDPR Art 33 (personal data involved — **72 hours**)

If you don't know that, you miss the tightest SLA. This MCP classifies the incident against every regime in scope for your entity and tells you the master deadline.

## Tools

- `classify_incident` — multi-regime decision tree
- `list_regime_clocks` — all regime clocks + authorities
- `sign_incident_response_attestation` — Pro/Enterprise: signed post-incident evidence

## Install

```bash
pip install ai-incident-reporting-mcp
```

## Tiers

- **Free** — 10 classifications/day
- **Pro £199/mo** — unlimited + signed attestations + notification templates
- **Enterprise £1,499/mo** — multi-entity + Trust Center webhook pushes
- **£5,000 assessment** — 48h incident-response audit + playbook hardening

## Full Compliance Platform

Need the complete multi-regime stack? **[councilof.ai](https://councilof.ai)** — EU AI Act, DORA, NIS2, CRA, CSRD compliance from £29/mo. 100x cheaper than traditional consulting.

→ **[Get started at councilof.ai](https://councilof.ai)**

## Related MEOK MCPs

- [`eu-ai-act-compliance-mcp`](https://pypi.org/project/eu-ai-act-compliance-mcp/)
- [`dora-compliance-mcp`](https://pypi.org/project/dora-compliance-mcp/)
- [`nis2-compliance-mcp`](https://pypi.org/project/nis2-compliance-mcp/)
- [`dora-nis2-crosswalk-mcp`](https://pypi.org/project/dora-nis2-crosswalk-mcp/)
- [`meok-attestation-verify`](https://pypi.org/project/meok-attestation-verify/)

> **If this tool helps your compliance workflow, please [star this repo](https://github.com/CSOAI-ORG/ai-incident-reporting-mcp/stargazers)** — it helps other teams find it.

## License

MIT — [MEOK AI Labs](https://meok.ai), 2026.

<!-- mcp-name: io.github.CSOAI-ORG/ai-incident-reporting-mcp -->
