# CloudOps Unified Portal v3 — FutureMinds

Production-grade Streamlit app aligned to the **Multi-Subscription Provisioning SVG diagram** with 6 numbered sections and 7 AI features.

## Navigation (mirrors SVG sections)

| Section | SVG Row | App Page | Content |
|---------|---------|----------|---------|
| ① Who Requests | Personas + Auth | 6 persona cards, auth flow | Cloud Eng, Network, Security, FinOps, DevOps, App Owner |
| ② Portal + AI Engine | Portal + 7 AI chips | 7 AI feature tabs | All features with full scenarios |
| ③ Risk Routing | Decision Diamond | 3-tier cards + simulator | Low/Med/High with factor breakdown |
| ④ Pipeline Execution | 5-stage chain | Stage-by-stage detail | Lint, Policy, Plan, Deploy, Validate |
| ⑤ Landing Zone Spokes | 5 subscriptions | Spoke cards + inventory | Hub, Prod, Dev/Test, Data, Sandbox |
| ⑥ Business Outcomes | 6 metric cards | Before/after + compliance | 40%, 60%, $156K, 50%, 96.2%, 100% |

## 7 AI Features (in Section ② tabs)

| # | Feature | Scenarios |
|---|---------|-----------|
| 1 | NL→IaC Generator | Guided form + NL input, Bicep with PE/diagnostics/tags |
| 2 | Ops Chatbot | 4 quick-actions, context-aware fallbacks |
| 3 | Drift Detector | 6 scenarios: NSG bypass, TLS downgrade, KV, VM resize, storage, AKS |
| 4 | Access Anomaly | 5 scenarios: stale SPN, impossible travel, over-priv, inactive, PIM |
| 5 | Network Posture | 5 CIS findings + topology + remediation CLI |
| 6 | FinOps AI | 5 savings ($13K/mo), cost breakdown, forecast, anomalies |
| 7 | Risk Scorer | 3 pending approvals, factor breakdown, scoring log, simulator |

## Deploy

```bash
pip install -r requirements.txt
streamlit run app.py
# Optional: add ANTHROPIC_API_KEY in .streamlit/secrets.toml for live AI
```
