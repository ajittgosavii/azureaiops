# CloudOps Unified Platform — Solution Architecture App

Production-grade Streamlit application implementing the **CloudOps Solution Architecture v2** SVG.
Maps all **6 architecture layers** with **7 Gen AI features**.

## Architecture Layers → Navigation

| Page | SVG Row | Content |
|---|---|---|
| ① Presentation Layer | Row 1 | Users, Portal (React SPA), APIM, Entra ID, Governance |
| ② Application Services | Row 2 | 7 Backend Microservices + State/Messaging + Security |
| ③ Gen AI Engine | Row 3 | **7 AI Features** (NL→IaC, Chatbot, Drift, Access, Network, FinOps, Risk Scorer) |
| ④ Orchestration + IaC | Row 4 | Logic Apps, DevOps/GitHub, ARM, AI Search RAG, Notifications |
| ⑤ Landing Zone Network | Row 5 | Hub-Spoke (Hub, Prod, Dev/Test, Data Platform, On-Premises) |
| ⑥ Data Flow + Outcomes | Row 6 | Oracle→ADF→Informatica→SQL MI→AI→PBI, Business Outcomes |

## 7 AI Features (Tab Interface in Page ③)

| # | Feature | Domain | Key Capabilities |
|---|---|---|---|
| 1 | NL→IaC Generator | Provisioning+Sandbox | Guided form + NL → Bicep with PE/diag/tags |
| 2 | Ops Chatbot | Env Provisioning | Chat UI, quick actions, RAG-powered responses |
| 3 | Drift Detector | Azure Resources | ARM vs IaC comparison, auto-fix PRs |
| 4 | Access Anomaly | Identity & Access | Stale SPNs, impossible travel, over-priv |
| 5 | Network Posture | Network Security | CIS benchmarks, topology, remediation CLI |
| 6 | FinOps AI | FinOps & Cost | Anomaly detect, forecast, rightsizing, RI recs |
| 7 | Risk Scorer | Approvals | 1-10 scoring, 3-tier routing, auto-approve |

## Quick Start

```bash
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit secrets.toml with your ANTHROPIC_API_KEY (optional — works offline)
streamlit run app.py
```

## Features

- **Production-grade CSS**: Min 12px fonts, explicit font-family, Google Fonts via `<link>`
- **Full offline mode**: Rich fallback scenarios for all 7 AI features
- **Live AI**: Add ANTHROPIC_API_KEY for Claude-powered responses
- **Interactive**: Forms, chat, expanders, Plotly charts, approval workflows
- **6 personas**: Cloud Engineer, Network Admin, Security Admin, FinOps Analyst, DevOps Engineer, App Owner
