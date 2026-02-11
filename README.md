# ☁️ CloudOps Unified Portal — 7 Gen AI Features

Azure multi-subscription management with **7 AI-powered features** built on Claude (Anthropic).

## 🧠 7 AI Features

| # | Feature | Module | What It Does |
|---|---------|--------|-------------|
| 1 | **NL → IaC Generator** | Provisioning | Describe infra in English → Bicep/Terraform with PE, diagnostics, tags |
| 2 | **Ops Chatbot / Copilot** | Chat Interface | Natural language queries about your Azure environment |
| 3 | **Resource Drift Detector** | Drift | ARM live state vs IaC repo → auto-fix PRs |
| 4 | **Access Anomaly / RBAC AI** | Identity | Stale SPNs, over-privilege, least-privilege recommendations |
| 5 | **Network Posture Analyzer** | Network | NSG/FW/UDR vs CIS benchmarks, auto topology, rule conflicts |
| 6 | **FinOps AI Engine** | Cost | Cost anomalies, forecast, rightsizing, orphan cleanup |
| 7 | **Risk Scorer + Auto-Approve** | Approvals | Score 1-10, auto-approve low risk, SLA-tracked chains |

## 🚀 Deploy to Streamlit Cloud

### Step 1: Push to GitHub
```bash
unzip cloudops-portal.zip && cd cloudops-portal
git init && git add . && git commit -m "CloudOps Portal v2 - 7 AI Features"
git remote add origin https://github.com/<your-user>/cloudops-portal.git
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. **New app** → Select repo → Branch: `main` → File: `app.py`
3. Click **Deploy** (2-3 min)

### Step 3: Enable AI (Optional)
App menu → **Settings** → **Secrets** → Add:
```
ANTHROPIC_API_KEY = "sk-ant-..."
```

> Portal works fully without API key — AI features use smart fallback templates. API key enables live AI responses.

## 🏗️ Tech Stack
- **Frontend:** Streamlit (Python)
- **Charts:** Plotly
- **AI:** Anthropic Claude API (claude-sonnet-4-20250514)
- **Data:** Pandas + simulated Azure data

## 📊 Personas
Cloud Engineer · Network Admin · Security Admin · FinOps Analyst · DevOps Engineer · App Owner
