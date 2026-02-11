import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import json, random, datetime, time

# ============================================================
ORG="FutureMinds"; DOMAIN="futureminds.cloud"; TENANT="futureminds.onmicrosoft.com"; PROJECT="Meridian-Analytics"
st.set_page_config(page_title=f"CloudOps Portal - {ORG}",page_icon="☁️",layout="wide",initial_sidebar_state="expanded")

# ============================================================
# CSS
# ============================================================
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
:root{--blue:#0369A1;--blue-l:#E0F2FE;--blue-d:#0C4A6E;--purple:#7C3AED;--purple-l:#EDE9FE;--purple-d:#5B21B6;
--green:#059669;--green-l:#D1FAE5;--green-d:#065F46;--amber:#D97706;--amber-l:#FEF3C7;--amber-d:#92400E;
--red:#DC2626;--red-l:#FEE2E2;--red-d:#991B1B;--text:#0F172A;--text2:#475569;--text3:#94A3B8;--border:#E2E8F0;--bg:#FFF;
--shadow:0 1px 3px rgba(0,0,0,0.06),0 1px 2px rgba(0,0,0,0.04);--shadow-md:0 4px 6px -1px rgba(0,0,0,0.07),0 2px 4px -2px rgba(0,0,0,0.05);--radius:10px}
*{font-family:'DM Sans',system-ui,sans-serif !important} code,pre{font-family:'JetBrains Mono',monospace !important}
.main .block-container{padding:1rem 2rem 2rem}
div[data-testid="stSidebar"]{background:#0F172A !important}
div[data-testid="stSidebar"] *{color:#E2E8F0 !important}
div[data-testid="stSidebar"] hr{border-color:#1E293B !important}
#MainMenu,footer,.stDeployButton,div[data-testid="stToolbar"]{display:none !important}
.hdr{background:linear-gradient(135deg,#0C4A6E 0%,#0369A1 50%,#0891B2 100%);padding:16px 28px;border-radius:12px;margin-bottom:20px;display:flex;justify-content:space-between;align-items:center;box-shadow:0 4px 20px rgba(3,105,161,0.25);position:relative;overflow:hidden}
.hdr::before{content:'';position:absolute;top:-50%;right:-10%;width:300px;height:300px;background:radial-gradient(circle,rgba(255,255,255,0.06) 0%,transparent 70%)}
.hdr h2{color:#FFF;margin:0;font-size:20px;font-weight:700} .hdr .sub{color:rgba(255,255,255,0.7);margin:0;font-size:11px}
.hdr .ri{text-align:right} .hdr .un{color:#FFF;font-size:13px;font-weight:600} .hdr .ut{color:rgba(255,255,255,0.55);font-size:10px}
.kpi{background:var(--bg);border:1px solid var(--border);border-radius:var(--radius);padding:16px 20px;text-align:center;box-shadow:var(--shadow);transition:transform .15s,box-shadow .15s}
.kpi:hover{transform:translateY(-1px);box-shadow:var(--shadow-md)}
.kpi .v{font-size:28px;font-weight:700;color:var(--blue);margin:4px 0;letter-spacing:-.5px}
.kpi .l{font-size:10px;color:var(--text3);text-transform:uppercase;letter-spacing:1px;font-weight:600}
.kpi .d{font-size:10px;padding:2px 8px;border-radius:10px;display:inline-block;margin-top:4px;font-weight:600}
.kpi .d.u{background:var(--green-l);color:var(--green-d)} .kpi .d.dn{background:var(--red-l);color:var(--red-d)}
.b{padding:3px 10px;border-radius:12px;font-size:10.5px;font-weight:600;display:inline-block;letter-spacing:.2px}
.bg{background:var(--green-l);color:var(--green-d)} .ba{background:var(--amber-l);color:var(--amber-d)} .br{background:var(--red-l);color:var(--red-d)} .bb{background:var(--blue-l);color:var(--blue-d)} .bp{background:var(--purple-l);color:var(--purple-d)}
.ai{background:linear-gradient(135deg,var(--purple-l),#F5F3FF);border:1px solid #C4B5FD;border-radius:8px;padding:4px 12px;font-size:10px;font-weight:700;color:var(--purple-d);display:inline-block}
.sc{background:var(--bg);border:1px solid var(--border);border-radius:var(--radius);padding:20px 24px;margin:8px 0;box-shadow:var(--shadow);border-left:4px solid var(--blue);transition:border-color .2s}
.sc:hover{border-left-color:var(--purple)} .sc h4{margin:0 0 6px;font-size:15px;font-weight:700}
.cu{background:var(--blue-l);border-radius:14px 14px 4px 14px;padding:12px 16px;margin:8px 0 8px 60px;font-size:13px;line-height:1.45}
.ca{background:#F0FDF4;border-radius:14px 14px 14px 4px;padding:12px 16px;margin:8px 60px 8px 0;font-size:13px;border-left:3px solid var(--green);line-height:1.45}
.ro{padding:12px 16px;margin:6px 0;border-radius:0 8px 8px 0;font-size:13px;line-height:1.5}
.ro.ok{background:#F0FDF4;border-left:3px solid var(--green)} .ro.wn{background:#FFFBEB;border-left:3px solid var(--amber)} .ro.cr{background:#FEF2F2;border-left:3px solid var(--red)}
.rt{border-radius:12px;padding:18px;text-align:center;transition:transform .15s} .rt:hover{transform:translateY(-2px)} .rt .s{font-size:26px;font-weight:700} .rt .lb{font-size:12px;font-weight:600;margin:4px 0} .rt .dt{font-size:11px;opacity:.75;margin-top:6px}
.spoke{border-radius:12px;padding:0;overflow:hidden;box-shadow:var(--shadow-md);height:100%}
.spoke .sh{padding:10px 16px;color:#FFF;font-weight:700;font-size:12px} .spoke .sb{padding:14px 16px;font-size:12px;line-height:1.8}
.sec{font-size:11px;font-weight:700;letter-spacing:1.5px;margin-bottom:4px;padding-bottom:4px;border-bottom:1px solid var(--border)}
div[data-testid="stExpander"] details{border:1px solid var(--border) !important;border-radius:var(--radius) !important;box-shadow:var(--shadow) !important}
</style>""", unsafe_allow_html=True)

# ============================================================
# HELPERS
# ============================================================
def K(l,v,d=None,dr="u"):
    dh=f'<div class="d {dr}">{d}</div>' if d else ""
    return f'<div class="kpi"><div class="l">{l}</div><div class="v">{v}</div>{dh}</div>'
def B(s):
    m={"Approved":"bg","Deployed":"bg","Pass":"bg","Low":"bg","OK":"bg","Resolved":"bg","Clean":"bg","Healthy":"bg","Auto-Approved":"bg",
       "Pending":"ba","Medium":"ba","Open":"ba","Awaiting Approval":"ba","Warning":"ba","Expiring":"ba",
       "Critical":"br","High":"br","Drift":"br","Stale":"br","Rejected":"br","Over-privileged":"br","Anomaly":"br","Blocked":"br",
       "AI Review":"bp"}
    return f'<span class="b {m.get(s,"bb")}">{s}</span>'
def AI(n): return f'<span class="ai">AI #{n}</span>'
def RB(t,lv="ok"): return f'<div class="ro {lv}">{t}</div>'
def SI(s): return {"Critical":"🔴","High":"🟠","Medium":"🟡","Low":"🟢"}.get(s,"⚪")

def call_claude(p,s="You are an Azure CloudOps AI for FutureMinds. Concise technical responses. Under 300 words."):
    try:
        import anthropic
        k=st.secrets.get("ANTHROPIC_API_KEY",None)
        if not k: return None
        return anthropic.Anthropic(api_key=k).messages.create(model="claude-sonnet-4-20250514",max_tokens=1024,system=s,messages=[{"role":"user","content":p}]).content[0].text
    except: return None

# ============================================================
# SESSION STATE
# ============================================================
if "i" not in st.session_state:
    st.session_state.i=True; st.session_state.persona="Cloud Engineer"; st.session_state.chat=[]
    st.session_state.reqs=[
        {"id":"REQ-2601","type":"Provision","desc":"AKS cluster for Meridian analytics (3-node, private API)","status":"Deployed","risk":"High","score":7.4,"date":"2026-02-03","sub":"Production","by":"Priya S."},
        {"id":"REQ-2602","type":"Network","desc":"Private endpoint for Cosmos DB multi-region (East US 2 + West Europe)","status":"Pending","risk":"High","score":8.1,"date":"2026-02-11","sub":"Production","by":"Marcus W."},
        {"id":"REQ-2603","type":"Access","desc":"Contributor role on rg-meridian-data for ETL service principal","status":"AI Review","risk":"Medium","score":5.3,"date":"2026-02-11","sub":"Data Platform","by":"Anika R."},
        {"id":"REQ-2604","type":"Firewall","desc":"Allow outbound HTTPS to Snowflake partner endpoints","status":"Approved","risk":"Medium","score":4.8,"date":"2026-02-09","sub":"Hub","by":"Devon L."},
        {"id":"REQ-2605","type":"Provision","desc":"Dev sandbox SQL+Redis for feature branch testing (14-day TTL)","status":"Auto-Approved","risk":"Low","score":1.9,"date":"2026-02-10","sub":"Dev/Test","by":"Jordan K."},
        {"id":"REQ-2606","type":"Access","desc":"Reader for external auditor (PwC) on compliance RG","status":"Auto-Approved","risk":"Low","score":2.1,"date":"2026-02-08","sub":"Production","by":"Compliance"},
        {"id":"REQ-2607","type":"Provision","desc":"GPU VM (NC6s_v3) for ML model training - recommendation engine","status":"Pending","risk":"High","score":8.6,"date":"2026-02-11","sub":"Data Platform","by":"Dr. Chen L."},
    ]
    st.session_state.approvals=[
        {"id":"APR-101","req":"REQ-2602","type":"Network","desc":"PE for Cosmos DB multi-region","risk_score":8.1,"risk_level":"High","ai_rec":"Config aligns with FutureMinds PE standards. 2 PEs + 2 Private DNS zones needed. Cost: +$73/mo. Requires Network + Security review (cross-region replication).","factors":{"Environment":"Production (+3)","Resource":"Cosmos DB multi-region (+2)","Network":"Cross-region peering (+2)","Template":"Standard PE template (+0)","Blast Radius":"Multi-region data (+1)"},"status":"Awaiting Approval"},
        {"id":"APR-102","req":"REQ-2603","type":"Access","desc":"Contributor for ETL SPN","risk_score":5.3,"risk_level":"Medium","ai_rec":"Contributor overly broad. Recommend custom role 'Meridian Data Pipeline Operator': SQL read, Storage write, ADF action. Set 90-day PIM expiry.","factors":{"Environment":"Data Platform (+1)","Permission":"Contributor broad (+2)","Scope":"Resource Group (+1)","Identity":"Service Principal (+1)","Pattern":"First-time (+0)"},"status":"Awaiting Approval"},
        {"id":"APR-103","req":"REQ-2607","type":"Provision","desc":"GPU VM for ML training","risk_score":8.6,"risk_level":"High","ai_rec":"NC6s_v3 = $1,096/mo. Recommend: Spot Instance ($329/mo, 70% savings), auto-shutdown 8PM, Managed Identity. Requires CTO approval per GPU policy.","factors":{"Environment":"Data Platform (+1)","Cost":"$1,096/mo GPU (+3)","Resource":"Compute-intensive (+2)","Policy":"GPU approval required (+2)","Duration":"Ongoing (+0)"},"status":"Awaiting Approval"},
    ]
    st.session_state.drifts=[
        {"res":"nsg-prod-aks-cluster","type":"NSG","sub":"Production","drift":"Inbound rule: Allow TCP 8443 from 0.0.0.0/0 (bypassed IaC)","sev":"Critical","age":"1h 23m","iac":"modules/network/nsg-aks.bicep","detail":"Engineer added kubectl debug port via Portal, bypassing GitOps. Exposes AKS API to public internet.","fix":"Remove rule. Add scoped rule for bastion subnet 10.0.3.0/24 only."},
        {"res":"sql-meridian-prod","type":"SQL","sub":"Production","drift":"TLS min version downgraded 1.2 → 1.0 via Portal","sev":"Critical","age":"3h 12m","iac":"modules/data/sql-meridian.bicep","detail":"TLS 1.0 enables BEAST/POODLE vulnerabilities. Changed for legacy Informatica connector.","fix":"Revert to TLS 1.2. Update Informatica connector to v10.5+."},
        {"res":"kv-futureminds-hub","type":"Key Vault","sub":"Hub","drift":"Soft-delete protection disabled manually","sev":"Critical","age":"6h 45m","iac":"modules/security/kv-hub.bicep","detail":"Soft-delete required by policy. Disabling allows permanent secret deletion.","fix":"Re-enable soft-delete (90-day). Enable purge protection."},
        {"res":"vm-meridian-etl-02","type":"VM","sub":"Production","drift":"SKU changed D4s_v5 → D8s_v5 via Portal","sev":"Medium","age":"12h","iac":"modules/compute/vm-etl.bicep","detail":"Manually upsized during data spike. Avg CPU since: 18% (over-provisioned).","fix":"Revert to D4s_v5, add auto-scale rule for spikes."},
        {"res":"sta-datalake-raw","type":"Storage","sub":"Data Platform","drift":"Public network access toggled Enabled","sev":"Critical","age":"45m","iac":"modules/data/storage-datalake.bicep","detail":"ADLS Gen2 raw zone exposed to public internet. Contains unmasked PII.","fix":"Disable public access immediately. Verify no exfiltration via logs."},
        {"res":"aks-meridian-prod","type":"AKS","sub":"Production","drift":"Node pool scaled 3 → 7 manually","sev":"Low","age":"2d","iac":"modules/compute/aks-prod.bicep","detail":"Scaled for v2.3 launch traffic spike. Traffic normalized. 4 excess nodes = $580/mo.","fix":"Update IaC to 3 nodes + HPA for auto-scaling."},
    ]
    st.session_state.anomalies=[
        {"sev":"Critical","id":"svc-legacy-etl-01 (SPN)","type":"Stale","finding":"Owner on Production sub - zero calls in 127 days","detail":"Legacy ETL SPN decommissioned Oct 2025. Owner = full sub control.","rec":"Revoke immediately. New SPN with custom role if needed.","score":9.4},
        {"sev":"Critical","id":"ext-contractor-rajesh@partner.com","type":"Anomaly","finding":"Sign-in from Vladivostok, Russia at 3:47 AM + 4 failed MFA","detail":"Contractor based in Bangalore. Impossible travel (8,400km in 2h).","rec":"Block sign-in. Rotate credentials. Trigger security incident.","score":9.8},
        {"sev":"High","id":"svc-jenkins-deploy (SPN)","type":"Over-privileged","finding":"Contributor on 4 subs - activity only in Dev/Test","detail":"CI/CD SPN has write to Prod, Hub, Data but never deployed outside Dev/Test in 6 months.","rec":"Scope to Dev/Test. Create separate Prod Deployer with JIT.","score":7.2},
        {"sev":"High","id":"CloudOps-Platform-Engineers (Group)","type":"Stale","finding":"3 of 8 members inactive 60+ days","detail":"alex.former@ (left), test.user@ (test), intern.2025@ (ended).","rec":"Remove 3 inactive. Quarterly access review. Lifecycle workflows.","score":6.8},
        {"sev":"Medium","id":"dr.chen@futureminds.cloud","type":"Anomaly","finding":"PIM Owner activation 14x this week (baseline 3x)","detail":"ML lead doing GPU VM sprint. Correlates with REQ-2607.","rec":"Likely legitimate. Convert to standing ML Platform Contributor.","score":4.6},
    ]
    st.session_state.net_findings=[
        {"sev":"Critical","cis":"CIS 6.2","finding":"NSG allows SSH 22 from 0.0.0.0/0","sub":"Dev/Test","impact":"Any IP can SSH. 847 brute-force attempts in 24h.","rec":"Restrict to BastionSubnet 10.0.3.0/24. Enable JIT VM Access.","cmd":"az network nsg rule update -g rg-devtest --nsg-name nsg-devtest-default -n AllowSSH --source-address-prefixes 10.0.3.0/24"},
        {"sev":"Critical","cis":"CIS 3.7","finding":"Storage sta-sandbox-analytics publicNetworkAccess=Enabled","sub":"Sandbox","impact":"Accessible from any IP. May contain derivative PII.","rec":"Disable public access. Add PE in sandbox VNet.","cmd":"az storage account update -n stasandboxanalytics -g rg-sandbox --public-network-access Disabled"},
        {"sev":"High","cis":"CIS 6.5","finding":"Azure Firewall allows outbound 0.0.0.0/0:443 from Sandbox","sub":"Hub","impact":"Sandbox can reach any HTTPS endpoint. Data exfiltration risk.","rec":"Replace wildcard with FQDN tags: AzureCloud, ACR. Add app rules for Snowflake, Databricks.","cmd":"az network firewall policy rule-collection-group ... --target-fqdns '*.snowflakecomputing.com'"},
        {"sev":"Medium","cis":"CIS 6.4","finding":"3 NSGs have no flow logs","sub":"Multiple","impact":"No traffic visibility for forensics.","rec":"Enable NSG flow logs v2, 90-day retention, Traffic Analytics.","cmd":"az network watcher flow-log create --nsg <id> --workspace <law-id> --enabled true"},
        {"sev":"Medium","cis":"CIS 6.1","finding":"Data Platform VNet missing UDR force-tunnel to Hub FW","sub":"Data Platform","impact":"Resources route directly to internet bypassing firewall.","rec":"Create UDR 0.0.0.0/0 → FW private IP 10.0.1.4.","cmd":"az network route-table route create -g rg-data --route-table-name rt-data -n force-tunnel --address-prefix 0.0.0.0/0 --next-hop-ip-address 10.0.1.4"},
    ]
    st.session_state.finops=[
        {"save":"$4,280/mo","action":"Rightsize 8 VMs in Dev/Test (avg CPU 11%)","detail":"D4s→D2s (4 VMs), D8s→D4s (2), NC6→NC4 (2). Based on 30-day P95.","cat":"Rightsizing","conf":"High"},
        {"save":"$3,640/mo","action":"Convert 5 Prod VMs to 1-year Reserved Instances","detail":"Stable 24/7 workloads for 6+ months. RI saves 38% vs PAYG.","cat":"Reserved Instance","conf":"High"},
        {"save":"$2,190/mo","action":"Delete 6 orphaned disks + 2 unattached PIPs in Sandbox","detail":"Disks from deleted VMs (45+ days unattached). PIPs with no NIC.","cat":"Orphan Cleanup","conf":"High"},
        {"save":"$1,840/mo","action":"Auto-pause Synapse SQL Pool (off-hours + weekends)","detail":"Runs 24/7 ($5,520/mo). Queries only 6AM-8PM weekdays. 67% idle.","cat":"Scheduling","conf":"High"},
        {"save":"$1,096/mo","action":"Switch GPU VM to Spot Instance for ML training","detail":"Fault-tolerant with checkpointing. Spot: $329/mo vs $1,096 on-demand.","cat":"Spot Instance","conf":"Medium"},
    ]

# ============================================================
# IaC TEMPLATES
# ============================================================
IAC={"Virtual Machine":"""// Bicep - VM with PE + Diagnostics | {ORG}
param location string = resourceGroup().location
param vmName string = '{name}'
var tags = {{ environment: '{env}'; costCenter: '{cc}'; project: 'Meridian-Analytics'; managedBy: 'CloudOps-AI' }}

resource nic 'Microsoft.Network/networkInterfaces@2024-01-01' = {{
  name: '${{vmName}}-nic'; location: location; tags: tags
  properties: {{ ipConfigurations: [{{ name: 'ipconfig1'; properties: {{ subnet: {{ id: subnetId }}; privateIPAllocationMethod: 'Dynamic' }} }}] }}
}}
resource vm 'Microsoft.Compute/virtualMachines@2024-03-01' = {{
  name: vmName; location: location; tags: tags
  identity: {{ type: 'SystemAssigned' }}
  properties: {{
    hardwareProfile: {{ vmSize: '{size}' }}
    osProfile: {{ computerName: vmName; adminUsername: 'fmadmin'; linuxConfiguration: {{ disablePasswordAuthentication: true }} }}
    networkProfile: {{ networkInterfaces: [{{ id: nic.id }}] }}
    securityProfile: {{ securityType: 'TrustedLaunch' }}
  }}
}}
resource diag 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {{
  name: '${{vmName}}-diag'; scope: vm
  properties: {{ workspaceId: logAnalyticsId; metrics: [{{ category: 'AllMetrics'; enabled: true }}] }}
}}""",
"Azure SQL Database":"""// Bicep - SQL + PE + DNS | {ORG}
param sqlName string = '{name}'
var tags = {{ environment: '{env}'; costCenter: '{cc}'; project: 'Meridian-Analytics'; managedBy: 'CloudOps-AI' }}

resource sql 'Microsoft.Sql/servers@2023-08-01-preview' = {{
  name: sqlName; location: location; tags: tags
  properties: {{ administratorLogin: 'fmsqladmin'; minimalTlsVersion: '1.2'; publicNetworkAccess: 'Disabled' }}
}}
resource pe 'Microsoft.Network/privateEndpoints@2024-01-01' = {{
  name: '${{sqlName}}-pe'; location: location; tags: tags
  properties: {{ subnet: {{ id: subnetId }}; privateLinkServiceConnections: [{{ name: 'plsc'; properties: {{ privateLinkServiceId: sql.id; groupIds: ['sqlServer'] }} }}] }}
}}""",
"Storage Account":"""// Bicep - ADLS Gen2 + PE | {ORG}
param storageName string = '{name}'
var tags = {{ environment: '{env}'; costCenter: '{cc}'; project: 'Meridian-Analytics'; managedBy: 'CloudOps-AI' }}

resource sa 'Microsoft.Storage/storageAccounts@2023-05-01' = {{
  name: storageName; location: location; kind: 'StorageV2'; sku: {{ name: '{size}' }}; tags: tags
  properties: {{ isHnsEnabled: true; publicNetworkAccess: 'Disabled'; minimumTlsVersion: 'TLS1_2'; allowBlobPublicAccess: false; supportsHttpsTrafficOnly: true
    networkAcls: {{ defaultAction: 'Deny'; bypass: 'AzureServices' }} }}
}}
resource pe 'Microsoft.Network/privateEndpoints@2024-01-01' = {{
  name: '${{storageName}}-blob-pe'; location: location; tags: tags
  properties: {{ subnet: {{ id: subnetId }}; privateLinkServiceConnections: [{{ name: 'blob-plsc'; properties: {{ privateLinkServiceId: sa.id; groupIds: ['blob'] }} }}] }}
}}"""}

def gen_iac(rt,cfg):
    r=call_claude(f"Generate Bicep for {rt}: {json.dumps(cfg)}. Org: {ORG}. Include PE, diagnostics, tags, Managed Identity. Code only.","Azure IaC expert for FutureMinds. Production Bicep. Code only.")
    if r: return r
    return IAC.get(rt,f"// Template for {rt}").format(name=cfg.get("name","res-01"),size=cfg.get("size","Standard_D2s_v3"),env=cfg.get("env","dev"),cc=cfg.get("cc","IT-Platform"),ORG=ORG)

# ============================================================
# SIDEBAR — mirrors SVG 6-section layout
# ============================================================
with st.sidebar:
    st.markdown(f"""<div style="text-align:center;padding:16px 12px 12px;margin:-1rem -1rem 12px;background:linear-gradient(180deg,#1E293B,#0F172A);border-bottom:1px solid #334155">
    <div style="font-size:32px;margin-bottom:4px">☁️</div>
    <div style="font-size:15px;font-weight:700;color:#E0F2FE">CloudOps Portal</div>
    <div style="font-size:10px;color:#64748B;letter-spacing:.5px;margin-top:2px">{ORG.upper()} - AZURE MULTI-SUB</div></div>""",unsafe_allow_html=True)
    st.markdown(f"""<div style="background:#1E293B;border:1px solid #334155;border-radius:8px;padding:10px 14px;margin-bottom:16px">
    <div style="font-size:10px;color:#94A3B8;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px">Signed in as</div>
    <div style="font-size:14px;font-weight:600;color:#F1F5F9">{st.session_state.persona}</div>
    <div style="font-size:10px;color:#64748B;margin-top:2px">{TENANT}</div></div>""",unsafe_allow_html=True)
    st.session_state.persona=st.selectbox("Switch Persona",["Cloud Engineer","Network Admin","Security Admin","FinOps Analyst","DevOps Engineer","App Owner","Platform Lead"],label_visibility="collapsed")
    page=st.radio("",["① Who Requests","② Portal + AI Engine","③ Risk Routing","④ Pipeline Execution","⑤ Landing Zone Spokes","⑥ Business Outcomes"],label_visibility="collapsed")
    st.markdown("---")
    st.markdown('<div style="font-size:10px;color:#64748B;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;font-weight:600">Subscriptions</div>',unsafe_allow_html=True)
    for n,s,i in [("Hub-Connectivity","Healthy","🟢"),("Prod-LandingZone","Healthy","🟢"),("Dev-Test","Healthy","🟢"),("Data-Platform","1 Advisory","🟡"),("Sandbox-POC","Healthy","🟢")]:
        st.markdown(f'<div style="display:flex;align-items:center;gap:6px;margin:4px 0;font-size:12px"><span>{i}</span><span style="color:#E2E8F0;font-weight:500">{n}</span><span style="color:#64748B;font-size:10px;margin-left:auto">{s}</span></div>',unsafe_allow_html=True)
    st.markdown("---")
    st.caption(f"CloudOps v3.0 - AI: Claude (Anthropic) - (c) 2026 {ORG}")

# HEADER
st.markdown(f'<div class="hdr"><div><h2>☁️ CloudOps Unified Portal</h2><p class="sub">Azure Multi-Subscription - 7 Gen AI Features - {ORG}</p></div><div class="ri"><div class="un">{st.session_state.persona}</div><div class="ut">{TENANT}</div></div></div>',unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# ① WHO REQUESTS — Personas + Auth
# ════════════════════════════════════════════════════════════
if page=="① Who Requests":
    st.markdown('<div class="sec" style="color:#0C4A6E">① WHO REQUESTS</div>',unsafe_allow_html=True)
    st.markdown(f"All {ORG} users authenticate via **Entra ID SSO** (OAuth2 + MFA + Conditional Access) before accessing the portal.")
    personas=[("👨‍💻","Cloud Engineer","Infra provisioning","Requests VMs, AKS clusters, storage, databases. Primary user of AI #1 NL-to-IaC Generator.","Provision, Network"),
              ("🌐","Network Admin","PE, FW, NSG, VPN","Manages Private Endpoints, Azure Firewall rules, NSG policies, VPN/ExpressRoute. Uses AI #5 Network Posture.","Network, Firewall"),
              ("🔐","Security Admin","RBAC, PIM, NSG audit","Reviews access requests, PIM activations, security anomalies. Primary user of AI #4 Access Anomaly.","Access"),
              ("💰","FinOps Analyst","Cost, budgets, RI","Monitors spend, approves cost-impactful resources, manages Reserved Instances. Uses AI #6 FinOps Engine.","Cost"),
              ("⚙️","DevOps Engineer","Pipelines, IaC, CI/CD","Manages deployment pipelines, IaC templates, drift remediation. Uses AI #3 Drift Detector.","Provision, Network"),
              ("📱","App Owner","Workload requests","Business stakeholders requesting resources for their applications. Uses AI #2 Ops Chatbot.","Provision, Access")]
    cols=st.columns(3)
    for idx,(icon,name,scope,desc,types) in enumerate(personas):
        with cols[idx%3]:
            active="border-left:4px solid #0369A1;" if name==st.session_state.persona else "border-left:4px solid transparent;"
            st.markdown(f"""<div style="background:#FFF;border:1px solid #E2E8F0;border-radius:10px;padding:16px;margin:6px 0;box-shadow:0 1px 3px rgba(0,0,0,0.06);{active}">
            <div style="font-size:28px;margin-bottom:6px">{icon}</div>
            <div style="font-size:14px;font-weight:700;color:#0F172A">{name}</div>
            <div style="font-size:10px;color:#94A3B8;margin-bottom:8px">{scope}</div>
            <div style="font-size:12px;color:#475569;line-height:1.5">{desc}</div>
            <div style="margin-top:8px;font-size:10px;color:#0369A1;font-weight:600">Request types: {types}</div></div>""",unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("##### Authentication Flow")
    c1,c2,c3,c4=st.columns(4)
    steps=[("🔑 Entra ID SSO","User signs in with corporate credentials. OAuth2 + PKCE flow.","#0C4A6E"),
           ("🛡️ MFA + Conditional Access","Require MFA from untrusted networks. Block legacy auth.","#7C3AED"),
           ("👤 Persona Detection","Role-based UI: persona derived from Entra ID group membership.","#0369A1"),
           ("✅ Portal Access","User lands on CloudOps Portal with persona-scoped view.","#059669")]
    for col,(title,desc,color) in zip([c1,c2,c3,c4],steps):
        with col:
            st.markdown(f'<div style="background:{color};color:#FFF;border-radius:10px;padding:14px;text-align:center;min-height:120px"><div style="font-size:12px;font-weight:700;margin-bottom:6px">{title}</div><div style="font-size:10px;opacity:.8;line-height:1.4">{desc}</div></div>',unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# ② CLOUDOPS PORTAL + AI ENGINE
# ════════════════════════════════════════════════════════════
elif page=="② Portal + AI Engine":
    st.markdown('<div class="sec" style="color:#7C3AED">② CLOUDOPS PORTAL + AI ENGINE</div>',unsafe_allow_html=True)

    # Portal overview + AI stats
    col1,col2=st.columns([3,2])
    with col1:
        st.markdown(f"""**CloudOps Unified Portal** ingests requests via 4 input methods, processes them through the **7-feature AI Engine**, and outputs production-ready IaC + risk scores.""")
        st.markdown("**Request Types:** Provision | Network | Access | Firewall | Cost")
        st.markdown("**Input Methods:** Guided Form | Natural Language | Teams Bot | REST API")
    with col2:
        st.markdown("**AI at a Glance**")
        for lbl,val,clr in [("Requests scored/mo","523","#7C3AED"),("Auto-approved (low)","74%","#059669"),("Avg approval time","1.8 hrs","#0369A1"),("IaC templates gen'd","47/mo","#7C3AED"),("Policy compliance","96.2%","#059669")]:
            st.markdown(f'<div style="display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid #F1F5F9"><span style="color:#475569;font-size:12px">{lbl}</span><span style="color:{clr};font-weight:700;font-size:13px">{val}</span></div>',unsafe_allow_html=True)

    st.markdown("---")
    ai_tab=st.tabs(["🏗️ #1 NL→IaC","🤖 #2 Chatbot","🔄 #3 Drift","🔐 #4 Access","🛡️ #5 Network","💰 #6 FinOps","⚡ #7 Risk Scorer"])

    # ── AI #1: NL → IaC Generator ──────────────────────────
    with ai_tab[0]:
        st.markdown(f"### {AI(1)} Natural Language → Infrastructure-as-Code",unsafe_allow_html=True)
        st.markdown("Describe infrastructure in plain English. AI generates production Bicep with PE, diagnostics, mandatory tags, Managed Identity.")
        t1,t2=st.tabs(["Guided Form","Natural Language"])
        with t1:
            with st.form("prov",border=True):
                c1,c2=st.columns(2)
                with c1:
                    rt=st.selectbox("Resource Type",["Virtual Machine","Azure SQL Database","Storage Account","AKS Cluster","Cosmos DB","Redis Cache","Function App"])
                    ts=st.selectbox("Target Subscription",["Prod-LandingZone","Dev-Test","Data-Platform","Sandbox-POC"])
                    rn=st.text_input("Resource Name",placeholder="e.g., vm-meridian-api-03")
                    env=st.selectbox("Environment",["Production","Development","Test","Sandbox"])
                with c2:
                    skus={"Virtual Machine":["Standard_D2s_v5","Standard_D4s_v5","Standard_D8s_v5","Standard_NC6s_v3 (GPU)"],"Azure SQL Database":["GP_Gen5_2","GP_Gen5_4","BC_Gen5_4"],"Storage Account":["Standard_LRS","Standard_GRS","Premium_LRS"],"AKS Cluster":["Standard_D4s_v5/node"],"Cosmos DB":["Serverless","400 RU/s","4000 RU/s"]}
                    sku=st.selectbox("SKU",skus.get(rt,["Standard"]))
                    region=st.selectbox("Region",["East US 2 (Primary)","West Europe (DR)","Central US"])
                    cc=st.text_input("Cost Center",value="IT-Platform")
                    just=st.text_area("Justification",placeholder="Required for Meridian v2.4 analytics pipeline...",height=80)
                sub=st.form_submit_button("Generate IaC + Submit Request",type="primary",use_container_width=True)
                if sub and rn:
                    cfg={"name":rn,"size":sku.split(" ")[0],"env":env.lower(),"cc":cc}
                    with st.spinner("AI generating IaC + policy pre-flight..."):
                        time.sleep(1)
                    rid=f"REQ-{random.randint(2700,2999)}"
                    risk="Low" if env in ["Development","Sandbox"] else "Medium" if env=="Test" else "High"
                    score=round(random.uniform(1.5,3.5) if risk=="Low" else random.uniform(4,6.5) if risk=="Medium" else random.uniform(7,9),1)
                    st.success(f"Request **{rid}** submitted!")
                    ca,cb=st.columns(2)
                    with ca:
                        st.markdown("**Policy Pre-flight:**")
                        for chk,res in [("Region allowed","Pass"),("SKU in catalog","Pass"),("Naming convention","Pass" if "-" in rn else "Warn"),("Mandatory tags","Pass"),("Private Endpoint","Auto-attached"),("Diagnostics","Auto-configured"),("Managed Identity","SystemAssigned")]:
                            st.markdown(f"{'✅' if res=='Pass' else '⚠️'} {chk}")
                    with cb:
                        st.markdown(f"**Risk Assessment:** {score}/10 {B(risk)}",unsafe_allow_html=True)
                        if risk=="Low": st.markdown(RB("✅ <strong>Auto-Approved</strong> - Pipeline triggers instantly.","ok"),unsafe_allow_html=True)
                        elif risk=="Medium": st.markdown(RB("⏳ <strong>L1 Approval</strong> - Teams card sent. SLA: 4 hrs.","wn"),unsafe_allow_html=True)
                        else: st.markdown(RB("🔒 <strong>L1+L2+CISO</strong> - Multi-level review. SLA: 24 hrs.","cr"),unsafe_allow_html=True)
                    st.markdown("**AI-Generated Bicep:**")
                    st.code(gen_iac(rt,cfg),language="bicep")
        with t2:
            nl=st.text_area("Describe your infrastructure need:",placeholder="I need a 3-node AKS cluster in production with private API, Azure CNI, connected to Meridian SQL via PE...",height=120,label_visibility="collapsed")
            if st.button("Generate from Description",type="primary",use_container_width=True) and nl:
                with st.spinner("AI analyzing..."):
                    r=call_claude(f"Request: {nl}\nOrg: {ORG}, Project: {PROJECT}. Generate: resource list + cost + risk + Bicep.",f"Azure IaC expert for {ORG}. Format: ## Resources, ## Cost, ## Risk, ## Bicep")
                    if r: st.markdown(r)
                    else:
                        st.markdown("**Resources:** AKS (3+autoscale) $876/mo | PE $7/mo | Container Insights ~$120/mo\n\n**Risk:** 7.8/10 (High) - Production AKS + custom networking = L1+L2 approval")
                        st.code(gen_iac("Virtual Machine",{"name":"aks-meridian-prod","size":"Standard_D4s_v5","env":"production","cc":"IT-Platform"}),language="bicep")

    # ── AI #2: Ops Chatbot ─────────────────────────────────
    with ai_tab[1]:
        st.markdown(f"### {AI(2)} CloudOps Copilot",unsafe_allow_html=True)
        st.markdown(f"Ask anything about {ORG}'s Azure environment. AI has context on subscriptions, policies, cost, compliance.")
        for m in st.session_state.chat:
            cls="cu" if m["role"]=="user" else "ca"
            st.markdown(f'<div class="{cls}">{"👤" if m["role"]=="user" else "🤖"} {m["content"]}</div>',unsafe_allow_html=True)
        qcols=st.columns(4)
        qps=["Show untagged resources","Over-provisioned VMs in Dev/Test?","PIM roles expiring this week?","Cosmos DB Bicep with geo-rep"]
        for i,qp in enumerate(qps):
            if qcols[i].button(qp,key=f"q_{i}",use_container_width=True):
                st.session_state.chat.append({"role":"user","content":qp}); st.rerun()
        msg=st.chat_input("Ask the CloudOps AI...")
        if msg:
            st.session_state.chat.append({"role":"user","content":msg})
            ctx=f"CloudOps AI for {ORG}. 5 Azure subs, 847 resources, $142K/mo, 96.2% compliance. Project: {PROJECT}. Persona: {st.session_state.persona}. Concise, actionable."
            with st.spinner("Thinking..."):
                resp=call_claude(msg,ctx)
                if not resp:
                    ml=msg.lower()
                    if "untag" in ml: resp="**Untagged Resources:**\n\n| Resource | Type | Sub |\n|---|---|---|\n| vm-test-scratch-03 | VM | Sandbox |\n| disk-orphan-data-01 | Disk | Dev/Test |\n| pip-unused-02 | PIP | Sandbox |\n\nFix: `az tag create --resource-id <id> --tags costCenter=IT-Platform environment=dev project=Meridian-Analytics`"
                    elif "over" in ml or "provision" in ml: resp="**Over-Provisioned VMs (30d P95):**\n\n| VM | SKU | CPU | Rec | Save |\n|---|---|---|---|---|\n| vm-dev-api-01 | D4s_v5 | 8% | D2s_v5 | $73/mo |\n| vm-dev-api-02 | D4s_v5 | 12% | D2s_v5 | $73/mo |\n| vm-test-worker-01 | D8s_v5 | 6% | D4s_v5 | $146/mo |\n\n**Total: $1,059/mo savings**"
                    elif "pim" in ml or "expir" in ml: resp="**PIM Expiring This Week:**\n\n| User | Role | Scope | Expires |\n|---|---|---|---|\n| priya.s@ | Contributor | Prod | Feb 14 |\n| devon.l@ | Network Contrib | Hub | Feb 13 |\n| ext-auditor@pwc.com | Reader | rg-compliance | Feb 12 |"
                    elif "cosmos" in ml: resp="```bicep\nresource cosmos 'Microsoft.DocumentDB/databaseAccounts@2024-02-15-preview' = {\n  name: 'cosmos-meridian-prod'\n  location: 'East US 2'\n  tags: { environment: 'production'; project: 'Meridian-Analytics' }\n  properties: {\n    locations: [\n      { locationName: 'East US 2'; failoverPriority: 0 }\n      { locationName: 'West Europe'; failoverPriority: 1 }\n    ]\n    publicNetworkAccess: 'Disabled'\n  }\n}\n```"
                    else: resp="I can help with provisioning, networking, access, cost optimization, compliance, or any Azure ops question. Add `ANTHROPIC_API_KEY` in secrets for live AI."
                st.session_state.chat.append({"role":"assistant","content":resp}); st.rerun()
        if st.button("Clear chat"): st.session_state.chat=[]; st.rerun()

    # ── AI #3: Drift Detector ──────────────────────────────
    with ai_tab[2]:
        st.markdown(f"### {AI(3)} Resource Drift Detector",unsafe_allow_html=True)
        st.markdown("Compares ARM live state vs IaC Git repo. Detects unauthorized manual changes.")
        c1,c2,c3,c4=st.columns(4)
        with c1: st.markdown(K("Scanned","847","Hourly"),unsafe_allow_html=True)
        with c2: st.markdown(K("Drifted","6","3 fewer vs last wk"),unsafe_allow_html=True)
        with c3: st.markdown(K("Auto-Fixed PRs","14","This month"),unsafe_allow_html=True)
        with c4: st.markdown(K("Pending","3","Need human","dn"),unsafe_allow_html=True)
        st.markdown("---")
        for d in st.session_state.drifts:
            with st.expander(f"{SI(d['sev'])} **{d['res']}** ({d['type']}) - {d['drift'][:65]}... [{d['age']}]",expanded=d["sev"]=="Critical"):
                st.markdown(f"**Sub:** {d['sub']} | **Severity:** {B(d['sev'])} | **IaC:** `{d['iac']}`",unsafe_allow_html=True)
                st.markdown(f"**Detail:** {d['detail']}")
                lv="cr" if d["sev"]=="Critical" else "wn" if d["sev"] in ["High","Medium"] else "ok"
                st.markdown(RB(f"🤖 <strong>AI Fix:</strong> {d['fix']}",lv),unsafe_allow_html=True)
                c1,c2,c3=st.columns(3)
                if c1.button("Revert to IaC",key=f"fx_{d['res']}",use_container_width=True): st.success(f"PR #{random.randint(200,400)} created. CI validating.")
                if c2.button("Accept Drift",key=f"ac_{d['res']}",use_container_width=True): st.info("IaC updated to match live state. PR for review.")
                if c3.button("View Diff",key=f"df_{d['res']}",use_container_width=True):
                    st.code(f"--- a/{d['iac']}   (IaC repo)\n+++ b/ARM live state\n\n- // Original config\n+ // DRIFT: {d['drift']}\n+ // Changed by: Portal user ({d['age']} ago)\n+ // Detected by: AI #3 (hourly scan)",language="diff")

    # ── AI #4: Access Anomaly ──────────────────────────────
    with ai_tab[3]:
        st.markdown(f"### {AI(4)} Access Anomaly Detection + RBAC AI",unsafe_allow_html=True)
        st.markdown(f"Analyzes Entra ID sign-ins, RBAC, PIM patterns. Detects stale SPNs, over-priv, impossible travel.")
        c1,c2,c3,c4=st.columns(4)
        with c1: st.markdown(K("Identities","234","Users+SPNs+Groups"),unsafe_allow_html=True)
        with c2: st.markdown(K("Anomalies","5","Last 7 days","dn"),unsafe_allow_html=True)
        with c3: st.markdown(K("Stale","4","90+ days","dn"),unsafe_allow_html=True)
        with c4: st.markdown(K("Over-Priv","3","Recommend downgrade","dn"),unsafe_allow_html=True)
        st.markdown("---")
        t1,t2=st.tabs(["Anomaly Findings","Sign-in Heatmap"])
        with t1:
            for a in st.session_state.anomalies:
                with st.expander(f"{SI(a['sev'])} [{a['type']}] {a['id']}: {a['finding'][:70]}...",expanded=a["sev"]=="Critical"):
                    st.markdown(f"**Severity:** {B(a['sev'])} | **Type:** {B(a['type'])} | **Risk:** {a['score']}/10",unsafe_allow_html=True)
                    st.markdown(f"**Detail:** {a['detail']}")
                    lv="cr" if a["sev"]=="Critical" else "wn" if a["sev"]=="High" else "ok"
                    st.markdown(RB(f"🤖 <strong>Recommendation:</strong> {a['rec']}",lv),unsafe_allow_html=True)
                    if a["sev"] in ["Critical","High"]:
                        c1,c2=st.columns(2)
                        if c1.button("Apply Fix",key=f"af_{a['id'][:10]}",type="primary",use_container_width=True): st.success("Applied. Audit logged. User notified.")
                        if c2.button("Create Incident",key=f"ci_{a['id'][:10]}",use_container_width=True): st.info(f"ServiceNow INC-{random.randint(4800,4999)} created.")
        with t2:
            hours=list(range(24))
            normal=[3,2,1,1,0,1,6,22,48,44,40,35,32,36,42,44,38,26,14,10,8,6,5,4]
            anom=[0,0,0,4,6,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            fig=go.Figure()
            fig.add_trace(go.Bar(x=hours,y=normal,name="Normal",marker_color="#0369A1",opacity=.85))
            fig.add_trace(go.Bar(x=hours,y=anom,name="Anomalous",marker_color="#DC2626"))
            fig.update_layout(height=280,margin=dict(l=0,r=0,t=10,b=0),barmode="stack",xaxis_title="Hour (UTC)",yaxis_title="Sign-ins",plot_bgcolor="white",legend=dict(orientation="h",y=-.2))
            st.plotly_chart(fig,use_container_width=True)
            st.caption("Anomalous cluster at 3-5 AM UTC = ext-contractor-rajesh impossible travel.")

    # ── AI #5: Network Posture ─────────────────────────────
    with ai_tab[4]:
        st.markdown(f"### {AI(5)} Network Posture Analyzer",unsafe_allow_html=True)
        st.markdown(f"Scans NSG, Firewall, UDR, PE configs against CIS benchmarks + {ORG} policies.")
        c1,c2,c3,c4=st.columns(4)
        with c1: st.markdown(K("Posture","87/100","Up 4 this month"),unsafe_allow_html=True)
        with c2: st.markdown(K("NSGs","24","All subs"),unsafe_allow_html=True)
        with c3: st.markdown(K("FW Rules","47","5 conflicts","dn"),unsafe_allow_html=True)
        with c4: st.markdown(K("Findings","5","2 critical","dn"),unsafe_allow_html=True)
        st.markdown("---")
        t1,t2=st.tabs(["CIS Findings","Network Topology"])
        with t1:
            for f in st.session_state.net_findings:
                with st.expander(f"{SI(f['sev'])} [{f['cis']}] {f['finding']} - {f['sub']}",expanded=f["sev"]=="Critical"):
                    st.markdown(f"**Impact:** {f['impact']}")
                    lv="cr" if f["sev"]=="Critical" else "wn" if f["sev"]=="High" else "ok"
                    st.markdown(RB(f"🤖 <strong>Recommendation:</strong> {f['rec']}",lv),unsafe_allow_html=True)
                    st.markdown("**Remediation CLI:**")
                    st.code(f["cmd"],language="bash")
                    if st.button("Execute Remediation",key=f"nr_{f['cis']}",use_container_width=True): st.success("Pipeline triggered. PR created. Validating...")
        with t2:
            st.code(f"""Hub VNet (10.0.0.0/16) --- Connectivity Subscription
+-- AzureFirewallSubnet (10.0.1.0/24) -- Azure Firewall [DNAT+App+Net]
|   Private IP: 10.0.1.4 (force-tunnel target)
+-- GatewaySubnet (10.0.2.0/24) -------- ExpressRoute 2Gbps -> On-Prem
+-- AzureBastionSubnet (10.0.3.0/24) --- Bastion Host
+-- AppSubnet (10.0.10.0/24) ----------- APIM + Functions + OpenAI PE
|
+-- [Peering] -> Prod (10.1.0.0/16)
|   +-- snet-aks (10.1.1.0/24) --------- AKS (private API)
|   +-- snet-pe (10.1.2.0/24) ---------- SQL MI PE, Cosmos PE, Redis PE
|   +-- snet-apps (10.1.3.0/24) -------- App Services (VNet integrated)
|
+-- [Peering] -> Dev/Test (10.2.0.0/16)
|   +-- snet-dev (10.2.1.0/24) --------- Dev VMs, UAT
|   +-- snet-sandbox (10.2.2.0/24) ----- Auto-provisioned sandboxes
|   ** NSG: SSH from 0.0.0.0/0 OPEN - REMEDIATE (CIS 6.2)
|
+-- [Peering] -> Data Platform (10.3.0.0/16)
|   +-- snet-data (10.3.1.0/24) -------- ADLS, Synapse, ADF, Informatica
|   +-- snet-ml (10.3.2.0/24) ---------- ML Compute (GPU)
|   ** UDR: Missing force-tunnel - REMEDIATE (CIS 6.1)
|
+-- On-Premises (ExpressRoute)
    Source Systems: Oracle R12, Salesforce, SAP S/4HANA""",language="text")

    # ── AI #6: FinOps AI ───────────────────────────────────
    with ai_tab[5]:
        st.markdown(f"### {AI(6)} FinOps AI Engine",unsafe_allow_html=True)
        st.markdown(f"Monitors {ORG}'s $142K/mo spend. Anomaly detection, forecasting, rightsizing, RI, orphan cleanup.")
        c1,c2,c3,c4=st.columns(4)
        with c1: st.markdown(K("Feb MTD","$68.4K","On track"),unsafe_allow_html=True)
        with c2: st.markdown(K("Forecast","$138.2K","$3.8K under budget"),unsafe_allow_html=True)
        with c3: st.markdown(K("AI Savings","$13.0K/mo","5 recommendations"),unsafe_allow_html=True)
        with c4: st.markdown(K("Anomalies","2","1 open","dn"),unsafe_allow_html=True)
        st.markdown("---")
        t1,t2,t3=st.tabs(["Cost Breakdown","Savings Recs","Anomalies"])
        with t1:
            np.random.seed(99)
            subs=["Production","Dev/Test","Data Platform","Hub","Sandbox"]
            svcs=["Compute","Database","Storage","Network","AI/ML","Other"]
            data=[]
            for s in subs:
                mult=3.2 if s=="Production" else 2.0 if s=="Data Platform" else 1.5 if s=="Dev/Test" else .9 if s=="Hub" else .5
                for v in svcs: data.append({"Subscription":s,"Service":v,"Cost ($K)":round(np.random.uniform(.5,8)*mult,1)})
            fig=px.bar(pd.DataFrame(data),x="Subscription",y="Cost ($K)",color="Service",color_discrete_sequence=["#0369A1","#7C3AED","#059669","#DC2626","#D97706","#64748B"])
            fig.update_layout(height=320,margin=dict(l=0,r=0,t=10,b=0),plot_bgcolor="white",legend=dict(orientation="h",y=-.2))
            st.plotly_chart(fig,use_container_width=True)
            # Forecast
            np.random.seed(42)
            dates=pd.date_range("2026-02-01",periods=28,freq="D")
            actual=[4.8+np.random.uniform(-.3,.5) for _ in range(11)]
            forecast=[actual[-1]+(i*.12)+np.random.uniform(-.2,.2) for i in range(17)]
            fig2=go.Figure()
            fig2.add_trace(go.Scatter(x=dates[:11],y=actual,name="Actual",mode="lines+markers",line=dict(color="#0369A1",width=2.5)))
            fig2.add_trace(go.Scatter(x=dates[10:],y=[actual[-1]]+forecast,name="AI Forecast",mode="lines",line=dict(color="#7C3AED",width=2,dash="dash")))
            fig2.add_hline(y=5.1,line_dash="dot",line_color="#DC2626",annotation_text="Daily Budget")
            fig2.update_layout(height=200,margin=dict(l=0,r=0,t=10,b=0),plot_bgcolor="white",legend=dict(orientation="h",y=-.3),yaxis_title="$/day (K)")
            st.plotly_chart(fig2,use_container_width=True)
        with t2:
            st.markdown(f"**Total Potential Savings: $13.0K/mo ($156K/yr)**")
            for rec in st.session_state.finops:
                st.markdown(f"""<div class="sc" style="border-left-color:{'#059669' if rec['conf']=='High' else '#D97706'}">
                <div style="display:flex;justify-content:space-between"><h4>{rec['action']}</h4><span style="font-size:18px;font-weight:700;color:#059669">{rec['save']}</span></div>
                <div style="font-size:11px;color:#94A3B8;margin-bottom:6px">{rec['cat']} | Confidence: {B(rec['conf'])}</div>
                <div style="font-size:12px;color:#475569">{rec['detail']}</div></div>""",unsafe_allow_html=True)
                if st.button(f"Apply: {rec['cat']}",key=f"fn_{rec['save']}",use_container_width=True): st.success(f"Optimization applied. Annual savings: ${float(rec['save'].replace('$','').replace(',','').replace('/mo',''))*12:,.0f}")
        with t3:
            st.markdown(RB("🚨 <strong>OPEN - Data Platform</strong><br>Synapse SQL Pool spend spiked 42% ($187 to $266 in 24h). Auto-pause job failed (expired MI credential). Excess: ~$340/day.<br><strong>AI Fix:</strong> Credential rotated. Auto-pause re-enabled. Alert set.","cr"),unsafe_allow_html=True)
            st.markdown(RB("✅ <strong>RESOLVED - Sandbox</strong><br>Spend dropped to $0 (from $28/day avg). Auto-cleanup removed all resources per 14-day TTL. Expected behavior.","ok"),unsafe_allow_html=True)

    # ── AI #7: Risk Scorer ─────────────────────────────────
    with ai_tab[6]:
        st.markdown(f"### {AI(7)} Risk Scorer + Automated Approvals",unsafe_allow_html=True)
        st.markdown(f"Every request AI-scored 1-10. Low auto-approves. Med/High route through tiered chains.")
        c1,c2,c3,c4=st.columns(4)
        with c1: st.markdown(K("Scored","523","This month"),unsafe_allow_html=True)
        with c2: st.markdown(K("Auto-Approved","387","74%"),unsafe_allow_html=True)
        with c3: st.markdown(K("Manual","136","26%"),unsafe_allow_html=True)
        with c4: st.markdown(K("Avg Time","1.8 hrs","Was 18 hrs"),unsafe_allow_html=True)
        st.markdown("---")
        # Risk tier cards
        r1,r2,r3=st.columns(3)
        with r1: st.markdown('<div class="rt" style="background:#D1FAE5;border:2px solid #6EE7B7"><div class="s" style="color:#065F46">Low (1-3)</div><div class="lb" style="color:#065F46">✅ Auto-Approved</div><div class="dt" style="color:#065F46">Zero human touch. Pipeline triggers instantly.<br>Dev/Sandbox, Reader, tags, known templates</div></div>',unsafe_allow_html=True)
        with r2: st.markdown('<div class="rt" style="background:#FEF3C7;border:2px solid #FCD34D"><div class="s" style="color:#92400E">Med (4-6)</div><div class="lb" style="color:#92400E">⏳ L1 Approver (Teams)</div><div class="dt" style="color:#92400E">SLA: 4 hours. Auto-escalate if breached.<br>Test env, Contributor, FW rules</div></div>',unsafe_allow_html=True)
        with r3: st.markdown('<div class="rt" style="background:#FEE2E2;border:2px solid #FCA5A5"><div class="s" style="color:#991B1B">High (7-10)</div><div class="lb" style="color:#991B1B">🔒 L1+L2+CISO</div><div class="dt" style="color:#991B1B">SLA: 24 hours. VP escalation if breached.<br>Production, Owner, GPU, NSG 0.0.0.0/0</div></div>',unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("##### Pending Approvals")
        for a in [x for x in st.session_state.approvals if x["status"]=="Awaiting Approval"]:
            ico="🔴" if a["risk_level"]=="High" else "🟡"
            with st.expander(f"{ico} {a['id']} - {a['desc']} (Score: {a['risk_score']}/10)",expanded=True):
                c1,c2=st.columns([3,2])
                with c1:
                    st.markdown(f"**Req:** {a['req']} | **Type:** `{a['type']}` | **Risk:** {B(a['risk_level'])} **{a['risk_score']}**/10",unsafe_allow_html=True)
                    st.markdown("**Score Breakdown:**")
                    for f,v in a["factors"].items(): st.markdown(f"- **{f}:** {v}")
                with c2:
                    lv="cr" if a["risk_level"]=="High" else "wn"
                    st.markdown(RB(f"🤖 <strong>AI:</strong> {a['ai_rec']}",lv),unsafe_allow_html=True)
                b1,b2,b3=st.columns(3)
                if b1.button("Approve",key=f"ap_{a['id']}",type="primary",use_container_width=True): a["status"]="Approved"; st.success("Approved! Pipeline triggered."); st.rerun()
                if b2.button("Reject",key=f"rj_{a['id']}",use_container_width=True): a["status"]="Rejected"; st.error("Rejected. Requestor notified."); st.rerun()
                if b3.button("Request Info",key=f"ri_{a['id']}",use_container_width=True): st.info("Teams msg sent to requestor.")
        st.markdown("---")
        st.markdown("##### Recent Scoring Log")
        st.dataframe(pd.DataFrame([
            {"ID":"REQ-2605","Type":"Sandbox","Score":"1.9","Level":"Low","Decision":"✅ Auto","Time":"< 1 min"},
            {"ID":"REQ-2604","Type":"FW Rule","Score":"4.8","Level":"Med","Decision":"✅ L1","Time":"47 min"},
            {"ID":"REQ-2601","Type":"AKS Prod","Score":"7.4","Level":"High","Decision":"✅ L1+L2+CISO","Time":"5.2 hrs"},
            {"ID":"REQ-2606","Type":"Reader","Score":"2.1","Level":"Low","Decision":"✅ Auto","Time":"< 1 min"},
            {"ID":"REQ-2599","Type":"NSG 0.0.0.0/0","Score":"9.8","Level":"High","Decision":"❌ Rejected","Time":"Instant"},
        ]),use_container_width=True,hide_index=True)

# ════════════════════════════════════════════════════════════
# ③ INTELLIGENT RISK ROUTING
# ════════════════════════════════════════════════════════════
elif page=="③ Risk Routing":
    st.markdown('<div class="sec" style="color:#D97706">③ INTELLIGENT RISK ROUTING</div>',unsafe_allow_html=True)
    st.markdown("Every request passes through the **AI Risk Diamond**. Score determines routing path automatically.")

    # Visual risk routing
    r1,r2,r3=st.columns(3)
    with r1:
        st.markdown("""<div style="background:#D1FAE5;border:2px solid #6EE7B7;border-radius:14px;padding:24px;text-align:center">
        <div style="font-size:36px;font-weight:800;color:#065F46">1-3</div>
        <div style="font-size:16px;font-weight:700;color:#065F46;margin:8px 0">✅ Auto-Approved</div>
        <div style="font-size:12px;color:#059669;font-weight:600">Zero human touch</div>
        <div style="font-size:11px;color:#065F46;margin-top:12px;line-height:1.6">Pipeline triggers instantly.<br>Dev/Sandbox environments.<br>Reader roles, tag changes.<br>Known templates only.</div>
        <div style="margin-top:12px;background:#065F46;color:#FFF;border-radius:8px;padding:8px;font-size:11px;font-weight:600">SLA: 5-15 minutes (full auto)</div>
        </div>""",unsafe_allow_html=True)
    with r2:
        st.markdown("""<div style="background:#FEF3C7;border:2px solid #FCD34D;border-radius:14px;padding:24px;text-align:center">
        <div style="font-size:36px;font-weight:800;color:#92400E">4-6</div>
        <div style="font-size:16px;font-weight:700;color:#92400E;margin:8px 0">⏳ L1 Approval</div>
        <div style="font-size:12px;color:#D97706;font-weight:600">Teams Adaptive Card</div>
        <div style="font-size:11px;color:#92400E;margin-top:12px;line-height:1.6">Platform Lead reviews.<br>Test environment deploys.<br>Contributor role assignments.<br>Firewall rule additions.</div>
        <div style="margin-top:12px;background:#92400E;color:#FFF;border-radius:8px;padding:8px;font-size:11px;font-weight:600">SLA: 1-4 hours (auto-escalate)</div>
        </div>""",unsafe_allow_html=True)
    with r3:
        st.markdown("""<div style="background:#FEE2E2;border:2px solid #FCA5A5;border-radius:14px;padding:24px;text-align:center">
        <div style="font-size:36px;font-weight:800;color:#991B1B">7-10</div>
        <div style="font-size:16px;font-weight:700;color:#991B1B;margin:8px 0">🔒 L1+L2+CISO</div>
        <div style="font-size:12px;color:#DC2626;font-weight:600">Multi-Level Review Chain</div>
        <div style="font-size:11px;color:#991B1B;margin-top:12px;line-height:1.6">Production deployments.<br>Owner role grants.<br>GPU provisioning (>$1K/mo).<br>NSG rules with 0.0.0.0/0.</div>
        <div style="margin-top:12px;background:#991B1B;color:#FFF;border-radius:8px;padding:8px;font-size:11px;font-weight:600">SLA: 4-24 hours (VP escalation)</div>
        </div>""",unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("##### AI Risk Scoring Factors (Weighted Model)")
    factors=pd.DataFrame([
        {"Factor":"Target Environment","Low":"Dev/Sandbox (+0)","Medium":"Test (+1)","High":"Production (+3)","Weight":"30%"},
        {"Factor":"Resource Type","Low":"Tags, Reader (+0)","Medium":"VM, Storage (+1)","High":"AKS, SQL MI, GPU (+2-3)","Weight":"20%"},
        {"Factor":"Permission Scope","Low":"Reader, custom scoped (+0)","Medium":"Contributor (RG) (+1-2)","High":"Owner, subscription (+3)","Weight":"20%"},
        {"Factor":"Network Exposure","Low":"PE only, internal (+0)","Medium":"VNet-integrated (+1)","High":"Public IP, 0.0.0.0/0 (+3)","Weight":"15%"},
        {"Factor":"Cost Impact","Low":"< $100/mo (+0)","Medium":"$100-500/mo (+1)","High":"> $500/mo (+2-3)","Weight":"10%"},
        {"Factor":"Template Match","Low":"Exact match (+0)","Medium":"Minor variation (+1)","High":"Custom / no template (+2)","Weight":"5%"},
    ])
    st.dataframe(factors,use_container_width=True,hide_index=True)

    st.markdown("---")
    st.markdown("##### Live Request Simulation")
    sim_type=st.selectbox("Simulate request:",["Dev sandbox VM (Standard_D2s, Dev/Test)","Production AKS cluster (3-node, private API)","Reader role for auditor (PwC, Production)","GPU VM for ML training (NC6s_v3, Data Platform)","NSG rule: Allow SSH from 0.0.0.0/0 (Production)"])
    if st.button("Run AI Risk Assessment",type="primary"):
        sims={"Dev sandbox":("1.9","Low","✅ Auto-Approved","< 1 min","Dev env + known template + low cost = minimal risk"),
              "Production AKS":("7.4","High","🔒 L1+L2+CISO Required","SLA 24h","Prod (+3) + AKS compute-intensive (+2) + custom networking (+2)"),
              "Reader role":("2.1","Low","✅ Auto-Approved","< 1 min","Reader is read-only (+0) + time-bound (+0) + Prod (+2)"),
              "GPU VM":("8.6","High","🔒 L1+L2+CTO Required","SLA 24h","GPU $1,096/mo (+3) + Data Platform (+1) + compute-intensive (+2) + GPU policy (+2)"),
              "NSG rule":("9.8","High","❌ Auto-Rejected by AI","Instant","0.0.0.0/0 in Production = automatic block. Security policy violation.")}
        key=next((k for k in sims if k in sim_type),None)
        if key:
            sc,lv,dec,tm,expl=sims[key]
            lvc="cr" if lv=="High" else "wn" if lv=="Medium" else "ok"
            st.markdown(f"**Score:** {sc}/10 | **Level:** {B(lv)} | **Decision:** {dec} | **Time:** {tm}",unsafe_allow_html=True)
            st.markdown(RB(f"🤖 <strong>Explanation:</strong> {expl}",lvc),unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# ④ IaC PIPELINE EXECUTION
# ════════════════════════════════════════════════════════════
elif page=="④ Pipeline Execution":
    st.markdown('<div class="sec" style="color:#0369A1">④ IaC PIPELINE EXECUTION</div>',unsafe_allow_html=True)
    st.markdown("After approval, the IaC pipeline executes a **5-stage deployment chain** with zero manual intervention.")

    stages=[
        ("1. Lint + Security Scan","#0C4A6E","Checkov, tflint, Bicep validate","Static analysis of generated IaC. Checks for security misconfigs (open ports, missing encryption, public access). Blocks if any HIGH severity findings.",
         ["Checkov CKV_AZURE_35: Ensure Storage default action is Deny - PASS","tflint: No issues found (0 errors, 0 warnings)","Bicep validate: Template is valid","Credential scan: No secrets detected in template"]),
        ("2. Policy What-If","#0369A1","Region, SKU, Tags, PE, TLS","Azure Policy dry-run. Validates against FutureMinds policies before any resource creation. Catches non-compliant configs before they reach Azure.",
         ["Region: East US 2 - ALLOWED","SKU: Standard_D4s_v5 - APPROVED CATALOG","Tags: environment, costCenter, project, managedBy - ALL PRESENT","Private Endpoint: Auto-configured - COMPLIANT","TLS Minimum: 1.2 - COMPLIANT","Public Access: Disabled - COMPLIANT"]),
        ("3. Terraform Plan","#7C3AED","Diff preview, cost estimate","Generates execution plan showing exactly what will be created/modified/destroyed. AI estimates monthly cost impact before deployment.",
         ["Plan: 4 to add, 0 to change, 0 to destroy","+resource azurerm_kubernetes_cluster.meridian_prod","+resource azurerm_private_endpoint.aks_pe","+resource azurerm_private_dns_zone_virtual_network_link.aks","+resource azurerm_monitor_diagnostic_setting.aks_diag","Estimated cost: +$876/mo"]),
        ("4. ARM Deploy","#059669","Managed Identity, zero secrets","Azure Resource Manager deploys resources using Managed Identity (no stored credentials). Resources created with PE, diagnostics, and tags from the start.",
         ["Deploying to: sub-prod-landingzone / rg-meridian-prod","Identity: Managed Identity (SystemAssigned)","Private Endpoint: Creating in snet-pe (10.1.2.0/24)","DNS Zone: A record added to privatelink.azurecr.io","Diagnostics: Connected to law-futureminds-central","Status: Succeeded (2m 34s)"]),
        ("5. AI Validate + Notify","#059669","PE check, DNS, Teams, ServiceNow","Post-deployment AI validation confirms resource matches spec: connectivity tested, PE resolves correctly, diagnostics flowing, tags present.",
         ["PE connectivity: 10.1.2.47 resolves correctly - PASS","DNS resolution: meridian-prod.privatelink.database.windows.net - PASS","Diagnostics: Metrics flowing to Log Analytics - PASS","Tags: All 4 mandatory tags present - PASS","Teams: Notification sent to Priya S. (requestor)","ServiceNow: CHG-8847 auto-closed as successful"]),
    ]
    for title,color,sub,desc,checks in stages:
        with st.expander(f"**{title}** - {sub}",expanded=True):
            st.markdown(f"<div style='color:{color};font-size:13px;line-height:1.6'>{desc}</div>",unsafe_allow_html=True)
            st.markdown("**Sample Output (REQ-2601: AKS Production):**")
            for c in checks:
                icon="✅" if "PASS" in c or "COMPLIANT" in c or "ALLOWED" in c or "PRESENT" in c or "Succeeded" in c or "APPROVED" in c or "valid" in c.lower() or "No issues" in c or "No secrets" in c else "📋"
                st.markdown(f"``{icon}`` `{c}`")

    st.markdown("---")
    st.markdown("##### Pipeline Execution History")
    st.dataframe(pd.DataFrame([
        {"Request":"REQ-2601","Type":"AKS Prod","Lint":"✅ 0s","Policy":"✅ 3s","Plan":"✅ 12s","Deploy":"✅ 2m34s","Validate":"✅ 8s","Total":"2m 57s","Status":"Deployed"},
        {"Request":"REQ-2605","Type":"Sandbox SQL","Lint":"✅ 0s","Policy":"✅ 1s","Plan":"✅ 5s","Deploy":"✅ 47s","Validate":"✅ 4s","Total":"57s","Status":"Deployed"},
        {"Request":"REQ-2604","Type":"FW Rule","Lint":"✅ 0s","Policy":"✅ 2s","Plan":"✅ 3s","Deploy":"✅ 18s","Validate":"✅ 2s","Total":"25s","Status":"Deployed"},
        {"Request":"REQ-2599","Type":"NSG 0.0.0.0/0","Lint":"❌ HIGH","Policy":"BLOCKED","Plan":"-","Deploy":"-","Validate":"-","Total":"3s","Status":"Rejected"},
    ]),use_container_width=True,hide_index=True)

# ════════════════════════════════════════════════════════════
# ⑤ AZURE LANDING ZONE SPOKES
# ════════════════════════════════════════════════════════════
elif page=="⑤ Landing Zone Spokes":
    st.markdown('<div class="sec" style="color:#0F172A">⑤ AZURE LANDING ZONE - MULTI-SUBSCRIPTION DEPLOYMENT TARGETS</div>',unsafe_allow_html=True)
    st.markdown("Resources deploy into the correct subscription spoke based on request type and target environment. All spokes are VNet-peered to the Hub.")

    # 4 main spokes
    c1,c2=st.columns(2)
    with c1:
        st.markdown("""<div class="spoke"><div class="sh" style="background:#DC2626">🔴 Hub-Connectivity (10.0.0.0/16)</div><div class="sb">
        <strong>Central networking services:</strong><br>
        🔥 Azure Firewall (DNAT + App + Network Rules)<br>
        🌐 ExpressRoute GW 2Gbps to On-Prem (Oracle, SAP)<br>
        🔒 Azure Bastion (secure VM access, no public IPs)<br>
        🤖 Azure OpenAI PE + AI Search PE<br>
        📡 APIM + Azure Functions (Portal backend)<br><br>
        <span style="color:#DC2626;font-weight:600;font-size:11px">Deploys here: FW rules, VPN configs, APIM policies, DNS zones</span>
        </div></div>""",unsafe_allow_html=True)

    with c2:
        st.markdown("""<div class="spoke"><div class="sh" style="background:#059669">🟢 Production (10.1.0.0/16)</div><div class="sb">
        <strong>Business-critical workloads:</strong><br>
        ☸️ AKS Cluster (private API, 3-8 nodes autoscale)<br>
        🗄️ SQL MI + Cosmos DB (via Private Endpoints)<br>
        🌐 App Services (VNet integrated)<br>
        📊 Power BI Embedded + Redis Cache<br>
        🔐 Key Vault (soft-delete + purge protection)<br><br>
        <span style="color:#059669;font-weight:600;font-size:11px">Deploys here: VMs, AKS, SQL, storage, RBAC, PE configs</span>
        </div></div>""",unsafe_allow_html=True)

    c3,c4=st.columns(2)
    with c3:
        st.markdown("""<div class="spoke"><div class="sh" style="background:#0369A1">🔵 Dev/Test (10.2.0.0/16)</div><div class="sb">
        <strong>Development + testing:</strong><br>
        🧪 Feature branch sandboxes (14-day TTL auto-cleanup)<br>
        🖥️ Dev VMs + test databases<br>
        🔄 UAT environment (pre-prod mirror)<br>
        🤖 AI auto-cleanup (expired resources)<br>
        💰 Budget cap: $10K/mo (auto-shutdown)<br><br>
        <span style="color:#0369A1;font-weight:600;font-size:11px">Most requests auto-approve (Low risk 1-3)</span>
        </div></div>""",unsafe_allow_html=True)

    with c4:
        st.markdown("""<div class="spoke"><div class="sh" style="background:#7C3AED">🟣 Data Platform (10.3.0.0/16)</div><div class="sb">
        <strong>Data + analytics + ML:</strong><br>
        📦 ADLS Gen2 (raw / curated / serve zones)<br>
        ⚡ Synapse Analytics + ADF pipelines<br>
        🔌 Informatica Cloud agent (VNet injected)<br>
        🧠 ML Workspace + GPU VMs (NC6s_v3)<br>
        📊 Databricks + Snowflake connector<br><br>
        <span style="color:#7C3AED;font-weight:600;font-size:11px">Deploys here: Data pipelines, ML infra, ADLS, Synapse</span>
        </div></div>""",unsafe_allow_html=True)

    # Sandbox (smaller)
    st.markdown("""<div style="background:#FFF;border:2px solid #D97706;border-radius:12px;padding:16px 24px;margin-top:12px;display:flex;align-items:center;gap:24px;box-shadow:0 2px 6px rgba(0,0,0,0.06)">
    <div><span style="font-size:14px;font-weight:700;color:#92400E">🟡 Sandbox-POC</span><br><span style="font-size:12px;color:#475569">Experiments, POCs, training. 14-day auto-cleanup. Always auto-approved.</span></div>
    <div style="margin-left:auto;text-align:right"><span style="font-size:11px;color:#D97706;font-weight:600">Budget: $2K/mo cap</span></div>
    </div>""",unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("##### Subscription Resource Inventory")
    inv=pd.DataFrame([
        {"Subscription":"Hub-Connectivity","VNet":"10.0.0.0/16","Resources":47,"Monthly Cost":"$17.2K","Compliance":"100%","Key Services":"Firewall, Bastion, ExpressRoute, APIM"},
        {"Subscription":"Prod-LandingZone","VNet":"10.1.0.0/16","Resources":312,"Monthly Cost":"$56.8K","Compliance":"97%","Key Services":"AKS, SQL MI, Cosmos DB, App Service"},
        {"Subscription":"Dev-Test","VNet":"10.2.0.0/16","Resources":198,"Monthly Cost":"$26.4K","Compliance":"92%","Key Services":"Dev VMs, Test DBs, Sandboxes"},
        {"Subscription":"Data-Platform","VNet":"10.3.0.0/16","Resources":234,"Monthly Cost":"$34.1K","Compliance":"95%","Key Services":"ADLS, Synapse, ADF, ML Workspace"},
        {"Subscription":"Sandbox-POC","VNet":"10.4.0.0/16","Resources":56,"Monthly Cost":"$7.8K","Compliance":"88%","Key Services":"POC resources, experiments"},
    ])
    st.dataframe(inv,use_container_width=True,hide_index=True)

    st.markdown("---")
    st.markdown("##### Recent Deployments by Spoke")
    deps=pd.DataFrame([
        {"Time":"11 Feb 14:22","Request":"REQ-2605","Resource":"SQL+Redis sandbox","Target":"🔵 Dev/Test","Risk":"1.9 Low","Outcome":"✅ Auto-deployed"},
        {"Time":"11 Feb 09:15","Request":"REQ-2604","Resource":"FW rule (Snowflake)","Target":"🔴 Hub","Risk":"4.8 Med","Outcome":"✅ L1 approved"},
        {"Time":"10 Feb 16:30","Request":"REQ-2606","Resource":"Reader (PwC auditor)","Target":"🟢 Production","Risk":"2.1 Low","Outcome":"✅ Auto-deployed"},
        {"Time":"03 Feb 11:45","Request":"REQ-2601","Resource":"AKS cluster (3-node)","Target":"🟢 Production","Risk":"7.4 High","Outcome":"✅ L1+L2+CISO"},
        {"Time":"01 Feb 09:00","Request":"REQ-2598","Resource":"ADLS container (curated)","Target":"🟣 Data Platform","Risk":"3.2 Low","Outcome":"✅ Auto-deployed"},
    ])
    st.dataframe(deps,use_container_width=True,hide_index=True)

# ════════════════════════════════════════════════════════════
# ⑥ BUSINESS OUTCOMES
# ════════════════════════════════════════════════════════════
elif page=="⑥ Business Outcomes":
    st.markdown('<div class="sec" style="color:#059669">⑥ BUSINESS OUTCOMES</div>',unsafe_allow_html=True)
    st.markdown(f"Measurable impact of the CloudOps AI-powered portal across {ORG}'s Azure operations.")

    # 6 outcome cards matching SVG
    outcomes=[
        ("40%","Faster Provisioning","Minutes vs. 3-5 business days","#059669","Before: Engineer files ticket, waits 3-5 days for manual provisioning. After: NL description to AI, IaC generated, risk-scored, auto-approved, deployed in minutes. 74% of requests need zero human approval."),
        ("60%","Less Manual Effort","AI handles scoring, IaC gen, validation","#0369A1","AI features eliminate manual work: #1 generates IaC (no hand-writing Bicep), #7 scores risk (no committee meetings for low-risk), #3 detects drift (no manual audits), #5 scans network posture (no CIS checklist walkthrough)."),
        ("$156K","Annual Cost Savings","FinOps AI: $13K/mo optimizations","#7C3AED","AI #6 FinOps Engine identifies: VM rightsizing ($4.3K/mo), Reserved Instances ($3.6K/mo), orphan cleanup ($2.2K/mo), auto-pause ($1.8K/mo), Spot VMs ($1.1K/mo). Total: $13K/mo = $156K/yr."),
        ("50%","Faster MTTR","Drift detect + auto-remediate","#DC2626","AI #3 scans 847 resources hourly. Detects drift in minutes (was: discovered days/weeks later during audits). Auto-generates fix PRs. Critical drifts (TLS downgrade, public access) remediated in < 1 hour."),
        ("96.2%","Compliance Score","847 resources, CIS benchmarked","#D97706","Continuous compliance monitoring across all 5 subscriptions. Azure Policy in Deny mode prevents non-compliant deployments. AI #5 validates network posture against CIS Azure benchmarks. Auto-remediation for common violations."),
        ("100%","Audit Trail Coverage","Every action, decision, deployment","#0F172A","Immutable audit in Cosmos DB: every request, AI risk score, approval decision, pipeline execution, deployment outcome. Microsoft Sentinel for security correlation. ServiceNow integration for change management."),
    ]
    c1,c2,c3=st.columns(3)
    for idx,(val,title,sub,color,detail) in enumerate(outcomes):
        with [c1,c2,c3][idx%3]:
            st.markdown(f"""<div style="background:#FFF;border:2px solid {color};border-radius:14px;padding:20px;text-align:center;margin:6px 0;box-shadow:0 2px 8px rgba(0,0,0,0.06)">
            <div style="font-size:32px;font-weight:800;color:{color}">{val}</div>
            <div style="font-size:13px;font-weight:700;color:{color};margin:4px 0">{title}</div>
            <div style="font-size:10px;color:#64748B">{sub}</div></div>""",unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("##### Detailed Impact Analysis")
    for val,title,sub,color,detail in outcomes:
        with st.expander(f"**{val} {title}** - {sub}"):
            st.markdown(f"<div style='font-size:13px;color:#475569;line-height:1.7'>{detail}</div>",unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("##### Before vs After Comparison")
    comp=pd.DataFrame([
        {"Metric":"Provisioning Time","Before (Manual)":"3-5 business days","After (AI Portal)":"5-15 minutes (low) / 1-24 hrs (med-high)","Improvement":"40x faster"},
        {"Metric":"Approval Process","Before (Manual)":"Email chains, committee meetings","After (AI Portal)":"AI risk score + Teams adaptive cards","Improvement":"74% auto-approved"},
        {"Metric":"IaC Generation","Before (Manual)":"2-4 hours per template","After (AI Portal)":"AI generates in seconds (NL input)","Improvement":"95% time saved"},
        {"Metric":"Drift Detection","Before (Manual)":"Monthly manual audits","After (AI Portal)":"Hourly AI scans + auto-fix PRs","Improvement":"720x more frequent"},
        {"Metric":"Cost Optimization","Before (Manual)":"Quarterly reviews","After (AI Portal)":"Daily AI analysis + auto-recommendations","Improvement":"$156K/yr savings"},
        {"Metric":"Compliance Checking","Before (Manual)":"Periodic manual assessment","After (AI Portal)":"Continuous + Azure Policy deny mode","Improvement":"96.2% automated"},
        {"Metric":"Access Reviews","Before (Manual)":"Semi-annual review cycles","After (AI Portal)":"Real-time anomaly detection + PIM","Improvement":"Instant alerts"},
    ])
    st.dataframe(comp,use_container_width=True,hide_index=True)

    # Audit trail
    st.markdown("---")
    st.markdown("##### Compliance + Audit Summary")
    c1,c2=st.columns(2)
    with c1:
        cats=["Logging","Data Protection","Network Security","Compute","Identity","Tagging"]
        scores=[100,97,94,95,93,92]
        colors=["#059669" if s>=95 else "#D97706" for s in scores]
        fig=go.Figure(go.Bar(x=scores,y=cats,orientation="h",marker_color=colors,text=[f"{s}%" for s in scores],textposition="outside"))
        fig.update_layout(height=260,margin=dict(l=0,r=50,t=10,b=0),plot_bgcolor="white",xaxis=dict(range=[80,105]),yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig,use_container_width=True)
    with c2:
        st.markdown("**Active Violations:**")
        for ico,desc,sub in [("🔴","2 Storage with public access","Dev/Test + Sandbox"),("🟡","3 VMs missing diagnostics","Sandbox"),("🟡","1 NSG SSH from 0.0.0.0/0","Dev/Test"),("🟢","1 resource missing tags","Data Platform")]:
            bc="#DC2626" if ico=="🔴" else "#D97706" if ico=="🟡" else "#059669"
            st.markdown(f'<div style="padding:8px 12px;margin:4px 0;background:#F8FAFC;border-radius:6px;border-left:3px solid {bc};font-size:12px">{ico} <strong>{sub}:</strong> {desc}</div>',unsafe_allow_html=True)
        st.markdown("**Audit Systems:**")
        for sys,desc in [("Cosmos DB","Requests + AI scores + approvals"),("Log Analytics","Diagnostics + activity logs"),("Microsoft Sentinel","Security correlation + SOAR"),("ServiceNow","Change tickets + CI")]:
            st.markdown(f"- **{sys}:** {desc}")
