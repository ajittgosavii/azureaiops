# ☁️ CloudOps Unified Portal — FutureMinds

Production-grade Azure multi-subscription management portal with **7 AI-powered features** built on Claude (Anthropic).

## 🧠 7 AI Features with Scenario Coverage

| # | Feature | Scenarios Included | Key Capabilities |
|---|---------|-------------------|------------------|
| 1 | **NL → IaC Generator** | AKS cluster provisioning, SQL Database, Storage, GPU VMs | Form + NL input → Bicep with PE, diagnostics, tags, Managed Identity |
| 2 | **Ops Chatbot / Copilot** | Untagged resources, over-provisioned VMs, PIM expiry, IaC generation | RAG context: runbooks, env configs, cost data. 4 quick-action templates |
| 3 | **Resource Drift Detector** | 6 scenarios: NSG rule bypass, TLS downgrade, Key Vault soft-delete, VM resize, storage exposure, AKS manual scale | Auto-fix PR, accept drift, full diff view |
| 4 | **Access Anomaly / RBAC AI** | Stale SPN (127d), impossible travel (Russia), over-priv CI/CD, inactive group members, unusual PIM activation, expiring roles | Least-privilege recs, sign-in heatmap, incident creation |
| 5 | **Network Posture Analyzer** | SSH open to internet, storage public access, FW wildcard outbound, missing flow logs, missing force-tunnel UDR | CIS benchmarks, auto-topology generation, FW conflict matrix, remediation CLI |
| 6 | **FinOps AI Engine** | VM rightsizing ($4.2K), RI conversion ($3.6K), orphan cleanup ($2.2K), auto-pause ($1.8K), Spot VM ($1.1K) | Cost breakdown, 30-day forecast, anomaly detection with root cause |
| 7 | **Risk Scorer + Approvals** | 3 pending: Cosmos DB PE (8.1), ETL SPN access (5.3), GPU VM (8.6) | Score breakdown per factor, 3-tier routing, scoring activity log |

## 🚀 Deploy

```bash
# 1. Push to GitHub
unzip cloudops-portal-v3.zip && cd cloudops-portal
git init && git add . && git commit -m "CloudOps Portal v3 - FutureMinds"
git remote add origin https://github.com/<you>/cloudops-portal.git && git push -u origin main

# 2. Deploy on Streamlit Cloud
# → share.streamlit.io → New app → Select repo → Branch: main → File: app.py → Deploy

# 3. (Optional) Enable live AI
# App menu → Settings → Secrets → Add: ANTHROPIC_API_KEY = "sk-ant-..."
```

> Works fully without API key — all 7 features use rich fallback scenarios. API key enables live Claude responses.

## 🏗️ Tech Stack
- **Frontend:** Streamlit 1.32+ with custom CSS (DM Sans + JetBrains Mono)
- **Charts:** Plotly Express + Graph Objects
- **AI:** Anthropic Claude API (claude-sonnet-4-20250514)
- **Data:** Pandas + NumPy + simulated Azure operational data

## 👤 7 Personas
Cloud Engineer · Network Admin · Security Admin · FinOps Analyst · DevOps Engineer · App Owner · Platform Lead
