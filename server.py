#!/usr/bin/env python3
"""
AI Incident Reporting Compliance MCP Server
=============================================
By MEOK AI Labs | https://meok.ai

Unified AI incident reporting across:

  - EU AI Act Article 73 (serious-incident reporting to market-surveillance authorities)
  - DORA Article 17-19 + Delegated Reg (EU) 2024/1772 (major ICT incidents)
  - NIS2 Article 23 (significant incidents — 24h/72h/1mo)
  - GDPR Article 33-34 (personal-data breach — 72h)
  - CISA / NIST AI Risk Management Framework (voluntary U.S.)
  - ISO/IEC 42001 clause 9 (AIMS monitoring + incident)
  - UK AI Safety Institute voluntary reporting (for frontier models)

One incident → multiple mandatory notifications to different authorities on
different clocks. This MCP classifies an incident ONCE and emits the decision
tree for every regime that applies.

Install: pip install ai-incident-reporting-mcp
Run:     python server.py
"""

import json
from datetime import datetime, timedelta, timezone
from typing import Optional
from collections import defaultdict
from mcp.server.fastmcp import FastMCP

import os as _os
import sys
import os

_MEOK_API_KEY = _os.environ.get("MEOK_API_KEY", "")

try:
    sys.path.insert(0, os.path.expanduser("~/clawd/meok-labs-engine/shared"))
    from auth_middleware import check_access as _shared_check_access
except ImportError:
    def _shared_check_access(api_key: str = ""):
        if _MEOK_API_KEY and api_key and api_key == _MEOK_API_KEY:
            return True, "OK", "pro"
        if _MEOK_API_KEY and api_key and api_key != _MEOK_API_KEY:
            return False, "Invalid API key.", "free"
        return True, "OK", "free"


try:
    from attestation import get_attestation_tool_response
    _ATTESTATION_LOCAL = True
except ImportError:
    _ATTESTATION_LOCAL = False

_ATTESTATION_API = _os.environ.get(
    "MEOK_ATTESTATION_API", "https://meok-attestation-api.vercel.app"
)


def _sign_via_api(api_key, regulation, entity, score, findings, articles_audited, tier="pro", include_pdf_base64=False):
    import urllib.request as _url, urllib.error as _urlerr
    payload = {"api_key": api_key, "regulation": regulation, "entity": entity,
               "score": score, "findings": findings or [],
               "articles_audited": articles_audited or [], "tier": tier}
    try:
        req = _url.Request(f"{_ATTESTATION_API}/sign",
                           data=json.dumps(payload).encode("utf-8"),
                           headers={"Content-Type": "application/json"})
        with _url.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except _urlerr.HTTPError as e:
        try:
            return json.loads(e.read())
        except Exception:
            return {"error": f"Attestation API HTTP {e.code}."}
    except Exception as e:
        return {"error": f"Could not reach MEOK attestation API: {e}."}


def _attestation(regulation, entity, score, findings, articles_audited, tier, include_pdf_base64, api_key):
    if _ATTESTATION_LOCAL:
        return get_attestation_tool_response(
            regulation=regulation, entity=entity, score=score, findings=findings,
            articles_audited=articles_audited, tier=tier, include_pdf_base64=include_pdf_base64,
        )
    return _sign_via_api(api_key=api_key, regulation=regulation, entity=entity,
                        score=score, findings=findings, articles_audited=articles_audited or [],
                        tier=tier, include_pdf_base64=include_pdf_base64)


def check_access(api_key: str = ""):
    return _shared_check_access(api_key)


FREE_DAILY_LIMIT = 10
_usage: dict[str, list[datetime]] = defaultdict(list)
STRIPE_199 = "https://buy.stripe.com/14A4gB3K4eUWgYR56o8k836"
STRIPE_1499 = "https://buy.stripe.com/4gM9AV80kaEG0ZT42k8k837"
STRIPE_5K = "https://buy.stripe.com/4gM7sN2G0bIKeQJfL28k833"


def _rl(tier="free") -> Optional[str]:
    if tier in ("pro", "professional", "enterprise"):
        return None
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=1)
    _usage["anonymous"] = [t for t in _usage["anonymous"] if t > cutoff]
    if len(_usage["anonymous"]) >= FREE_DAILY_LIMIT:
        return f"Free tier limit ({FREE_DAILY_LIMIT}/day). Pro £199/mo: {STRIPE_199}"
    _usage["anonymous"].append(now)
    return None


# ── Regime classification thresholds ─────────────────────────────
REGIMES = {
    "eu_ai_act_art_73": {
        "name": "EU AI Act Article 73 — serious-incident reporting",
        "legal_basis": "Regulation (EU) 2024/1689 Article 73",
        "in_scope_if": [
            "provider or deployer of a HIGH-RISK AI system on the EU market",
            "OR general-purpose AI model with systemic risk",
        ],
        "trigger_examples": [
            "Death or serious bodily harm caused by the system",
            "Serious or irreversible disruption of critical infrastructure management",
            "Fundamental-rights infringement by the system",
            "Serious damage to property or environment",
        ],
        "clock_initial": "Without undue delay, and no later than 15 days after the provider or deployer becomes aware of the serious incident",
        "clock_final": "Further reports as required by competent authority",
        "authority": "National market-surveillance authority in each Member State where incident occurred",
        "notification_form": "National notification form + EU AI Office template (being published)",
    },
    "dora_art_19": {
        "name": "DORA Article 19 — major ICT incident reporting",
        "legal_basis": "Regulation (EU) 2022/2554 Article 19 + Commission Delegated Reg (EU) 2024/1772",
        "in_scope_if": [
            "financial entity per DORA Article 2 (credit institutions, payment institutions, investment firms, insurance undertakings, crypto-asset service providers, crowdfunding platforms, etc.)",
            "OR critical ICT third-party service provider (CTPP)",
        ],
        "trigger_examples": [
            "Incident classified 'major' per Delegated Reg 2024/1772 — customers affected ≥100k OR duration ≥24h (or 2h for critical function) OR economic impact ≥€100k OR data confidentiality breach OR cross-border impact",
        ],
        "clock_initial": "4 hours from classification as major",
        "clock_intermediate": "72 hours from classification",
        "clock_final": "1 month from classification",
        "authority": "National financial competent authority (BaFin, AMF, Banca d'Italia, FCA/PRA during transitional period, etc.)",
        "notification_form": "ESMA/EBA/EIOPA harmonised reporting templates (Commission Implementing Regulation)",
    },
    "nis2_art_23": {
        "name": "NIS2 Article 23 — significant incident reporting",
        "legal_basis": "Directive (EU) 2022/2555 Article 23 (as transposed)",
        "in_scope_if": [
            "Essential or important entity under NIS2 Annex I/II (18 sectors)",
        ],
        "trigger_examples": [
            "Significant impact on service provision",
            "Capable of causing substantial operational / financial loss",
            "Potentially affecting other natural/legal persons with material damage",
        ],
        "clock_early_warning": "24 hours from awareness",
        "clock_incident_notification": "72 hours from awareness",
        "clock_final": "1 month from incident notification",
        "clock_progress": "Up to 3 months if competent authority requests",
        "authority": "National CSIRT + competent authority (BSI, ANSSI, ACN, NCSC-NL, DNSC, etc.)",
        "notification_form": "National competent-authority form",
    },
    "gdpr_art_33": {
        "name": "GDPR Article 33 — personal-data breach notification",
        "legal_basis": "Regulation (EU) 2016/679 Article 33",
        "in_scope_if": [
            "Controller experiences a personal-data breach",
            "UNLESS breach is unlikely to result in a risk to rights/freedoms of natural persons",
        ],
        "trigger_examples": [
            "Confidentiality breach (unauthorised disclosure)",
            "Integrity breach (unauthorised alteration)",
            "Availability breach (unauthorised loss of access or destruction)",
        ],
        "clock_initial": "72 hours from awareness",
        "clock_final": "Without undue delay if subject notification required (Article 34)",
        "authority": "Supervisory authority in each EU Member State (ICO in UK, CNIL in FR, BfDI in DE, etc.)",
        "notification_form": "Supervisory-authority specific (most have online forms)",
    },
    "iso_42001_clause_9": {
        "name": "ISO/IEC 42001 clause 9 — AIMS monitoring + internal incident",
        "legal_basis": "ISO/IEC 42001:2023 clauses 9.1-9.3 + Annex A control A.9",
        "in_scope_if": [
            "Organisation certified or self-declaring to ISO/IEC 42001 AI management system",
        ],
        "trigger_examples": [
            "AI system incident falling outside AIMS risk acceptance criteria",
            "Repeated deviation from AI objectives",
        ],
        "clock_initial": "Per internal AIMS procedure (typically 24-48h to internal governance committee)",
        "authority": "Internal — Certification Body notified at next audit cycle",
        "notification_form": "Internal AIMS incident register + management review input",
    },
    "uk_ai_safety_institute": {
        "name": "UK AISI voluntary incident reporting (frontier models)",
        "legal_basis": "Voluntary MoU — frontier AI safety commitments",
        "in_scope_if": [
            "Developer of a 'frontier' general-purpose AI model that has signed the Bletchley/Seoul commitments or similar",
        ],
        "trigger_examples": [
            "Capability surprise beyond pre-deployment evaluation",
            "Material misuse incident",
            "Safety-relevant deployment outcome",
        ],
        "clock_initial": "Without undue delay per voluntary MoU (typically 14 days)",
        "authority": "UK AI Safety Institute (AISI)",
        "notification_form": "AISI direct engagement (contact: aisi@dsit.gov.uk)",
    },
}


mcp = FastMCP(
    "ai-incident-reporting",
    instructions=(
        "MEOK AI Labs AI Incident Reporting MCP. Given a single incident description + your "
        "entity type, returns the FULL DECISION TREE of which regimes require notification "
        "(EU AI Act Art 73, DORA, NIS2, GDPR, ISO 42001, UK AISI), with deadlines, authorities, "
        "and notification form references. Ask me to classify an incident, list active clocks, "
        "or generate a signed incident-response attestation."
    ),
)


@mcp.tool()
def classify_incident(
    entity_type: str,
    incident_description: str,
    affected_people_count: int = 0,
    duration_hours: float = 0,
    economic_impact_eur: float = 0,
    personal_data_breached: bool = False,
    cross_border: bool = False,
    is_high_risk_ai: bool = False,
    is_financial_entity: bool = False,
    is_nis2_entity: bool = False,
    is_iso42001_certified: bool = False,
    is_frontier_model_developer: bool = False,
    api_key: str = "",
) -> str:
    """Classify an incident against every regime in scope. Returns the multi-regime
    decision tree: which clocks start, who to notify, on what form, by when."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": STRIPE_199})
    if err := _rl(tier):
        return json.dumps({"error": err, "upgrade_url": STRIPE_199})

    now = datetime.now(timezone.utc)
    triggered = {}

    # EU AI Act Article 73
    if is_high_risk_ai:
        triggered["eu_ai_act_art_73"] = {
            **REGIMES["eu_ai_act_art_73"],
            "initial_deadline_utc": (now + timedelta(days=15)).isoformat(),
            "triggered_because": "entity declared in-scope high-risk AI system",
        }

    # DORA
    dora_triggers = []
    if affected_people_count >= 100_000:
        dora_triggers.append(f"customers affected ≥100k (actual {affected_people_count})")
    if duration_hours >= 24:
        dora_triggers.append(f"duration ≥24h (actual {duration_hours}h)")
    if economic_impact_eur >= 100_000:
        dora_triggers.append(f"economic impact ≥€100k (actual €{economic_impact_eur})")
    if personal_data_breached:
        dora_triggers.append("data confidentiality breach")
    if cross_border:
        dora_triggers.append("cross-border impact")
    if is_financial_entity and dora_triggers:
        triggered["dora_art_19"] = {
            **REGIMES["dora_art_19"],
            "initial_deadline_utc": (now + timedelta(hours=4)).isoformat(),
            "intermediate_deadline_utc": (now + timedelta(hours=72)).isoformat(),
            "final_deadline_utc": (now + timedelta(days=30)).isoformat(),
            "triggered_because": dora_triggers,
        }

    # NIS2
    if is_nis2_entity:
        triggered["nis2_art_23"] = {
            **REGIMES["nis2_art_23"],
            "early_warning_deadline_utc": (now + timedelta(hours=24)).isoformat(),
            "incident_notification_deadline_utc": (now + timedelta(hours=72)).isoformat(),
            "final_deadline_utc": (now + timedelta(days=30)).isoformat(),
            "triggered_because": "NIS2 essential/important entity — assess significance threshold under national transposition",
        }

    # GDPR
    if personal_data_breached:
        triggered["gdpr_art_33"] = {
            **REGIMES["gdpr_art_33"],
            "initial_deadline_utc": (now + timedelta(hours=72)).isoformat(),
            "triggered_because": "personal-data breach — Article 33 notification required unless risk-assessment rules it out",
        }

    # ISO 42001
    if is_iso42001_certified:
        triggered["iso_42001_clause_9"] = {
            **REGIMES["iso_42001_clause_9"],
            "initial_deadline_utc": (now + timedelta(hours=48)).isoformat(),
            "triggered_because": "ISO/IEC 42001 AIMS — log to internal incident register",
        }

    # UK AISI voluntary
    if is_frontier_model_developer:
        triggered["uk_ai_safety_institute"] = {
            **REGIMES["uk_ai_safety_institute"],
            "initial_deadline_utc": (now + timedelta(days=14)).isoformat(),
            "triggered_because": "Frontier AI safety voluntary commitment",
        }

    if not triggered:
        return json.dumps({
            "incident_description": incident_description,
            "regimes_triggered": [],
            "note": "No reporting regimes triggered based on provided flags. Still run an internal post-incident review and retain evidence.",
            "upsell_pro": f"Pro £199/mo auto-generates notifications for all triggered regimes: {STRIPE_199}" if tier == "free" else None,
        }, indent=2)

    tightest = None
    for reg, data in triggered.items():
        candidates = [
            data.get("initial_deadline_utc"),
            data.get("early_warning_deadline_utc"),
        ]
        for c in candidates:
            if c and (tightest is None or c < tightest):
                tightest = c

    return json.dumps({
        "incident_description": incident_description,
        "assessed_at_utc": now.isoformat(),
        "entity_type": entity_type,
        "regimes_triggered": list(triggered.keys()),
        "regimes_detail": triggered,
        "tightest_deadline_utc": tightest,
        "critical_next_action": (
            f"Tightest deadline is {tightest}. Treat as the master SLA for your incident-response runbook."
        ),
        "upsell_pro": f"Pro £199/mo: signed multi-regime incident cert + auto-generated notification templates: {STRIPE_199}" if tier == "free" else None,
    }, indent=2)


@mcp.tool()
def list_regime_clocks(api_key: str = "") -> str:
    """List the reporting clocks + authorities for every regime this MCP covers."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": STRIPE_199})
    return json.dumps({"regimes": REGIMES}, indent=2)


@mcp.tool()
def sign_incident_response_attestation(
    entity_name: str,
    incident_id: str,
    response_score: float,
    regimes_notified_csv: str = "",
    findings_csv: str = "",
    include_pdf_base64: bool = False,
    api_key: str = "",
) -> str:
    """Generate a cryptographically signed AI incident-response attestation (Pro+).

    Captures: which regimes were notified, within which SLAs, what the response score
    was. Auditors consume the verify_url as evidence of post-incident compliance.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": STRIPE_199})
    if tier == "free":
        return json.dumps({
            "error": "Signed attestations require Pro (£199/mo) or Enterprise tier.",
            "upgrade_url": STRIPE_199,
        })
    findings = [f.strip() for f in findings_csv.split(",") if f.strip()]
    regimes = [r.strip() for r in regimes_notified_csv.split(",") if r.strip()]
    cert = _attestation(
        regulation="AI incident reporting (EU AI Act Art 73 / DORA Art 19 / NIS2 Art 23 / GDPR Art 33 / ISO 42001 / AISI)",
        entity=f"{entity_name} — incident {incident_id}",
        score=response_score,
        findings=findings or [f"Incident {incident_id} response score: {response_score}"],
        articles_audited=regimes or list(REGIMES.keys()),
        tier=tier,
        include_pdf_base64=include_pdf_base64,
        api_key=api_key,
    )
    return json.dumps(cert, indent=2)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
