# AI Incident Reporting Compliance MCP


> ## Buy Starter — £29/mo
> **Signed attestations + unlimited audits + email support.**
> 👉 **[Subscribe at meok.ai](https://buy.stripe.com/3cI7sNfsMaEG5g9dCU8k83T)** — instant HMAC signing key + Stripe-managed billing.
>
> Free tier remains MIT-licensed and zero-config. Upgrade only when you need signed compliance artefacts for audit.

[![PyPI](https://img.shields.io/pypi/v/ai-incident-reporting-mcp)](https://pypi.org/project/ai-incident-reporting-mcp/) [![Python](https://img.shields.io/pypi/pyversions/ai-incident-reporting-mcp)](https://pypi.org/project/ai-incident-reporting-mcp/)


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

> **If this tool helps your compliance workflow, please [star this repo](https://github.com/meok-ai-labs/ai-incident-reporting-mcp/stargazers)** — it helps other teams find it.

## License

MIT — [MEOK AI Labs](https://meok.ai), 2026.

<<<<<<< Updated upstream
=======
<!-- meok-faq-schema-v1 -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Is this MCP server free to use?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes. The free tier gives you 10 calls per day with no API key required. Pro tier is £79/mo for unlimited calls plus cryptographically signed attestations your auditor can verify independently."
      }
    },
    {
      "@type": "Question",
      "name": "How does the signed attestation work?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Every Pro tier audit produces a HMAC-SHA256 signed certificate with a unique ID and a public verify URL. Your auditor pastes the cert into https://meok-attestation-api.vercel.app/verify and gets an independent valid/invalid response. No contact with MEOK required."
      }
    },
    {
      "@type": "Question",
      "name": "Which MCP clients does this work with?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "All standard MCP clients: Claude Desktop, Claude Code, Cursor, VS Code with MCP extension, Windsurf, Cline, and any custom MCP-compatible agent. Install via npx meok-setup or pip install for the underlying Python package."
      }
    },
    {
      "@type": "Question",
      "name": "Can I install all MEOK governance MCPs at once?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes. Run npx meok-setup --pack governance to install all 10 governance MCPs and write the configs for Claude Desktop, Cursor, or Windsurf in one command."
      }
    },
    {
      "@type": "Question",
      "name": "Is the regulation text authoritative?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes. MEOK syncs daily from the EUR-Lex Cellar SPARQL endpoint, the canonical EU regulation publication system. The text is verbatim with no LLM summarization. Every quote is auditor-defensible and includes the exact article number plus relevance score."
      }
    }
  ]
}
</script>

>>>>>>> Stashed changes

## Sister MCPs

Part of the MEOK **Governance** pack — designed to work together as a fleet. Install the whole pack with `npx meok-setup --pack governance`, or pick the ones you need:

- **EU AI Act** → `uvx eu-ai-act-compliance-mcp` · [PyPI](https://pypi.org/project/eu-ai-act-compliance-mcp/) · [GitHub](https://github.com/CSOAI-ORG/eu-ai-act-compliance-mcp)
- **DORA** → `uvx dora-compliance-mcp` · [PyPI](https://pypi.org/project/dora-compliance-mcp/) · [GitHub](https://github.com/CSOAI-ORG/dora-compliance-mcp)
- **NIS2** → `uvx nis2-compliance-mcp` · [PyPI](https://pypi.org/project/nis2-compliance-mcp/) · [GitHub](https://github.com/CSOAI-ORG/nis2-compliance-mcp)
- **Cyber Resilience Act** → `uvx cra-compliance-mcp` · [PyPI](https://pypi.org/project/cra-compliance-mcp/) · [GitHub](https://github.com/CSOAI-ORG/cra-compliance-mcp)
- **AI Bill of Materials** → `uvx ai-bom-mcp` · [PyPI](https://pypi.org/project/ai-bom-mcp/) · [GitHub](https://github.com/CSOAI-ORG/ai-bom-mcp)
- **DORA × NIS2 Crosswalk** → `uvx dora-nis2-crosswalk-mcp` · [PyPI](https://pypi.org/project/dora-nis2-crosswalk-mcp/) · [GitHub](https://github.com/CSOAI-ORG/dora-nis2-crosswalk-mcp)

Full catalogue + Anthropic Registry verify links: [meok.ai/anthropic-registry](https://meok.ai/anthropic-registry)

<!-- mcp-name: io.github.CSOAI-ORG/ai-incident-reporting-mcp -->
