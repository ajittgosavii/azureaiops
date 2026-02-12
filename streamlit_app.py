import streamlit as st, plotly.graph_objects as go, plotly.express as px, pandas as pd, numpy as np
import json, random, time

# ════════════════════════════════════════════════════════════════
# CONFIG
# ════════════════════════════════════════════════════════════════
ORG="FutureMinds"; TENANT="futureminds.onmicrosoft.com"; PROJECT="Meridian-Analytics"
F="'DM Sans','Segoe UI',system-ui,sans-serif"; M="'JetBrains Mono','Consolas',monospace"
st.set_page_config(page_title=f"CloudOps — {ORG}",page_icon="☁️",layout="wide",initial_sidebar_state="expanded")

# ════════════════════════════════════════════════════════════════
# CSS — Google Fonts via <link>, never @import. Min 12px everywhere
# ════════════════════════════════════════════════════════════════
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
html,body,[class*="css"]{font-family:'DM Sans','Segoe UI',system-ui,sans-serif}
.main .block-container{padding:1rem 2rem 2rem}
section[data-testid="stSidebar"]>div:first-child{background:linear-gradient(180deg,#0C1929,#0F172A)}
section[data-testid="stSidebar"] p,section[data-testid="stSidebar"] span,section[data-testid="stSidebar"] label{color:#CBD5E1!important}
section[data-testid="stSidebar"] hr{border-color:#1E293B!important}
#MainMenu,footer,.stDeployButton,div[data-testid="stToolbar"]{display:none!important}
div[data-testid="stExpander"] details{border:1px solid #E2E8F0!important;border-radius:10px!important;box-shadow:0 1px 3px rgba(0,0,0,.06)!important}
div[data-testid="stTabs"] button{font-family:'DM Sans','Segoe UI',sans-serif!important;font-size:14px!important;font-weight:600!important}
</style>""",unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# HELPERS — explicit font-family on every element
# ════════════════════════════════════════════════════════════════
def K(l,v,d=None,dr="u"):
    dh=""
    if d:
        bg,fg=("#D1FAE5","#065F46") if dr=="u" else ("#FEE2E2","#991B1B")
        dh=f'<div style="font-size:12px;padding:3px 10px;border-radius:10px;display:inline-block;margin-top:6px;font-weight:600;background:{bg};color:{fg};font-family:{F}">{d}</div>'
    return f'<div style="background:#FFF;border:1px solid #E2E8F0;border-radius:10px;padding:18px;text-align:center;box-shadow:0 1px 3px rgba(0,0,0,.06);font-family:{F}"><div style="font-size:12px;color:#94A3B8;text-transform:uppercase;letter-spacing:1px;font-weight:600">{l}</div><div style="font-size:28px;font-weight:800;color:#0078D4;margin:6px 0">{v}</div>{dh}</div>'

def B(s):
    m={"Pass":"#D1FAE5,#065F46","Low":"#D1FAE5,#065F46","Healthy":"#D1FAE5,#065F46","Deployed":"#D1FAE5,#065F46","Auto-Approved":"#D1FAE5,#065F46","Approved":"#D1FAE5,#065F46","Resolved":"#D1FAE5,#065F46",
       "Medium":"#FEF3C7,#92400E","Pending":"#FEF3C7,#92400E","Warning":"#FEF3C7,#92400E","Awaiting":"#FEF3C7,#92400E","Open":"#FEF3C7,#92400E",
       "High":"#FEE2E2,#991B1B","Critical":"#FEE2E2,#991B1B","Drift":"#FEE2E2,#991B1B","Rejected":"#FEE2E2,#991B1B","Stale":"#FEE2E2,#991B1B","Anomaly":"#FEE2E2,#991B1B","Over-privileged":"#FEE2E2,#991B1B",
       "AI":"#EDE7F6,#4527A0"}
    bg,fg=m.get(s,"#E3F2FD,#0C4A6E").split(",")
    return f'<span style="padding:4px 12px;border-radius:12px;font-size:12px;font-weight:600;display:inline-block;background:{bg};color:{fg};font-family:{F}">{s}</span>'

def AI(n): return f'<span style="background:linear-gradient(135deg,#EDE7F6,#F3E5F5);border:1px solid #B39DDB;border-radius:8px;padding:5px 14px;font-size:12px;font-weight:700;color:#4527A0;display:inline-block;font-family:{F}">AI #{n}</span>'
def RB(t,lv="ok"):
    b={"ok":"#107C10","wn":"#D97706","cr":"#E74856"};bg={"ok":"#F0FDF4","wn":"#FFFBEB","cr":"#FEF2F2"}
    return f'<div style="padding:14px 18px;margin:8px 0;border-radius:0 8px 8px 0;font-size:14px;line-height:1.6;background:{bg[lv]};border-left:4px solid {b[lv]};font-family:{F}">{t}</div>'
def SI(s): return {"Critical":"🔴","High":"🟠","Medium":"🟡","Low":"🟢"}.get(s,"⚪")
def SEC(label,color):
    return f'<div style="font-size:13px;font-weight:700;letter-spacing:1.5px;color:{color};border-bottom:2px solid {color}22;padding-bottom:6px;margin-bottom:14px;font-family:{F}">{label}</div>'
def CARD(title,items,tc="#0078D4",bg="#E3F2FD",bc="#90CAF9"):
    body="".join(f'<div style="font-size:13px;color:#333;font-family:{M};line-height:1.8">{i}</div>' for i in items)
    return f'<div style="background:{bg};border:1px solid {bc};border-radius:8px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,.06);height:100%"><div style="padding:12px 16px;font-size:14px;font-weight:700;color:{tc};font-family:{F};border-bottom:1px solid {bc}">{title}</div><div style="background:#FFF;margin:0 8px 8px;border-radius:6px;padding:12px 14px">{body}</div></div>'

BICEP="""// Bicep — {rt} + PE + Diagnostics | {org}
param location string = resourceGroup().location
param name string = '{name}'
var tags = {{ environment: '{env}'; costCenter: '{cc}'; project: '{proj}'; managedBy: 'CloudOps-AI' }}

resource res 'Microsoft.{ns}@2024-01-01' = {{
  name: name
  location: location
  tags: tags
  identity: {{ type: 'SystemAssigned' }}
  properties: {{
    publicNetworkAccess: 'Disabled'
    minimalTlsVersion: '1.2'
  }}
}}
resource pe 'Microsoft.Network/privateEndpoints@2024-01-01' = {{
  name: '${{name}}-pe'
  location: location
  tags: tags
  properties: {{
    subnet: {{ id: subnetId }}
    privateLinkServiceConnections: [{{ name: '${{name}}-pls'; properties: {{ groupIds: ['{grp}']; privateLinkServiceId: res.id }} }}]
  }}
}}
resource diag 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {{
  name: '${{name}}-diag'
  scope: res
  properties: {{ workspaceId: logAnalyticsId; metrics: [{{ category: 'AllMetrics'; enabled: true }}] }}
}}"""

def gen_bicep(rt,cfg):
    ns_map={"Virtual Machine":"Compute/virtualMachines","Azure SQL Database":"Sql/servers","Storage Account":"Storage/storageAccounts","AKS Cluster":"ContainerService/managedClusters","Cosmos DB":"DocumentDB/databaseAccounts"}
    grp_map={"Virtual Machine":"","Azure SQL Database":"sqlServer","Storage Account":"blob","AKS Cluster":"management","Cosmos DB":"Sql"}
    try:
        import anthropic
        k=st.secrets.get("ANTHROPIC_API_KEY")
        if k:
            r=anthropic.Anthropic(api_key=k).messages.create(model="claude-sonnet-4-20250514",max_tokens=1024,system="Generate production Bicep. Include PE, diagnostics, tags, Managed Identity. Code only.",messages=[{"role":"user","content":f"Resource: {rt}, Config: {json.dumps(cfg)}"}]).content[0].text
            if r: return r
    except: pass
    return BICEP.format(rt=rt,org=ORG,name=cfg.get("name","res-01"),env=cfg.get("env","dev"),cc=cfg.get("cc","IT-Platform"),proj=PROJECT,ns=ns_map.get(rt,"Compute/virtualMachines"),grp=grp_map.get(rt,""))

def call_ai(prompt,sys="You are an Azure CloudOps AI assistant. Be concise and technical."):
    try:
        import anthropic
        k=st.secrets.get("ANTHROPIC_API_KEY")
        if not k: return None
        return anthropic.Anthropic(api_key=k).messages.create(model="claude-sonnet-4-20250514",max_tokens=1024,system=sys,messages=[{"role":"user","content":prompt}]).content[0].text
    except: return None

# ════════════════════════════════════════════════════════════════
# SESSION STATE
# ════════════════════════════════════════════════════════════════
if "init" not in st.session_state:
    st.session_state.init=True; st.session_state.persona="Cloud Engineer"; st.session_state.chat=[]
    st.session_state.reqs=[
        {"id":"REQ-2601","type":"Provision","desc":"AKS cluster for Meridian (3-node, private API)","status":"Deployed","risk":"High","score":7.4,"date":"2026-02-03","sub":"Production","by":"Cloud Engineer"},
        {"id":"REQ-2602","type":"Network","desc":"PE for Cosmos DB multi-region (East US 2 + West Europe)","status":"Pending","risk":"High","score":8.1,"date":"2026-02-11","sub":"Production","by":"Network Admin"},
        {"id":"REQ-2603","type":"Access","desc":"Contributor on rg-meridian-data for ETL SPN","status":"AI Review","risk":"Medium","score":5.3,"date":"2026-02-11","sub":"Data Platform","by":"DevOps Engineer"},
        {"id":"REQ-2604","type":"Firewall","desc":"Allow outbound HTTPS to Snowflake endpoints","status":"Approved","risk":"Medium","score":4.8,"date":"2026-02-09","sub":"Hub","by":"Network Admin"},
        {"id":"REQ-2605","type":"Provision","desc":"Dev sandbox SQL+Redis (14d TTL)","status":"Auto-Approved","risk":"Low","score":1.9,"date":"2026-02-10","sub":"Dev/Test","by":"App Owner"},
        {"id":"REQ-2606","type":"Access","desc":"Reader for PwC auditor on compliance RG","status":"Auto-Approved","risk":"Low","score":2.1,"date":"2026-02-08","sub":"Production","by":"Security Admin"},
        {"id":"REQ-2607","type":"Provision","desc":"GPU VM (NC6s_v3) for ML training","status":"Pending","risk":"High","score":8.6,"date":"2026-02-11","sub":"Data Platform","by":"Cloud Engineer"},
    ]
    st.session_state.approvals=[
        {"id":"APR-101","req":"REQ-2602","type":"Network","desc":"PE for Cosmos DB multi-region","score":8.1,"level":"High",
         "ai":"Config aligns with PE standards. 2 PEs + 2 DNS zones. +$73/mo. Requires Network + Security review.",
         "factors":{"Environment":"Production (+3)","Resource":"Cosmos multi-region (+2)","Network":"Cross-region (+2)","Template":"Standard PE (+0)"},"status":"Awaiting"},
        {"id":"APR-102","req":"REQ-2603","type":"Access","desc":"Contributor for ETL SPN","score":5.3,"level":"Medium",
         "ai":"Contributor overly broad. Recommend custom role 'Data Pipeline Operator'. 90-day PIM expiry.",
         "factors":{"Environment":"Data Platform (+1)","Permission":"Contributor (+2)","Scope":"RG (+1)","Identity":"SPN (+1)"},"status":"Awaiting"},
        {"id":"APR-103","req":"REQ-2607","type":"Provision","desc":"GPU VM NC6s_v3 for ML","score":8.6,"level":"High",
         "ai":"$1,096/mo. Recommend Spot ($329/mo, 70% savings), auto-shutdown 8PM. CTO approval required.",
         "factors":{"Environment":"Data Platform (+1)","Cost":"$1,096/mo GPU (+3)","Resource":"Compute-intensive (+2)","Policy":"GPU approval (+2)"},"status":"Awaiting"},
    ]
    st.session_state.drifts=[
        {"res":"nsg-prod-aks","type":"NSG","sub":"Production","drift":"Inbound TCP 8443 from 0.0.0.0/0","sev":"Critical","age":"1h 23m","iac":"modules/network/nsg-aks.bicep","detail":"kubectl debug port opened via Portal bypassing GitOps.","fix":"Remove rule. Scope to bastion 10.0.3.0/24."},
        {"res":"sql-meridian-prod","type":"SQL","sub":"Production","drift":"TLS downgraded 1.2→1.0","sev":"Critical","age":"3h 12m","iac":"modules/data/sql.bicep","detail":"TLS 1.0 enables BEAST/POODLE. Changed for legacy Informatica connector.","fix":"Revert TLS 1.2. Update Informatica to v10.5+."},
        {"res":"kv-hub","type":"Key Vault","sub":"Hub","drift":"Soft-delete disabled","sev":"Critical","age":"6h 45m","iac":"modules/security/kv.bicep","detail":"Allows permanent secret deletion. Policy violation.","fix":"Re-enable soft-delete 90d + purge protection."},
        {"res":"sta-datalake-raw","type":"Storage","sub":"Data Platform","drift":"publicNetworkAccess=Enabled","sev":"Critical","age":"45m","iac":"modules/data/storage.bicep","detail":"ADLS raw zone exposed. Contains unmasked PII.","fix":"Disable public access. Verify no exfiltration via logs."},
        {"res":"vm-etl-02","type":"VM","sub":"Production","drift":"SKU D4s_v5→D8s_v5 manually","sev":"Medium","age":"12h","iac":"modules/compute/vm-etl.bicep","detail":"Upsized during data spike. Avg CPU since: 18%.","fix":"Revert D4s_v5. Add auto-scale rule."},
        {"res":"aks-meridian","type":"AKS","sub":"Production","drift":"Nodes 3→7 manually","sev":"Low","age":"2d","iac":"modules/compute/aks.bicep","detail":"Scaled for v2.3 launch. Traffic normalized. 4 excess = $580/mo.","fix":"Update IaC to 3 + HPA auto-scaling."},
    ]
    st.session_state.anomalies=[
        {"sev":"Critical","id":"svc-legacy-etl-01 (SPN)","type":"Stale","finding":"Owner on Prod sub — 0 API calls in 127 days","detail":"Legacy ETL SPN decommissioned Oct 2025. Owner = full sub control.","rec":"Revoke immediately. Create new SPN with custom role if needed.","score":9.4},
        {"sev":"Critical","id":"ext-contractor-rajesh@partner.com","type":"Anomaly","finding":"Sign-in from Vladivostok 3:47AM + 4 failed MFA","detail":"Contractor based in Bangalore. Impossible travel 8,400km in 2h.","rec":"Block sign-in. Rotate credentials. Trigger security incident.","score":9.8},
        {"sev":"High","id":"svc-jenkins-deploy (SPN)","type":"Over-privileged","finding":"Contributor on 4 subs but only uses Dev/Test","detail":"CI/CD SPN has write to Prod, Hub, Data. Never deployed outside Dev/Test in 6mo.","rec":"Scope to Dev/Test only. Create separate Prod Deployer with JIT.","score":7.2},
        {"sev":"High","id":"CloudOps-Platform-Engineers (Group)","type":"Stale","finding":"3 of 8 members inactive 60+ days","detail":"alex.former@ (left), test.user@ (test), intern.2025@ (ended).","rec":"Remove 3 inactive members. Set up quarterly access review.","score":6.8},
        {"sev":"Medium","id":"dr.chen@futureminds.cloud","type":"Anomaly","finding":"PIM Owner activation 14x this week (baseline 3x)","detail":"ML lead doing GPU VM sprint. Correlates with REQ-2607.","rec":"Likely legitimate. Convert to standing ML Platform Contributor.","score":4.6},
    ]
    st.session_state.net_findings=[
        {"sev":"Critical","cis":"CIS 6.2","finding":"NSG allows SSH 22 from 0.0.0.0/0","sub":"Dev/Test","impact":"847 brute-force attempts in 24h.","rec":"Restrict to BastionSubnet 10.0.3.0/24. Enable JIT.","cmd":"az network nsg rule update -g rg-devtest --nsg-name nsg-default -n AllowSSH --source-address-prefixes 10.0.3.0/24"},
        {"sev":"Critical","cis":"CIS 3.7","finding":"Storage publicNetworkAccess=Enabled","sub":"Sandbox","impact":"Accessible from any IP. May contain derivative PII.","rec":"Disable public access. Add PE in sandbox VNet.","cmd":"az storage account update -n stasandbox -g rg-sandbox --public-network-access Disabled"},
        {"sev":"High","cis":"CIS 6.5","finding":"FW allows outbound 0.0.0.0/0:443 from Sandbox","sub":"Hub","impact":"Sandbox can reach any HTTPS endpoint. Exfiltration risk.","rec":"Replace wildcard with FQDN tags.","cmd":"az network firewall policy rule-collection-group ... --target-fqdns '*.snowflakecomputing.com'"},
        {"sev":"Medium","cis":"CIS 6.4","finding":"3 NSGs missing flow logs","sub":"Multiple","impact":"No traffic visibility for forensics.","rec":"Enable NSG flow logs v2 with 90-day retention.","cmd":"az network watcher flow-log create --nsg <id> --workspace <law-id> --enabled true"},
        {"sev":"Medium","cis":"CIS 6.1","finding":"Data Platform VNet missing UDR force-tunnel","sub":"Data Platform","impact":"Resources route directly to internet bypassing firewall.","rec":"Create UDR 0.0.0.0/0 → FW IP 10.0.1.4.","cmd":"az network route-table route create -g rg-data --route-table-name rt-data -n force-tunnel --address-prefix 0.0.0.0/0 --next-hop-ip-address 10.0.1.4"},
    ]
    st.session_state.finops=[
        {"save":"$4,280/mo","action":"Rightsize 8 Dev/Test VMs (avg CPU 11%)","detail":"D4s→D2s (4 VMs), D8s→D4s (2), NC6→NC4 (2). Based on 30-day P95.","cat":"Rightsizing","conf":"High"},
        {"save":"$3,640/mo","action":"Convert 5 Prod VMs to 1-year RI","detail":"Stable 24/7 workloads 6+ months. RI saves 38% vs PAYG.","cat":"Reserved Instance","conf":"High"},
        {"save":"$2,190/mo","action":"Delete 6 orphaned disks + 2 PIPs","detail":"Disks from deleted VMs (45+ days). PIPs with no NIC.","cat":"Orphan Cleanup","conf":"High"},
        {"save":"$1,840/mo","action":"Auto-pause Synapse SQL Pool off-hours","detail":"Runs 24/7 ($5,520/mo). Queries only 6AM-8PM weekdays. 67% idle.","cat":"Scheduling","conf":"High"},
        {"save":"$1,096/mo","action":"Switch GPU VM to Spot Instance","detail":"Fault-tolerant with checkpointing. Spot $329/mo vs $1,096 on-demand.","cat":"Spot Instance","conf":"Medium"},
    ]

# ════════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"""<div style="text-align:center;padding:20px 12px 16px;margin:-1rem -1rem 16px;background:linear-gradient(180deg,#0C2D4A,#0F172A);border-bottom:1px solid #1E3A5F">
    <div style="font-size:36px;margin-bottom:6px">☁️</div>
    <div style="font-size:17px;font-weight:800;color:#E0F2FE;font-family:{F}">CloudOps Platform</div>
    <div style="font-size:12px;color:#64748B;letter-spacing:1px;margin-top:4px;font-family:{F}">{ORG.upper()} · AZURE MULTI-SUB</div></div>""",unsafe_allow_html=True)
    st.markdown(f"""<div style="background:#1E293B;border:1px solid #334155;border-radius:8px;padding:12px 16px;margin-bottom:16px">
    <div style="font-size:12px;color:#94A3B8;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;font-family:{F}">Signed in as</div>
    <div style="font-size:15px;font-weight:600;color:#F1F5F9;font-family:{F}">{st.session_state.persona}</div>
    <div style="font-size:12px;color:#64748B;margin-top:4px;font-family:{F}">{TENANT}</div></div>""",unsafe_allow_html=True)
    st.session_state.persona=st.selectbox("Switch Persona",["Cloud Engineer","Network Admin","Security Admin","FinOps Analyst","DevOps Engineer","App Owner","Platform Lead"],label_visibility="collapsed")
    page=st.radio("Architecture Layers",["① Presentation Layer","② Application Services","③ Gen AI Engine","④ Orchestration + IaC","⑤ Landing Zone Network","⑥ Data Flow + Outcomes"],label_visibility="collapsed")
    st.markdown("---")
    st.markdown(f'<div style="font-size:12px;color:#94A3B8;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;font-weight:600;font-family:{F}">Subscription Health</div>',unsafe_allow_html=True)
    for n,s,i in [("Hub-Connectivity","Healthy","🟢"),("Prod-LandingZone","Healthy","🟢"),("Dev-Test","Healthy","🟢"),("Data-Platform","1 Advisory","🟡"),("Sandbox-POC","Healthy","🟢")]:
        st.markdown(f'<div style="display:flex;align-items:center;gap:8px;margin:6px 0;font-size:13px;font-family:{F}"><span>{i}</span><span style="color:#E2E8F0;font-weight:500">{n}</span><span style="color:#64748B;font-size:12px;margin-left:auto">{s}</span></div>',unsafe_allow_html=True)
    st.markdown("---")
    st.caption(f"CloudOps v3.0 · AI: Claude Sonnet · © 2026 {ORG}")

# ── HEADER ──
st.markdown(f"""<div style="background:linear-gradient(135deg,#002050 0%,#0078D4 50%,#00A4EF 100%);padding:18px 28px;border-radius:12px;margin-bottom:20px;display:flex;justify-content:space-between;align-items:center;box-shadow:0 4px 20px rgba(0,120,212,.25)">
<div><div style="color:#FFF;font-size:20px;font-weight:800;font-family:{F}">☁️ CloudOps Unified Platform — Solution Architecture</div>
<div style="color:rgba(255,255,255,.75);margin:4px 0 0;font-size:13px;font-family:{F}">Azure Multi-Subscription · 7 Gen AI Features · {ORG}</div></div>
<div style="text-align:right"><div style="color:#FFF;font-size:14px;font-weight:600;font-family:{F}">{st.session_state.persona}</div>
<div style="color:rgba(255,255,255,.6);font-size:12px;font-family:{F}">{TENANT}</div></div></div>""",unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# ① PRESENTATION LAYER (SVG Row 1)
# ════════════════════════════════════════════════════════════════
if page=="① Presentation Layer":
    st.markdown(SEC("① PRESENTATION LAYER — Users · Portal · APIM · Auth · Governance","#0078D4"),unsafe_allow_html=True)
    st.markdown("End users access the **CloudOps Portal** via browser or Teams, authenticated through **Entra ID SSO**, routed via **Azure API Management**, governed by **Azure Policy + Cost Management**.")

    # ── Users ──
    st.markdown("#### End Users")
    personas=[("👨‍💻","Cloud Engineer","Infra provisioning","VMs, AKS, storage, databases. Primary user of AI #1 NL→IaC.","Provision, Network"),
              ("🌐","Network Admin","PE, FW, NSG, VPN","Manages Private Endpoints, Firewall rules, NSG policies. Uses AI #5.","Network, Firewall"),
              ("🔐","Security Admin","RBAC, PIM, NSG audit","Reviews access requests, PIM activations, anomalies. Uses AI #4.","Access"),
              ("💰","FinOps Analyst","Cost, budgets, RI","Monitors spend, approves cost-impactful resources. Uses AI #6.","Cost"),
              ("⚙️","DevOps Engineer","Pipelines, IaC","Manages pipelines, drift remediation. Uses AI #3 Drift Detector.","Provision, Network"),
              ("📱","App Owner","Workload requests","Business stakeholders requesting resources. Uses AI #2 Chatbot.","Provision, Access")]
    cols=st.columns(3)
    for idx,(icon,name,scope,desc,types) in enumerate(personas):
        with cols[idx%3]:
            hl="border-left:4px solid #0078D4;" if name==st.session_state.persona else "border-left:4px solid transparent;"
            st.markdown(f"""<div style="background:#FFF;border:1px solid #E2E8F0;border-radius:10px;padding:18px;margin:8px 0;box-shadow:0 1px 3px rgba(0,0,0,.06);{hl}font-family:{F}">
            <div style="font-size:32px;margin-bottom:8px">{icon}</div>
            <div style="font-size:16px;font-weight:700;color:#0F172A">{name}</div>
            <div style="font-size:12px;color:#94A3B8;margin:4px 0 10px">{scope}</div>
            <div style="font-size:13px;color:#475569;line-height:1.6">{desc}</div>
            <div style="margin-top:10px;font-size:12px;color:#0078D4;font-weight:600">Requests: {types}</div></div>""",unsafe_allow_html=True)

    st.markdown("---")
    # ── Portal + APIM + Auth + Gov ──
    st.markdown("#### Architecture Components")
    c1,c2,c3,c4=st.columns(4)
    with c1: st.markdown(CARD("🌐 Portal Frontend",["Azure Static Web Apps","React SPA — CloudOps Portal","Dashboard | Provisioning","Network | Access | FinOps","Approvals | Compliance","AI Copilot Chat Interface"],"#2E7D32","#E8F5E9","#81C784"),unsafe_allow_html=True)
    with c2: st.markdown(CARD("🔌 Azure API Management",["Gateway + Rate Limit + Logging","/api/provision/* /api/network/*","/api/access/*   /api/finops/*","/api/approval/* /api/comply/*","/api/ai/chat   /api/ai/generate","OAuth2 JWT validation"],"#E65100","#FFF3E0","#FFB74D"),unsafe_allow_html=True)
    with c3: st.markdown(CARD("🔐 Microsoft Entra ID",["SSO + MFA (Conditional Access)","App Registration (OAuth2 PKCE)","PIM for Admin Roles","Security Groups → RBAC Map","Conditional Access Policies","Token-based API auth"],"#6A1B9A","#F3E5F5","#CE93D8"),unsafe_allow_html=True)
    with c4: st.markdown(CARD("📋 Governance",["Azure Policy (Deny+Audit)","· Allowed regions/SKUs","· Tagging enforcement","· Deny public access","Cost Management + Budgets","Defender for Cloud"],"#F57F17","#FFF8E1","#FFD54F"),unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### Authentication Flow")
    steps=[("🔑 Entra ID SSO","OAuth2 + PKCE. Corporate credentials.","#002050"),("🛡️ MFA + Conditional Access","MFA from untrusted networks. Block legacy auth.","#5C2D91"),("🔌 APIM Gateway","Rate limit, JWT validation, API routing.","#E65100"),("✅ Portal Access","Persona-scoped CloudOps Portal view.","#107C10")]
    cols=st.columns(4)
    for col,(title,desc,color) in zip(cols,steps):
        with col:
            st.markdown(f'<div style="background:{color};color:#FFF;border-radius:10px;padding:16px;text-align:center;min-height:110px;font-family:{F}"><div style="font-size:14px;font-weight:700;margin-bottom:8px">{title}</div><div style="font-size:13px;opacity:.85;line-height:1.5">{desc}</div></div>',unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# ② APPLICATION SERVICES (SVG Row 2)
# ════════════════════════════════════════════════════════════════
elif page=="② Application Services":
    st.markdown(SEC("② APPLICATION LAYER — Azure Functions (Premium VNet-Integrated) + Logic Apps","#0078D4"),unsafe_allow_html=True)
    st.markdown("7 backend microservices + state/messaging + security services. Each service maps to a CloudOps domain and an AI feature.")

    services=[
        ("① Provisioning Svc","ARM/Bicep execution, Subscription vending, Sandbox auto-cleanup","AI #1 NL→IaC","#1565C0","#E3F2FD","#90CAF9"),
        ("② Network Svc","NSG/FW rule mgmt, PE/DNS operations, Route table updates","AI #5 Net Posture","#1565C0","#E3F2FD","#90CAF9"),
        ("③ Access Svc","RBAC assignment API, PIM activation, SPN lifecycle","AI #4 Access Anomaly","#1565C0","#E3F2FD","#90CAF9"),
        ("④ FinOps Svc","Cost API aggregation, Budget enforcement, Chargeback calc","AI #6 FinOps AI","#1565C0","#E3F2FD","#90CAF9"),
        ("⑤ Approval Engine","Logic Apps workflow, Multi-level routing, Teams adaptive cards","AI #7 Risk Scorer","#1565C0","#E3F2FD","#90CAF9"),
        ("⑥ Compliance Svc","Policy eval + report, Audit trail export, Remediation tasks","—","#1565C0","#E3F2FD","#90CAF9"),
        ("⑦ Observability Svc","Alert + health API, Incident triage, SLA dashboard","—","#1565C0","#E3F2FD","#90CAF9"),
    ]
    cols=st.columns(4)
    for idx,(name,desc,ai,tc,bg,bc) in enumerate(services):
        with cols[idx%4]:
            ai_tag=f'<div style="margin-top:8px">{AI(ai.split("#")[1].strip()) if "#" in ai else ""}</div>' if ai!="—" else ""
            lines=desc.split(", ")
            body="".join(f'<div style="font-size:13px;color:#555;font-family:{M};line-height:1.7">{l}</div>' for l in lines)
            st.markdown(f"""<div style="background:{bg};border:1px solid {bc};border-radius:8px;padding:0;overflow:hidden;margin:8px 0;box-shadow:0 1px 3px rgba(0,0,0,.06)">
            <div style="padding:12px 16px;font-size:14px;font-weight:700;color:{tc};font-family:{F};border-bottom:1px solid {bc}">{name}</div>
            <div style="padding:12px 16px;background:#FFF">{body}{ai_tag}</div></div>""",unsafe_allow_html=True)

    st.markdown("---")
    c1,c2=st.columns(2)
    with c1:
        st.markdown(CARD("🗄️ State + Messaging",["Cosmos DB — request store","Service Bus — async orchestration","Redis Cache — session + caching","Event Grid — event routing"],"#00695C","#E0F2F1","#80CBC4"),unsafe_allow_html=True)
    with c2:
        st.markdown(CARD("🔒 Security Services",["Key Vault — secrets, certs, keys","Azure Monitor + Sentinel (SIEM)","Defender for Cloud — CSPM","Managed Identity — zero secrets"],"#C62828","#FCE4EC","#EF9A9A"),unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### Service Communication Matrix")
    st.dataframe(pd.DataFrame([
        {"Service":"Provisioning","Inbound":"APIM, Service Bus","Outbound":"ARM API, AI Engine #1","Auth":"Managed Identity","Protocol":"REST + Async"},
        {"Service":"Network","Inbound":"APIM, Service Bus","Outbound":"ARM API, AI Engine #5","Auth":"Managed Identity","Protocol":"REST + Async"},
        {"Service":"Access","Inbound":"APIM, Service Bus","Outbound":"Graph API, AI Engine #4","Auth":"Managed Identity","Protocol":"REST + Async"},
        {"Service":"FinOps","Inbound":"APIM, Timer Trigger","Outbound":"Cost API, AI Engine #6","Auth":"Managed Identity","Protocol":"REST + Scheduled"},
        {"Service":"Approval","Inbound":"Service Bus","Outbound":"Logic Apps, Teams, AI #7","Auth":"Managed Identity","Protocol":"Async + Webhook"},
        {"Service":"Compliance","Inbound":"APIM, Timer","Outbound":"Policy API, Sentinel","Auth":"Managed Identity","Protocol":"REST + Scheduled"},
        {"Service":"Observability","Inbound":"APIM, Alerts","Outbound":"Monitor API, ServiceNow","Auth":"Managed Identity","Protocol":"REST + Webhook"},
    ]),use_container_width=True,hide_index=True)

# ════════════════════════════════════════════════════════════════
# ③ GEN AI ENGINE — 7 AI FEATURES (SVG Row 3)
# ════════════════════════════════════════════════════════════════
elif page=="③ Gen AI Engine":
    st.markdown(SEC("③ GEN AI ENGINE — 7 AI Features (Azure OpenAI GPT-4o + AI Search RAG + Azure ML)","#5C2D91"),unsafe_allow_html=True)
    st.markdown(f"All AI features accessible via **Private Endpoint**. RAG powered by **Azure AI Search** indexing IaC templates, CIS benchmarks, runbooks, and past deployments.")

    c1,c2,c3,c4=st.columns(4)
    with c1: st.markdown(K("Requests Scored/mo","523","74% auto-approved"),unsafe_allow_html=True)
    with c2: st.markdown(K("Avg Approval Time","1.8 hrs","Was 18 hrs"),unsafe_allow_html=True)
    with c3: st.markdown(K("IaC Templates Gen'd","47/mo","+12 vs last mo"),unsafe_allow_html=True)
    with c4: st.markdown(K("Policy Compliance","96.2%","+2.1%"),unsafe_allow_html=True)

    st.markdown("---")
    tabs=st.tabs(["🏗️ #1 NL→IaC","🤖 #2 Chatbot","🔄 #3 Drift","🔐 #4 Access","🛡️ #5 Network","💰 #6 FinOps","⚡ #7 Risk Scorer"])

    # ── AI #1: NL → IaC Generator ──
    with tabs[0]:
        st.markdown(f"### {AI(1)} Natural Language → IaC Generator",unsafe_allow_html=True)
        st.markdown("**Domain:** Provisioning + Sandbox · **Input:** NL description / diagram · **Output:** Bicep / Terraform · **RAG:** IaC library + standards")
        t1,t2=st.tabs(["Guided Form","Natural Language"])
        with t1:
            with st.form("prov",border=True):
                c1,c2=st.columns(2)
                with c1:
                    rt=st.selectbox("Resource Type",["Virtual Machine","Azure SQL Database","Storage Account","AKS Cluster","Cosmos DB","Redis Cache","Function App"])
                    ts=st.selectbox("Target Subscription",["Prod-LandingZone","Dev-Test","Data-Platform","Sandbox-POC"])
                    rn=st.text_input("Resource Name",placeholder="vm-meridian-api-03")
                    env=st.selectbox("Environment",["Production","Development","Test","Sandbox"])
                with c2:
                    skus={"Virtual Machine":["Standard_D2s_v5","Standard_D4s_v5","Standard_D8s_v5","Standard_NC6s_v3 (GPU)"],"Azure SQL Database":["GP_Gen5_2","GP_Gen5_4","BC_Gen5_4"],"Storage Account":["Standard_LRS","Standard_GRS","Premium_LRS"],"AKS Cluster":["Standard_D4s_v5 (3-node)","Standard_D4s_v5 (5-node)"],"Cosmos DB":["Serverless","Provisioned 400 RU"]}
                    sku=st.selectbox("SKU",skus.get(rt,["Standard"]))
                    region=st.selectbox("Region",["East US 2 (Primary)","West Europe (DR)","Central US"])
                    cc=st.text_input("Cost Center",value="IT-Platform")
                    just=st.text_area("Justification",placeholder="Required for Meridian v2.4...",height=80)
                sub=st.form_submit_button("🚀 Generate IaC + Submit",type="primary",use_container_width=True)
                if sub and rn:
                    with st.spinner("AI generating IaC + policy pre-flight..."):
                        time.sleep(1)
                    rid=f"REQ-{random.randint(2700,2999)}"
                    risk="Low" if env in ["Development","Sandbox"] else "Medium" if env=="Test" else "High"
                    score=round(random.uniform(1.5,3.5) if risk=="Low" else random.uniform(4,6.5) if risk=="Medium" else random.uniform(7,9),1)
                    st.success(f"✅ Request **{rid}** submitted!")
                    ca,cb=st.columns(2)
                    with ca:
                        st.markdown("**Policy Pre-flight (7/7 passed):**")
                        for chk in ["✅ Region: East US 2 — ALLOWED","✅ SKU in approved catalog","✅ Naming convention validated","✅ Mandatory tags (4/4)","✅ Private Endpoint auto-attached","✅ Diagnostics auto-configured","✅ Managed Identity: SystemAssigned"]:
                            st.markdown(chk)
                    with cb:
                        st.markdown(f"**Risk Assessment:** {score}/10 {B(risk)}",unsafe_allow_html=True)
                        lv="ok" if risk=="Low" else "wn" if risk=="Medium" else "cr"
                        msgs={"Low":"✅ <strong>Auto-Approved</strong> — Pipeline triggers instantly.","Medium":"⏳ <strong>L1 Approval</strong> — Teams card sent. SLA: 4 hrs.","High":"🔒 <strong>L1+L2+CISO</strong> — Multi-level review. SLA: 24 hrs."}
                        st.markdown(RB(msgs[risk],lv),unsafe_allow_html=True)
                    st.markdown("**AI-Generated Bicep:**")
                    st.code(gen_bicep(rt,{"name":rn,"size":sku.split(" ")[0],"env":env.lower(),"cc":cc}),language="bicep")
        with t2:
            nl=st.text_area("Describe your infrastructure need:",placeholder="I need a 3-node AKS cluster in production with private API, Azure CNI...",height=120,label_visibility="collapsed")
            if st.button("Generate from Description",type="primary",use_container_width=True) and nl:
                with st.spinner("AI analyzing..."):
                    r=call_ai(f"Parse this request and generate: resource list, estimated cost, risk score, and Bicep code.\n\nRequest: {nl}")
                    if r: st.markdown(r)
                    else:
                        st.markdown("**Parsed Resources:** AKS (3-node + autoscale) $876/mo · PE $7/mo · Container Insights ~$120/mo")
                        st.markdown(f"**Risk:** 7.8/10 {B('High')} — Production AKS + custom networking = L1+L2 approval required",unsafe_allow_html=True)
                        st.code(gen_bicep("AKS Cluster",{"name":"aks-meridian-prod","size":"Standard_D4s_v5","env":"production","cc":"IT-Platform"}),language="bicep")

    # ── AI #2: Ops Chatbot ──
    with tabs[1]:
        st.markdown(f"### {AI(2)} CloudOps Copilot / Chatbot",unsafe_allow_html=True)
        st.markdown(f"**Domain:** Env Provisioning · **RAG:** Env configs + runbooks. Ask anything about {ORG}'s 5 subscriptions, 847 resources, $142K/mo spend.")
        for m in st.session_state.chat:
            if m["role"]=="user":
                st.markdown(f'<div style="background:#E3F2FD;border-radius:14px 14px 4px 14px;padding:14px 18px;margin:10px 0 10px 40px;font-size:14px;line-height:1.5;font-family:{F}">👤 {m["content"]}</div>',unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="background:#F0FDF4;border-radius:14px 14px 14px 4px;padding:14px 18px;margin:10px 40px 10px 0;font-size:14px;border-left:3px solid #107C10;line-height:1.5;font-family:{F}">🤖 {m["content"]}</div>',unsafe_allow_html=True)
        qcols=st.columns(4)
        for i,qp in enumerate(["Show untagged resources","Over-provisioned VMs?","PIM roles expiring?","Cosmos Bicep geo-rep"]):
            if qcols[i].button(qp,key=f"q_{i}",use_container_width=True):
                st.session_state.chat.append({"role":"user","content":qp}); st.rerun()
        msg=st.chat_input("Ask the CloudOps AI...")
        if msg:
            st.session_state.chat.append({"role":"user","content":msg})
            with st.spinner("Thinking..."):
                resp=call_ai(msg,f"CloudOps AI for {ORG}. 5 Azure subs, 847 resources, $142K/mo. Be concise.")
                if not resp:
                    ml=msg.lower()
                    if "untag" in ml: resp="**Untagged Resources:**\n\n| Resource | Type | Sub |\n|---|---|---|\n| vm-test-scratch-03 | VM | Sandbox |\n| disk-orphan-data-01 | Disk | Dev/Test |\n| pip-unused-02 | PIP | Sandbox |\n\n`az tag create --resource-id <id> --tags costCenter=IT-Platform environment=dev`"
                    elif "over" in ml or "provision" in ml: resp="**Over-Provisioned VMs (30d P95):**\n\n| VM | SKU | CPU | Rec | Save |\n|---|---|---|---|---|\n| vm-dev-api-01 | D4s | 8% | D2s | $73/mo |\n| vm-dev-api-02 | D4s | 12% | D2s | $73/mo |\n| vm-test-worker-01 | D8s | 6% | D4s | $146/mo |\n\n**Total: $1,059/mo savings**"
                    elif "pim" in ml: resp="**PIM Expiring This Week:**\n\n| User | Role | Scope | Expires |\n|---|---|---|---|\n| priya.s@ | Contributor | Prod | Feb 14 |\n| devon.l@ | Network Contrib | Hub | Feb 13 |"
                    elif "cosmos" in ml or "bicep" in ml: resp="```bicep\nresource cosmos 'Microsoft.DocumentDB/databaseAccounts@2024-02-15' = {\n  name: 'cosmos-meridian-prod'\n  location: 'East US 2'\n  properties: {\n    locations: [\n      { locationName: 'East US 2'; failoverPriority: 0 }\n      { locationName: 'West Europe'; failoverPriority: 1 }\n    ]\n    publicNetworkAccess: 'Disabled'\n  }\n}\n```"
                    else: resp=f"I can help with provisioning, networking, access, cost, or compliance across {ORG}'s Azure environment. Try one of the quick actions above, or add ANTHROPIC_API_KEY for live AI."
                st.session_state.chat.append({"role":"assistant","content":resp}); st.rerun()
        if st.button("Clear chat"): st.session_state.chat=[]; st.rerun()

    # ── AI #3: Drift Detector ──
    with tabs[2]:
        st.markdown(f"### {AI(3)} Resource Drift Detector",unsafe_allow_html=True)
        st.markdown("**Domain:** Azure Resources / IaC · **Input:** ARM state vs IaC repo · **Output:** Drift report + fix PR · **RAG:** Deployed templates")
        c1,c2,c3,c4=st.columns(4)
        with c1: st.markdown(K("Scanned","847","Hourly"),unsafe_allow_html=True)
        with c2: st.markdown(K("Drifted","6","3 fewer vs last wk"),unsafe_allow_html=True)
        with c3: st.markdown(K("Auto-Fixed PRs","14","This month"),unsafe_allow_html=True)
        with c4: st.markdown(K("Pending","3","Need human","dn"),unsafe_allow_html=True)
        st.markdown("---")
        for d in st.session_state.drifts:
            with st.expander(f"{SI(d['sev'])} **{d['res']}** ({d['type']}) — {d['drift'][:55]}... [{d['age']}]",expanded=d["sev"]=="Critical"):
                st.markdown(f"**Sub:** {d['sub']} · **Severity:** {B(d['sev'])} · **IaC:** `{d['iac']}`",unsafe_allow_html=True)
                st.markdown(f"**Detail:** {d['detail']}")
                lv="cr" if d["sev"]=="Critical" else "wn" if d["sev"]=="Medium" else "ok"
                st.markdown(RB(f"🤖 <strong>AI Fix:</strong> {d['fix']}",lv),unsafe_allow_html=True)
                c1,c2,c3=st.columns(3)
                if c1.button("Revert to IaC",key=f"fx_{d['res']}",use_container_width=True): st.success(f"PR #{random.randint(200,400)} created → auto-merge pipeline.")
                if c2.button("Accept Drift",key=f"ac_{d['res']}",use_container_width=True): st.info("IaC updated to match live state.")
                if c3.button("View Diff",key=f"df_{d['res']}",use_container_width=True):
                    st.code(f"--- a/{d['iac']}\n+++ b/ARM live state\n\n- // Original config\n+ // DRIFT: {d['drift']}\n+ // Changed by: Portal user ({d['age']} ago)",language="diff")

    # ── AI #4: Access Anomaly ──
    with tabs[3]:
        st.markdown(f"### {AI(4)} Access Anomaly / RBAC AI",unsafe_allow_html=True)
        st.markdown("**Domain:** Identity & Access · **Input:** Entra ID sign-in logs · **Output:** Stale SPNs, over-priv, role recommendations")
        c1,c2,c3,c4=st.columns(4)
        with c1: st.markdown(K("Identities","234","Users+SPNs+Groups"),unsafe_allow_html=True)
        with c2: st.markdown(K("Anomalies","5","Last 7 days","dn"),unsafe_allow_html=True)
        with c3: st.markdown(K("Stale","4","90+ days","dn"),unsafe_allow_html=True)
        with c4: st.markdown(K("Over-Priv","3","Recommend downgrade","dn"),unsafe_allow_html=True)
        st.markdown("---")
        t1,t2=st.tabs(["Anomaly Findings","Sign-in Heatmap"])
        with t1:
            for a in st.session_state.anomalies:
                with st.expander(f"{SI(a['sev'])} [{a['type']}] {a['id']}: {a['finding'][:60]}...",expanded=a["sev"]=="Critical"):
                    st.markdown(f"**Severity:** {B(a['sev'])} · **Type:** {B(a['type'])} · **Risk:** {a['score']}/10",unsafe_allow_html=True)
                    st.markdown(f"**Detail:** {a['detail']}")
                    lv="cr" if a["sev"]=="Critical" else "wn" if a["sev"]=="High" else "ok"
                    st.markdown(RB(f"🤖 <strong>Recommendation:</strong> {a['rec']}",lv),unsafe_allow_html=True)
                    if a["sev"] in ["Critical","High"]:
                        c1,c2=st.columns(2)
                        if c1.button("Apply Fix",key=f"af_{a['id'][:12]}",type="primary",use_container_width=True): st.success("Applied. Audit logged.")
                        if c2.button("Create Incident",key=f"ci_{a['id'][:12]}",use_container_width=True): st.info(f"ServiceNow INC-{random.randint(4800,4999)} created.")
        with t2:
            hours=list(range(24))
            normal=[3,2,1,1,0,1,6,22,48,44,40,35,32,36,42,44,38,26,14,10,8,6,5,4]
            anom=[0,0,0,4,6,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            fig=go.Figure()
            fig.add_trace(go.Bar(x=hours,y=normal,name="Normal",marker_color="#0078D4",opacity=.85))
            fig.add_trace(go.Bar(x=hours,y=anom,name="Anomalous",marker_color="#E74856"))
            fig.update_layout(height=280,margin=dict(l=0,r=0,t=10,b=0),barmode="stack",xaxis_title="Hour (UTC)",yaxis_title="Sign-ins",plot_bgcolor="white",legend=dict(orientation="h",y=-.2))
            st.plotly_chart(fig,use_container_width=True)
            st.caption("Anomalous cluster at 3–5 AM UTC = ext-contractor-rajesh impossible travel event.")

    # ── AI #5: Network Posture ──
    with tabs[4]:
        st.markdown(f"### {AI(5)} Network Posture Analyzer",unsafe_allow_html=True)
        st.markdown(f"**Domain:** Network Security · **Input:** NSG/FW/UDR configs · **RAG:** CIS benchmarks, {ORG} policies")
        c1,c2,c3,c4=st.columns(4)
        with c1: st.markdown(K("Posture Score","87/100","Up 4 this month"),unsafe_allow_html=True)
        with c2: st.markdown(K("NSGs","24","All subs"),unsafe_allow_html=True)
        with c3: st.markdown(K("FW Rules","47","5 conflicts","dn"),unsafe_allow_html=True)
        with c4: st.markdown(K("Findings","5","2 critical","dn"),unsafe_allow_html=True)
        st.markdown("---")
        t1,t2=st.tabs(["CIS Findings","Network Topology"])
        with t1:
            for f in st.session_state.net_findings:
                with st.expander(f"{SI(f['sev'])} [{f['cis']}] {f['finding']} — {f['sub']}",expanded=f["sev"]=="Critical"):
                    st.markdown(f"**Impact:** {f['impact']}")
                    lv="cr" if f["sev"]=="Critical" else "wn" if f["sev"]=="High" else "ok"
                    st.markdown(RB(f"🤖 <strong>Recommendation:</strong> {f['rec']}",lv),unsafe_allow_html=True)
                    st.code(f["cmd"],language="bash")
                    if st.button("Execute Remediation",key=f"nr_{f['cis']}",use_container_width=True): st.success("Pipeline triggered. PR created.")
        with t2:
            st.code(f"""Hub VNet (10.0.0.0/16) ─── Connectivity Subscription
├── AzureFirewallSubnet  (10.0.1.0/24)  Azure Firewall [DNAT+App+Net]
│   Private IP: 10.0.1.4 (force-tunnel target)
├── GatewaySubnet        (10.0.2.0/24)  ExpressRoute 2Gbps → On-Prem
├── AzureBastionSubnet   (10.0.3.0/24)  Bastion Host (secure VM access)
├── AppSubnet            (10.0.10.0/24) APIM + Functions + OpenAI PE
│
├── [Peering] → Prod (10.1.0.0/16)
│   ├── snet-aks   (10.1.1.0/24) AKS private API
│   ├── snet-pe    (10.1.2.0/24) SQL MI PE, Cosmos PE, Redis PE
│   └── snet-apps  (10.1.3.0/24) App Services (VNet integrated)
│
├── [Peering] → Dev/Test (10.2.0.0/16)
│   ├── snet-dev     (10.2.1.0/24) Dev VMs, UAT
│   └── snet-sandbox (10.2.2.0/24) Auto-provisioned sandboxes
│   ⚠️  NSG: SSH 0.0.0.0/0 OPEN — REMEDIATE (CIS 6.2)
│
├── [Peering] → Data Platform (10.3.0.0/16)
│   ├── snet-data (10.3.1.0/24) ADLS, Synapse, ADF, Informatica
│   └── snet-ml   (10.3.2.0/24) ML Compute (GPU)
│   ⚠️  UDR: Missing force-tunnel — REMEDIATE (CIS 6.1)
│
└── On-Premises (ExpressRoute)
    Oracle R12 | GLTM | Cognos | Encompass NV | SAP (future)""",language="text")

    # ── AI #6: FinOps AI ──
    with tabs[5]:
        st.markdown(f"### {AI(6)} FinOps AI Engine",unsafe_allow_html=True)
        st.markdown(f"**Domain:** FinOps & Cost · **Input:** Cost Management API · **Output:** Anomalies, forecast, rightsizing + RI recommendations")
        c1,c2,c3,c4=st.columns(4)
        with c1: st.markdown(K("Feb MTD","$68.4K","On track"),unsafe_allow_html=True)
        with c2: st.markdown(K("Forecast","$138.2K","$3.8K under budget"),unsafe_allow_html=True)
        with c3: st.markdown(K("AI Savings","$13.0K/mo","5 recommendations"),unsafe_allow_html=True)
        with c4: st.markdown(K("Anomalies","2","1 open","dn"),unsafe_allow_html=True)
        st.markdown("---")
        t1,t2,t3=st.tabs(["Cost Breakdown","Savings Recommendations","Anomalies"])
        with t1:
            np.random.seed(99)
            data=[]
            for s,mult in [("Production",3.2),("Data Platform",2.0),("Dev/Test",1.5),("Hub",0.9),("Sandbox",0.5)]:
                for svc in ["Compute","Database","Storage","Network","AI/ML","Other"]:
                    data.append({"Subscription":s,"Service":svc,"Cost ($K)":round(np.random.uniform(.5,8)*mult,1)})
            fig=px.bar(pd.DataFrame(data),x="Subscription",y="Cost ($K)",color="Service",color_discrete_sequence=["#0078D4","#5C2D91","#107C10","#E74856","#D97706","#64748B"])
            fig.update_layout(height=320,margin=dict(l=0,r=0,t=10,b=0),plot_bgcolor="white",legend=dict(orientation="h",y=-.2))
            st.plotly_chart(fig,use_container_width=True)
            np.random.seed(42)
            dates=pd.date_range("2026-02-01",periods=28,freq="D")
            actual=[4.8+np.random.uniform(-.3,.5) for _ in range(11)]
            forecast=[actual[-1]+(i*.12)+np.random.uniform(-.2,.2) for i in range(17)]
            fig2=go.Figure()
            fig2.add_trace(go.Scatter(x=dates[:11],y=actual,name="Actual",mode="lines+markers",line=dict(color="#0078D4",width=2.5)))
            fig2.add_trace(go.Scatter(x=dates[10:],y=[actual[-1]]+forecast,name="AI Forecast",mode="lines",line=dict(color="#5C2D91",width=2,dash="dash")))
            fig2.add_hline(y=5.1,line_dash="dot",line_color="#E74856",annotation_text="Daily Budget")
            fig2.update_layout(height=200,margin=dict(l=0,r=0,t=10,b=0),plot_bgcolor="white",legend=dict(orientation="h",y=-.3),yaxis_title="$/day (K)")
            st.plotly_chart(fig2,use_container_width=True)
        with t2:
            st.markdown("**Total Potential Savings: $13.0K/mo ($156K/yr)**")
            for rec in st.session_state.finops:
                bc="#107C10" if rec["conf"]=="High" else "#D97706"
                st.markdown(f"""<div style="background:#FFF;border:1px solid #E2E8F0;border-radius:10px;padding:20px 24px;margin:10px 0;border-left:4px solid {bc};font-family:{F}">
                <div style="display:flex;justify-content:space-between;align-items:center"><div style="font-size:15px;font-weight:700;color:#0F172A">{rec['action']}</div><span style="font-size:18px;font-weight:800;color:#107C10">{rec['save']}</span></div>
                <div style="font-size:12px;color:#94A3B8;margin:6px 0 8px">{rec['cat']} · Confidence: {B(rec['conf'])}</div>
                <div style="font-size:13px;color:#475569;line-height:1.5">{rec['detail']}</div></div>""",unsafe_allow_html=True)
                if st.button(f"Apply: {rec['cat']}",key=f"fn_{rec['save']}",use_container_width=True): st.success("Optimization applied!")
        with t3:
            st.markdown(RB("🚨 <strong>OPEN — Data Platform:</strong> Synapse SQL Pool spend spiked 42% ($187→$266 in 24h). Auto-pause job failed (expired credential). Excess: ~$340/day.<br><strong>AI Fix:</strong> Credential rotated. Auto-pause re-enabled.","cr"),unsafe_allow_html=True)
            st.markdown(RB("✅ <strong>RESOLVED — Sandbox:</strong> Spend dropped to $0 (from $28/day avg). Auto-cleanup removed all resources per 14-day TTL. Expected behavior.","ok"),unsafe_allow_html=True)

    # ── AI #7: Risk Scorer ──
    with tabs[6]:
        st.markdown(f"### {AI(7)} Risk Scorer + Auto-Approve",unsafe_allow_html=True)
        st.markdown("**Domain:** Automated Approvals · **Input:** Any change request · **Output:** Risk score (1-10) + route: auto/L1/L2/L3")
        c1,c2,c3,c4=st.columns(4)
        with c1: st.markdown(K("Scored","523","This month"),unsafe_allow_html=True)
        with c2: st.markdown(K("Auto-Approved","387","74%"),unsafe_allow_html=True)
        with c3: st.markdown(K("Manual Review","136","26%"),unsafe_allow_html=True)
        with c4: st.markdown(K("Avg Time","1.8 hrs","Was 18 hrs"),unsafe_allow_html=True)
        st.markdown("---")
        r1,r2,r3=st.columns(3)
        with r1: st.markdown(f'<div style="background:#D1FAE5;border:2px solid #6EE7B7;border-radius:14px;padding:20px;text-align:center;font-family:{F}"><div style="font-size:32px;font-weight:800;color:#065F46">Low (1-3)</div><div style="font-size:14px;font-weight:700;color:#065F46;margin:6px 0">✅ Auto-Approved</div><div style="font-size:13px;color:#065F46;line-height:1.6;margin-top:8px">Zero human touch. Pipeline triggers instantly. Dev/Sandbox, Reader, known templates.</div><div style="margin-top:12px;background:#065F46;color:#FFF;border-radius:8px;padding:10px;font-size:13px;font-weight:600">SLA: 5-15 min (full auto)</div></div>',unsafe_allow_html=True)
        with r2: st.markdown(f'<div style="background:#FEF3C7;border:2px solid #FCD34D;border-radius:14px;padding:20px;text-align:center;font-family:{F}"><div style="font-size:32px;font-weight:800;color:#92400E">Med (4-6)</div><div style="font-size:14px;font-weight:700;color:#92400E;margin:6px 0">⏳ L1 Approver (Teams)</div><div style="font-size:13px;color:#92400E;line-height:1.6;margin-top:8px">Platform Lead reviews via Teams card. Test env, Contributor, FW rules.</div><div style="margin-top:12px;background:#92400E;color:#FFF;border-radius:8px;padding:10px;font-size:13px;font-weight:600">SLA: 1-4 hrs (auto-escalate)</div></div>',unsafe_allow_html=True)
        with r3: st.markdown(f'<div style="background:#FEE2E2;border:2px solid #FCA5A5;border-radius:14px;padding:20px;text-align:center;font-family:{F}"><div style="font-size:32px;font-weight:800;color:#991B1B">High (7-10)</div><div style="font-size:14px;font-weight:700;color:#991B1B;margin:6px 0">🔒 L1+L2+CISO</div><div style="font-size:13px;color:#991B1B;line-height:1.6;margin-top:8px">Multi-level chain. Production, Owner, GPU, NSG 0.0.0.0/0.</div><div style="margin-top:12px;background:#991B1B;color:#FFF;border-radius:8px;padding:10px;font-size:13px;font-weight:600">SLA: 4-24 hrs (VP escalation)</div></div>',unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("#### Pending Approvals")
        for a in [x for x in st.session_state.approvals if x["status"]=="Awaiting"]:
            ico="🔴" if a["level"]=="High" else "🟡"
            with st.expander(f"{ico} {a['id']} — {a['desc']} (Score: {a['score']}/10)",expanded=True):
                c1,c2=st.columns([3,2])
                with c1:
                    st.markdown(f"**Req:** {a['req']} · **Type:** `{a['type']}` · **Risk:** {B(a['level'])} **{a['score']}**/10",unsafe_allow_html=True)
                    st.markdown("**Score Breakdown:**")
                    for fk,fv in a["factors"].items(): st.markdown(f"- **{fk}:** {fv}")
                with c2:
                    lv="cr" if a["level"]=="High" else "wn"
                    st.markdown(RB(f"🤖 <strong>AI:</strong> {a['ai']}",lv),unsafe_allow_html=True)
                b1,b2,b3=st.columns(3)
                if b1.button("Approve",key=f"ap_{a['id']}",type="primary",use_container_width=True): a["status"]="Approved"; st.success("Approved!"); st.rerun()
                if b2.button("Reject",key=f"rj_{a['id']}",use_container_width=True): a["status"]="Rejected"; st.error("Rejected."); st.rerun()
                if b3.button("Request Info",key=f"ri_{a['id']}",use_container_width=True): st.info("Teams msg sent to requestor.")
        st.markdown("---")
        st.markdown("#### Recent Scoring Log")
        st.dataframe(pd.DataFrame([
            {"ID":"REQ-2605","Type":"Sandbox SQL","Score":"1.9","Level":"Low","Decision":"✅ Auto","Time":"< 1 min"},
            {"ID":"REQ-2604","Type":"FW Rule","Score":"4.8","Level":"Med","Decision":"✅ L1","Time":"47 min"},
            {"ID":"REQ-2601","Type":"AKS Prod","Score":"7.4","Level":"High","Decision":"✅ L1+L2+CISO","Time":"5.2 hrs"},
            {"ID":"REQ-2606","Type":"Reader","Score":"2.1","Level":"Low","Decision":"✅ Auto","Time":"< 1 min"},
            {"ID":"REQ-2599","Type":"NSG 0.0.0.0/0","Score":"9.8","Level":"High","Decision":"❌ Rejected","Time":"Instant"},
        ]),use_container_width=True,hide_index=True)

# ════════════════════════════════════════════════════════════════
# ④ ORCHESTRATION + IaC EXECUTION (SVG Row 4)
# ════════════════════════════════════════════════════════════════
elif page=="④ Orchestration + IaC":
    st.markdown(SEC("④ ORCHESTRATION + IaC EXECUTION + RAG KNOWLEDGE BASE","#0078D4"),unsafe_allow_html=True)
    st.markdown("After approval, the **Logic Apps → DevOps → ARM** pipeline executes with zero manual steps. **AI Search RAG** provides context to all 7 AI features.")

    c1,c2,c3,c4=st.columns(4)
    with c1: st.markdown(CARD("⚙️ Logic Apps (Approval Workflows)",["1. Service Bus trigger → AI risk score","2. Route: auto-approve / Teams card","3. On approve → trigger DevOps pipeline","Multi-level escalation chains","SLA tracking + auto-escalate"],"#283593","#E8EAF6","#9FA8DA"),unsafe_allow_html=True)
    with c2: st.markdown(CARD("🔧 Azure DevOps / GitHub Actions",["IaC Repos: Bicep + Terraform HCL","Pipeline templates per domain (7)","Service Conn → Managed Identity","Lint → Policy → Plan → Deploy","PR-based GitOps workflow"],"#E65100","#FFF3E0","#FFB74D"),unsafe_allow_html=True)
    with c3: st.markdown(CARD("☁️ Azure Resource Manager",["Deployment what-if → validate","Policy eval (deny/audit/modify)","Deploy to target subscription","Managed Identity auth (zero secrets)","Deployment history + rollback"],"#0277BD","#E1F5FE","#4FC3F7"),unsafe_allow_html=True)
    with c4: st.markdown(CARD("🔍 Azure AI Search (RAG)",["Index: IaC templates + runbooks","Index: CIS benchmarks + policies","Index: Past deployments + incidents","Semantic ranking + hybrid search","All 7 AI features query this KB"],"#4527A0","#EDE7F6","#B39DDB"),unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 5-Stage IaC Pipeline Execution")
    stages=[
        ("1. Lint + Security Scan","Checkov, tflint, Bicep validate, credential scan","#002050",
         ["✅ Checkov CKV_AZURE_35: Storage Deny — PASS","✅ tflint: 0 errors, 0 warnings","✅ Bicep validate: Template is valid","✅ Credential scan: No secrets detected"]),
        ("2. Policy What-If","Azure Policy dry-run against governance rules","#0078D4",
         ["✅ Region: East US 2 — ALLOWED","✅ SKU: Standard_D4s_v5 — APPROVED","✅ Tags: 4/4 mandatory present","✅ Private Endpoint: auto-config — COMPLIANT","✅ TLS Minimum: 1.2 — COMPLIANT"]),
        ("3. Terraform Plan","Execution plan with cost estimate","#5C2D91",
         ["📋 Plan: 4 to add, 0 to change, 0 to destroy","📋 +azurerm_kubernetes_cluster.meridian","📋 +azurerm_private_endpoint.aks_pe","📋 +azurerm_private_dns_zone_link.aks","💰 Estimated cost: +$876/mo"]),
        ("4. ARM Deploy","Managed Identity, PE, diagnostics from start","#107C10",
         ["✅ Target: sub-prod / rg-meridian-prod","✅ Identity: Managed (SystemAssigned)","✅ PE: 10.1.2.47 in snet-pe","✅ Diagnostics: → Log Analytics","✅ Status: Succeeded (2m 34s)"]),
        ("5. AI Validate + Notify","Post-deploy AI validation + notifications","#107C10",
         ["✅ PE connectivity: resolves correctly","✅ DNS: privatelink.database.windows.net","✅ Diagnostics: Metrics flowing","✅ Tags: All 4 present","✅ Teams: Notification sent","✅ ServiceNow: CHG-8847 auto-closed"]),
    ]
    for title,desc,color,checks in stages:
        with st.expander(f"**{title}** — {desc}",expanded=True):
            st.markdown("**Sample Output (REQ-2601: AKS Production):**")
            for c in checks: st.markdown(f"`{c}`")

    st.markdown("---")
    c1,c2=st.columns(2)
    with c1:
        st.markdown(CARD("📣 Notifications + ITSM",["Teams: Adaptive cards (approve/reject inline)","Email: O365 connector (status updates)","ServiceNow: Change/Incident tickets (API)","Slack: Webhook integration (optional)"],"#6A1B9A","#F3E5F5","#CE93D8"),unsafe_allow_html=True)
    with c2:
        st.markdown("#### Pipeline Execution History")
        st.dataframe(pd.DataFrame([
            {"Request":"REQ-2601","Type":"AKS Prod","Lint":"✅","Policy":"✅","Plan":"✅","Deploy":"✅ 2m34s","Validate":"✅","Total":"2m 57s"},
            {"Request":"REQ-2605","Type":"Sandbox SQL","Lint":"✅","Policy":"✅","Plan":"✅","Deploy":"✅ 47s","Validate":"✅","Total":"57s"},
            {"Request":"REQ-2604","Type":"FW Rule","Lint":"✅","Policy":"✅","Plan":"✅","Deploy":"✅ 18s","Validate":"✅","Total":"25s"},
            {"Request":"REQ-2599","Type":"NSG 0.0.0.0/0","Lint":"❌ BLOCKED","Policy":"—","Plan":"—","Deploy":"—","Validate":"—","Total":"3s"},
        ]),use_container_width=True,hide_index=True)

# ════════════════════════════════════════════════════════════════
# ⑤ LANDING ZONE NETWORK (SVG Row 5)
# ════════════════════════════════════════════════════════════════
elif page=="⑤ Landing Zone Network":
    st.markdown(SEC("⑤ AZURE LANDING ZONE — Hub-Spoke Network Topology","#0078D4"),unsafe_allow_html=True)
    st.markdown("All AI-generated deployments target the correct subscription spoke. Hub provides shared connectivity, firewall, DNS, and monitoring.")

    # Hub
    st.markdown(f"""<div style="background:#E3F2FD;border:2px solid #1976D2;border-radius:12px;padding:0;overflow:hidden;margin-bottom:16px;font-family:{F}">
    <div style="background:#1976D2;padding:14px 20px;color:#FFF;font-size:15px;font-weight:700">🔵 Hub VNet (10.0.0.0/16) — Connectivity Subscription</div>
    <div style="padding:16px 20px">""",unsafe_allow_html=True)
    h1,h2,h3=st.columns(3)
    with h1:
        st.markdown(CARD("🔥 Azure Firewall",["10.0.1.0/24","DNAT + Network rules","Private IP: 10.0.1.4"],"#D32F2F","#FFF","#BBDEFB"),unsafe_allow_html=True)
        st.markdown(CARD("🔒 Private DNS Zones",["*.database.windows.net","*.blob.core.windows.net","*.vault.azure.net, *.openai"],"#1565C0","#FFF","#BBDEFB"),unsafe_allow_html=True)
    with h2:
        st.markdown(CARD("🌐 VPN / ExpressRoute GW",["10.0.2.0/24","ExpressRoute 2Gbps","On-prem circuit to Oracle/SAP"],"#1565C0","#FFF","#BBDEFB"),unsafe_allow_html=True)
        st.markdown(CARD("📊 Log Analytics (Central)",["Central workspace","All subs → diagnostics","90-day retention"],"#1565C0","#FFF","#BBDEFB"),unsafe_allow_html=True)
    with h3:
        st.markdown(CARD("🛡️ Azure Bastion",["10.0.3.0/24","Secure VM access","No public IP required"],"#1565C0","#FFF","#BBDEFB"),unsafe_allow_html=True)
        st.markdown(CARD("⚙️ Shared Services",["ACR, Key Vault, ADF","Automation Account","APIM + Functions + OpenAI PE"],"#1565C0","#FFF","#BBDEFB"),unsafe_allow_html=True)
    st.markdown(f'<div style="background:#C8E6C9;border-radius:8px;padding:12px 18px;margin-top:8px;font-size:13px;font-weight:600;color:#2E7D32;font-family:{F}">📡 App Subnet (10.0.10.0/24) — Functions + APIM + Azure OpenAI PE + AI Search PE</div>',unsafe_allow_html=True)
    st.markdown("</div></div>",unsafe_allow_html=True)

    # Spokes
    c1,c2,c3=st.columns(3)
    with c1:
        st.markdown(f"""<div style="background:#E8F5E9;border:2px solid #388E3C;border-radius:12px;overflow:hidden;font-family:{F}">
        <div style="background:#388E3C;padding:12px 18px;color:#FFF;font-size:14px;font-weight:700">🟢 Production (10.1.0.0/16)</div>
        <div style="padding:14px 18px;font-size:14px;line-height:2.0;color:#333">
        🗄️ Azure SQL MI — Atlas DW (PE)<br>📊 Power BI Premium — Reports<br>☸️ AKS Cluster — private API<br>🌐 App Services — VNet integrated<br>🔐 Key Vault — soft-delete + purge<br>
        <span style="color:#2E7D32;font-weight:600;font-size:13px">VNet peered to Hub · Strict NSG</span></div></div>""",unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div style="background:#E3F2FD;border:2px solid #1976D2;border-radius:12px;overflow:hidden;font-family:{F}">
        <div style="background:#1976D2;padding:12px 18px;color:#FFF;font-size:14px;font-weight:700">🔵 Dev/Test (10.2.0.0/16)</div>
        <div style="padding:14px 18px;font-size:14px;line-height:2.0;color:#333">
        🧪 Dev SQL + Storage<br>🔄 UAT / SIT / Perf envs<br>🤖 Sandboxes (AI-provisioned, 14d TTL)<br>💰 Budget cap: $10K/mo<br>🧹 Auto-cleanup expired resources<br>
        <span style="color:#1565C0;font-weight:600;font-size:13px">Most requests auto-approve (Low)</span></div></div>""",unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div style="background:#F3E5F5;border:2px solid #7B1FA2;border-radius:12px;overflow:hidden;font-family:{F}">
        <div style="background:#7B1FA2;padding:12px 18px;color:#FFF;font-size:14px;font-weight:700">🟣 Data Platform (10.3.0.0/16)</div>
        <div style="padding:14px 18px;font-size:14px;line-height:2.0;color:#333">
        🔌 Informatica Cloud — ETL → SQL<br>📦 ADLS Gen2 — Raw + Curated<br>⚡ Data Factory + Synapse Analytics<br>🧠 ML Workspace + GPU VMs<br>📊 Databricks + Snowflake connector<br>
        <span style="color:#6A1B9A;font-weight:600;font-size:13px">Data pipelines, ML infra</span></div></div>""",unsafe_allow_html=True)

    st.markdown("---")
    # On-Premises
    st.markdown(f"""<div style="background:#F5F5F5;border:2px dashed #9E9E9E;border-radius:12px;overflow:hidden;font-family:{F};margin-bottom:16px">
    <div style="background:#757575;padding:12px 18px;color:#FFF;font-size:14px;font-weight:700">🏢 On-Premises (via ExpressRoute / S2S VPN)</div>
    <div style="padding:16px 18px">""",unsafe_allow_html=True)
    o1,o2,o3=st.columns(3)
    with o1:
        st.markdown(CARD("Oracle R12 (EBS)",["GL, AP, Inventory, Customer","Source system for Atlas DW"],"#424242","#FFF","#BDBDBD"),unsafe_allow_html=True)
        st.markdown(CARD("Cognos (Retiring)",["Legacy BI → Power BI migration","Decommission after validation"],"#424242","#FFF","#BDBDBD"),unsafe_allow_html=True)
    with o2:
        st.markdown(CARD("Oracle GLTM",["Master data source","Global Transfer Module"],"#424242","#FFF","#BDBDBD"),unsafe_allow_html=True)
        st.markdown(CARD("Encompass NV (SSAS)",["NV Cube → migrate to Azure","SSAS to Synapse/Power BI"],"#424242","#FFF","#BDBDBD"),unsafe_allow_html=True)
    with o3:
        st.markdown(CARD("Manufacturing Plans",["Excel via FTP → ADF ingestion","Automated pipeline scheduled"],"#424242","#FFF","#BDBDBD"),unsafe_allow_html=True)
        st.markdown(CARD("🟢 Downstream Consumers",["Executives (PBI Dashboards)","Sales (Self-Service Reports)","Ad Hoc Users (PBI Datasets)","Accelerate R4 (US API feed)","SAP alignment (2+ yr history)"],"#2E7D32","#E8F5E9","#66BB6A"),unsafe_allow_html=True)
    st.markdown("</div></div>",unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### Subscription Resource Inventory")
    st.dataframe(pd.DataFrame([
        {"Subscription":"Hub-Connectivity","VNet":"10.0.0.0/16","Resources":47,"Monthly Cost":"$17.2K","Compliance":"100%","Key Services":"Firewall, Bastion, ER GW, APIM, DNS"},
        {"Subscription":"Prod-LandingZone","VNet":"10.1.0.0/16","Resources":312,"Monthly Cost":"$56.8K","Compliance":"97%","Key Services":"AKS, SQL MI, Cosmos DB, PBI, App Svc"},
        {"Subscription":"Dev-Test","VNet":"10.2.0.0/16","Resources":198,"Monthly Cost":"$26.4K","Compliance":"92%","Key Services":"Dev VMs, Test DBs, Sandboxes"},
        {"Subscription":"Data-Platform","VNet":"10.3.0.0/16","Resources":234,"Monthly Cost":"$34.1K","Compliance":"95%","Key Services":"ADLS, Synapse, ADF, Informatica, ML"},
        {"Subscription":"Sandbox-POC","VNet":"10.4.0.0/16","Resources":56,"Monthly Cost":"$7.8K","Compliance":"88%","Key Services":"POC resources, experiments"},
    ]),use_container_width=True,hide_index=True)

# ════════════════════════════════════════════════════════════════
# ⑥ DATA FLOW + BUSINESS OUTCOMES (SVG Row 6)
# ════════════════════════════════════════════════════════════════
elif page=="⑥ Data Flow + Outcomes":
    st.markdown(SEC("⑥ DATA FLOW + BUSINESS OUTCOMES","#107C10"),unsafe_allow_html=True)

    # ── Data Flow Pipeline ──
    st.markdown("#### Atlas Migration Data Flow — AI Reconciliation at Every Stage")
    flow_steps=[
        ("Oracle R12\n+ GLTM","#FFEBEE","#E57373","#C62828"),
        ("ADF\n(FTP Ingest)","#FFF3E0","#FFB74D","#E65100"),
        ("Informatica\nCloud","#F3E5F5","#CE93D8","#6A1B9A"),
        ("Azure\nSQL MI","#E3F2FD","#64B5F6","#1565C0"),
        ("🧠 AI\nReconciliation","#EDE7F6","#9575CD","#4527A0"),
        ("Power BI\nReports","#E8F5E9","#66BB6A","#2E7D32"),
        ("End\nUsers","#E8F5E9","#66BB6A","#2E7D32"),
    ]
    cols=st.columns(len(flow_steps))
    for col,(label,bg,border,tc) in zip(cols,flow_steps):
        with col:
            st.markdown(f'<div style="background:{bg};border:2px solid {border};border-radius:10px;padding:14px 12px;text-align:center;font-family:{F};min-height:70px;display:flex;align-items:center;justify-content:center"><div style="font-size:13px;font-weight:700;color:{tc};line-height:1.4">{label.replace(chr(10),"<br>")}</div></div>',unsafe_allow_html=True)
    st.markdown(f'<div style="text-align:center;font-size:13px;color:#5C2D91;font-family:{M};margin:8px 0 16px">AI validates: schema mapping (UR-009) → data parity (UR-009) → Informatica mappings (UR-010) → PBI vs Cognos (UR-011)</div>',unsafe_allow_html=True)

    st.markdown("---")
    # ── Business Outcomes ──
    st.markdown("#### Business Outcomes")
    outcomes=[
        ("40%","Faster Provisioning","Minutes vs 3-5 business days","#107C10"),
        ("60%","Less Manual Effort","AI handles scoring, IaC gen, validation","#0078D4"),
        ("$156K","Annual Cost Savings","FinOps AI: $13K/mo optimizations","#5C2D91"),
        ("50%","Faster MTTR","Drift detect + auto-remediate","#E74856"),
        ("96.2%","Compliance Score","847 resources, CIS benchmarked","#D97706"),
        ("100%","Audit Trail Coverage","Every action, decision, deployment","#0F172A"),
    ]
    cols=st.columns(3)
    for idx,(val,title,sub,color) in enumerate(outcomes):
        with cols[idx%3]:
            st.markdown(f"""<div style="background:#FFF;border:2px solid {color};border-radius:14px;padding:20px;text-align:center;margin:8px 0;box-shadow:0 2px 8px rgba(0,0,0,.06);font-family:{F}">
            <div style="font-size:36px;font-weight:800;color:{color}">{val}</div>
            <div style="font-size:14px;font-weight:700;color:{color};margin:4px 0">{title}</div>
            <div style="font-size:12px;color:#64748B">{sub}</div></div>""",unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### Before vs After Comparison")
    st.dataframe(pd.DataFrame([
        {"Metric":"Provisioning Time","Before":"3-5 business days","After":"5-15 min (low) / 1-24 hrs (high)","Improvement":"40x faster"},
        {"Metric":"Approval Process","Before":"Email chains, meetings","After":"AI risk score + Teams cards","Improvement":"74% auto-approved"},
        {"Metric":"IaC Generation","Before":"2-4 hours per template","After":"AI generates in seconds","Improvement":"95% time saved"},
        {"Metric":"Drift Detection","Before":"Monthly manual audits","After":"Hourly AI scans + auto-fix","Improvement":"720x more frequent"},
        {"Metric":"Cost Optimization","Before":"Quarterly reviews","After":"Daily AI recs + auto-apply","Improvement":"$156K/yr savings"},
        {"Metric":"Compliance","Before":"Periodic assessment","After":"Continuous + Policy deny","Improvement":"96.2% automated"},
        {"Metric":"Access Reviews","Before":"Semi-annual cycles","After":"Real-time anomaly detection","Improvement":"Instant alerts"},
    ]),use_container_width=True,hide_index=True)

    st.markdown("---")
    c1,c2=st.columns(2)
    with c1:
        st.markdown("#### Compliance Summary")
        cats=["Logging","Data Protection","Network Security","Compute","Identity","Tagging"]
        scores=[100,97,94,95,93,92]
        colors=["#107C10" if s>=95 else "#D97706" for s in scores]
        fig=go.Figure(go.Bar(x=scores,y=cats,orientation="h",marker_color=colors,text=[f"{s}%" for s in scores],textposition="outside"))
        fig.update_layout(height=260,margin=dict(l=0,r=50,t=10,b=0),plot_bgcolor="white",xaxis=dict(range=[80,105]),yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig,use_container_width=True)
    with c2:
        st.markdown("#### AI Feature Cross-Reference")
        st.dataframe(pd.DataFrame([
            {"AI#":"#1","Feature":"NL→IaC Generator","Domain":"Provisioning+Sandbox","Key Capability":"NL → Bicep/TF with PE+diag+tags"},
            {"AI#":"#2","Feature":"Ops Chatbot","Domain":"Env Provisioning","Key Capability":"Conversational self-service portal"},
            {"AI#":"#3","Feature":"Drift Detector","Domain":"Azure Resources","Key Capability":"ARM vs IaC + auto-fix PRs"},
            {"AI#":"#4","Feature":"Access Anomaly","Domain":"Identity & Access","Key Capability":"Stale SPNs, impossible travel"},
            {"AI#":"#5","Feature":"Network Posture","Domain":"Network Security","Key Capability":"CIS benchmark + topology docs"},
            {"AI#":"#6","Feature":"FinOps AI","Domain":"FinOps & Cost","Key Capability":"Anomaly detect + forecast + RI"},
            {"AI#":"#7","Feature":"Risk Scorer","Domain":"Approvals","Key Capability":"1-10 score + auto-route"},
        ]),use_container_width=True,hide_index=True)

    st.markdown("---")
    st.markdown("#### Audit & Observability Stack")
    a1,a2,a3,a4=st.columns(4)
    with a1: st.markdown(CARD("🗄️ Cosmos DB",["Request store","AI scores + decisions","Full audit trail"],"#00695C","#E0F2F1","#80CBC4"),unsafe_allow_html=True)
    with a2: st.markdown(CARD("📊 Log Analytics",["Diagnostics (all subs)","Activity logs","Custom queries (KQL)"],"#0078D4","#E3F2FD","#90CAF9"),unsafe_allow_html=True)
    with a3: st.markdown(CARD("🛡️ Microsoft Sentinel",["SIEM + SOAR","Security correlation","Incident automation"],"#5C2D91","#EDE7F6","#B39DDB"),unsafe_allow_html=True)
    with a4: st.markdown(CARD("📋 ServiceNow",["Change tickets (auto)","Incident management","CMDB integration"],"#E65100","#FFF3E0","#FFB74D"),unsafe_allow_html=True)
