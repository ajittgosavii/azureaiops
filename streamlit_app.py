import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import json, random, datetime, time, hashlib

# ============================================================
# PAGE CONFIG + BRANDING
# ============================================================
ORG = "FutureMinds"
DOMAIN = "futureminds.cloud"
TENANT = "futureminds.onmicrosoft.com"
PROJECT = "Meridian-Analytics"

st.set_page_config(
    page_title=f"CloudOps Portal — {ORG}",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# PRODUCTION-GRADE CSS
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
:root{
    --bg:#F8FAFC;--surface:#FFFFFF;--border:#E2E8F0;--text:#0F172A;--text2:#475569;--text3:#94A3B8;
    --blue:#0369A1;--blue-light:#E0F2FE;--blue-dark:#0C4A6E;
    --purple:#7C3AED;--purple-light:#EDE9FE;--purple-dark:#5B21B6;
    --green:#059669;--green-light:#D1FAE5;--green-dark:#065F46;
    --amber:#D97706;--amber-light:#FEF3C7;--amber-dark:#92400E;
    --red:#DC2626;--red-light:#FEE2E2;--red-dark:#991B1B;
    --cyan:#0891B2;--cyan-light:#CFFAFE;
    --radius:10px;--shadow:0 1px 3px rgba(0,0,0,0.06),0 1px 2px rgba(0,0,0,0.04);
    --shadow-md:0 4px 6px -1px rgba(0,0,0,0.07),0 2px 4px -2px rgba(0,0,0,0.05);
}
*{font-family:'DM Sans',system-ui,-apple-system,sans-serif !important}
code,pre,.mono{font-family:'JetBrains Mono',monospace !important}
.main .block-container{padding:1rem 2rem 2rem}
div[data-testid="stSidebar"]{background:#0F172A !important}
div[data-testid="stSidebar"] *{color:#E2E8F0 !important}
div[data-testid="stSidebar"] .stRadio label span{font-size:13px}
div[data-testid="stSidebar"] hr{border-color:#1E293B !important}
#MainMenu,footer,.stDeployButton,div[data-testid="stToolbar"]{display:none !important}

.portal-header{
    background:linear-gradient(135deg,#0C4A6E 0%,#0369A1 50%,#0891B2 100%);
    padding:16px 28px;border-radius:12px;margin-bottom:20px;
    display:flex;justify-content:space-between;align-items:center;
    box-shadow:0 4px 20px rgba(3,105,161,0.25);
    position:relative;overflow:hidden;
}
.portal-header::before{
    content:'';position:absolute;top:-50%;right:-10%;width:300px;height:300px;
    background:radial-gradient(circle,rgba(255,255,255,0.06) 0%,transparent 70%);
}
.portal-header h2{color:#FFF;margin:0;font-size:20px;font-weight:700;letter-spacing:-0.3px}
.portal-header .sub{color:rgba(255,255,255,0.75);margin:0;font-size:11px;letter-spacing:0.3px}
.portal-header .user-info{text-align:right}
.portal-header .user-name{color:#FFF;font-size:13px;font-weight:600}
.portal-header .user-tenant{color:rgba(255,255,255,0.6);font-size:10px}

.kpi{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:16px 20px;text-align:center;box-shadow:var(--shadow);transition:transform 0.15s,box-shadow 0.15s}
.kpi:hover{transform:translateY(-1px);box-shadow:var(--shadow-md)}
.kpi .val{font-size:28px;font-weight:700;color:var(--blue);margin:4px 0;letter-spacing:-0.5px}
.kpi .lbl{font-size:10px;color:var(--text3);text-transform:uppercase;letter-spacing:1px;font-weight:600}
.kpi .delta{font-size:10px;padding:2px 8px;border-radius:10px;display:inline-block;margin-top:4px;font-weight:600}
.kpi .delta.up{background:var(--green-light);color:var(--green-dark)}
.kpi .delta.dn{background:var(--red-light);color:var(--red-dark)}

.badge{padding:3px 10px;border-radius:12px;font-size:10.5px;font-weight:600;display:inline-block;letter-spacing:0.2px}
.bg-green{background:var(--green-light);color:var(--green-dark)}
.bg-amber{background:var(--amber-light);color:var(--amber-dark)}
.bg-red{background:var(--red-light);color:var(--red-dark)}
.bg-blue{background:var(--blue-light);color:var(--blue-dark)}
.bg-purple{background:var(--purple-light);color:var(--purple-dark)}

.ai-pill{
    background:linear-gradient(135deg,var(--purple-light),#F5F3FF);
    border:1px solid #C4B5FD;border-radius:8px;padding:4px 12px;
    font-size:10px;font-weight:700;color:var(--purple-dark);
    display:inline-block;letter-spacing:0.3px;
}

.scenario-card{
    background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);
    padding:20px 24px;margin:8px 0;box-shadow:var(--shadow);
    border-left:4px solid var(--blue);transition:border-color 0.2s;
}
.scenario-card:hover{border-left-color:var(--purple)}
.scenario-card h4{margin:0 0 6px;color:var(--text);font-size:15px;font-weight:700}
.scenario-card .meta{color:var(--text3);font-size:11px;margin-bottom:10px}
.scenario-card .desc{color:var(--text2);font-size:13px;line-height:1.5}

.chat-u{background:var(--blue-light);border-radius:14px 14px 4px 14px;padding:12px 16px;margin:8px 0 8px 60px;font-size:13px;color:var(--text);line-height:1.45}
.chat-a{background:#F0FDF4;border-radius:14px 14px 14px 4px;padding:12px 16px;margin:8px 60px 8px 0;font-size:13px;color:var(--text);border-left:3px solid var(--green);line-height:1.45}

.rec-box{padding:12px 16px;margin:6px 0;border-radius:0 8px 8px 0;font-size:13px;line-height:1.5}
.rec-ok{background:#F0FDF4;border-left:3px solid var(--green);color:var(--text)}
.rec-warn{background:#FFFBEB;border-left:3px solid var(--amber);color:var(--text)}
.rec-crit{background:#FEF2F2;border-left:3px solid var(--red);color:var(--text)}

.risk-tier{border-radius:12px;padding:18px;text-align:center;transition:transform 0.15s}
.risk-tier:hover{transform:translateY(-2px)}
.risk-tier .score{font-size:26px;font-weight:700}
.risk-tier .label{font-size:12px;font-weight:600;margin:4px 0}
.risk-tier .detail{font-size:11px;opacity:0.75;margin-top:6px}

div[data-testid="stExpander"] details{border:1px solid var(--border) !important;border-radius:var(--radius) !important;box-shadow:var(--shadow) !important}
div[data-testid="stExpander"] summary span{font-weight:600 !important;font-size:13px !important}
</style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE — RICH SCENARIO DATA
# ============================================================
if "init" not in st.session_state:
    st.session_state.init = True
    st.session_state.persona = "Cloud Engineer"
    st.session_state.chat_history = []

    # Enterprise request backlog with realistic scenarios
    st.session_state.requests = [
        {"id":"REQ-2601","type":"Provision","desc":"AKS cluster for Meridian analytics microservices (3-node, private API)","status":"Deployed","risk":"High","score":7.4,"date":"2026-02-03","sub":"Production","requestor":"Priya S.","approver":"CISO + Platform Lead"},
        {"id":"REQ-2602","type":"Network","desc":"Private endpoint for Cosmos DB multi-region (East US 2 + West Europe)","status":"Pending","risk":"High","score":8.1,"date":"2026-02-11","sub":"Production","requestor":"Marcus W.","approver":"Network Admin"},
        {"id":"REQ-2603","type":"Access","desc":"Contributor role on rg-meridian-data for ETL service principal","status":"AI Review","risk":"Medium","score":5.3,"date":"2026-02-11","sub":"Data Platform","requestor":"Anika R.","approver":"L1 - Platform"},
        {"id":"REQ-2604","type":"Firewall","desc":"Allow outbound HTTPS to Snowflake partner endpoints (52.x.x.x/24)","status":"Approved","risk":"Medium","score":4.8,"date":"2026-02-09","sub":"Hub","requestor":"Devon L.","approver":"L1 Auto"},
        {"id":"REQ-2605","type":"Provision","desc":"Dev sandbox with SQL + Redis for feature branch testing (14-day TTL)","status":"Approved","risk":"Low","score":1.9,"date":"2026-02-10","sub":"Dev/Test","requestor":"Jordan K.","approver":"Auto-Approved"},
        {"id":"REQ-2606","type":"Access","desc":"Reader role for external auditor (PwC) on compliance resource group","status":"Approved","risk":"Low","score":2.1,"date":"2026-02-08","sub":"Production","requestor":"Compliance Team","approver":"Auto-Approved"},
        {"id":"REQ-2607","type":"Provision","desc":"GPU VM (NC6s_v3) for ML model training — Meridian recommendation engine","status":"Pending","risk":"High","score":8.6,"date":"2026-02-11","sub":"Data Platform","requestor":"Dr. Chen L.","approver":"L1+L2+CTO"},
    ]

    # Approval queue
    st.session_state.approvals = [
        {"id":"APR-101","req":"REQ-2602","type":"Network","desc":"Private endpoint for Cosmos DB multi-region","risk_score":8.1,"risk_level":"High",
         "ai_rec":"Configuration aligns with FutureMinds PE standards. Cosmos DB multi-region requires 2 PEs (one per region) + 2 Private DNS zones. Estimated cost impact: +$73/mo. Requires Network Admin + Security review due to cross-region data replication implications.",
         "factors":{"Environment":"Production (+3)","Resource":"Cosmos DB multi-region (+2)","Network":"Cross-region peering (+2)","Template":"Standard PE template (+0)","Blast Radius":"Multi-region data (+1)"},
         "status":"Awaiting Approval"},
        {"id":"APR-102","req":"REQ-2603","type":"Access","desc":"Contributor role for ETL service principal","risk_score":5.3,"risk_level":"Medium",
         "ai_rec":"Contributor role is overly broad for ETL operations. AI recommends custom role 'Meridian Data Pipeline Operator' with: Microsoft.Sql/*/read, Microsoft.Storage/storageAccounts/blobServices/*/write, Microsoft.DataFactory/factories/pipelines/*/action. Set 90-day auto-expiry with PIM.",
         "factors":{"Environment":"Data Platform (+1)","Permission":"Contributor (broad) (+2)","Scope":"Resource Group (+1)","Identity":"Service Principal (+1)","Pattern":"First-time access (+0)"},
         "status":"Awaiting Approval"},
        {"id":"APR-103","req":"REQ-2607","type":"Provision","desc":"GPU VM for ML model training","risk_score":8.6,"risk_level":"High",
         "ai_rec":"NC6s_v3 GPU is $1,096/mo — significant cost. AI recommends: (1) Use Spot Instance for training workloads ($329/mo, 70% savings), (2) Auto-shutdown at 8PM daily, (3) Managed Identity for model registry access. Requires CTO approval per FutureMinds GPU policy.",
         "factors":{"Environment":"Data Platform (+1)","Cost":"$1,096/mo GPU (+3)","Resource":"Compute-intensive (+2)","Policy":"GPU approval required (+2)","Duration":"Ongoing (+0)"},
         "status":"Awaiting Approval"},
    ]

    # Drift detection scenarios
    st.session_state.drifts = [
        {"res":"nsg-prod-aks-cluster","type":"NSG","sub":"Production","drift":"Inbound rule added manually: Allow TCP 8443 from 0.0.0.0/0 (bypassed IaC pipeline)","sev":"Critical","age":"1h 23m","iac":"modules/network/nsg-aks.bicep",
         "detail":"An engineer added a kubectl debug port directly via Azure Portal, bypassing the GitOps workflow. This exposes the AKS API to the public internet.","fix":"Remove rule, add scoped rule for bastion subnet 10.0.3.0/24 only."},
        {"res":"sql-meridian-prod","type":"SQL Server","sub":"Production","drift":"TLS minimum version downgraded from 1.2 to 1.0 via Portal","sev":"Critical","age":"3h 12m","iac":"modules/data/sql-meridian.bicep",
         "detail":"TLS 1.0 enables known vulnerabilities (BEAST, POODLE). Likely changed to support legacy Informatica connector.","fix":"Revert to TLS 1.2. Update Informatica connector to v10.5+ which supports TLS 1.2."},
        {"res":"kv-futureminds-hub","type":"Key Vault","sub":"Hub","drift":"Soft-delete protection disabled manually","sev":"Critical","age":"6h 45m","iac":"modules/security/kv-hub.bicep",
         "detail":"Key Vault soft-delete is required by FutureMinds security policy and Azure compliance. Disabling allows permanent secret deletion.","fix":"Re-enable soft-delete (90-day retention). Enable purge protection."},
        {"res":"vm-meridian-etl-02","type":"Virtual Machine","sub":"Production","drift":"VM SKU changed from Standard_D4s_v5 to Standard_D8s_v5 via Portal","sev":"Medium","age":"12h","iac":"modules/compute/vm-etl.bicep",
         "detail":"VM was manually upsized during a data load spike. Average CPU since resize: 18%. This is now over-provisioned.","fix":"Update IaC to D4s_v5, add auto-scale rule for spikes instead."},
        {"res":"sta-datalake-raw","type":"Storage","sub":"Data Platform","drift":"Public network access toggled to 'Enabled' from 'Disabled'","sev":"Critical","age":"45m","iac":"modules/data/storage-datalake.bicep",
         "detail":"ADLS Gen2 raw zone exposed to public internet. Contains unmasked PII data from Meridian user analytics.","fix":"Immediate: Disable public access. Verify no data exfiltration via diagnostic logs."},
        {"res":"aks-meridian-prod","type":"AKS","sub":"Production","drift":"Node pool 'userpool' scaled from 3 to 7 nodes manually","sev":"Low","age":"2d","iac":"modules/compute/aks-prod.bicep",
         "detail":"Scaled during Meridian v2.3 launch for traffic spike. Traffic has normalized. 4 excess nodes cost ~$580/mo.","fix":"Update IaC to 3 nodes + configure HPA (Horizontal Pod Autoscaler) for auto-scaling."},
    ]

    # Access anomaly scenarios
    st.session_state.access_anomalies = [
        {"sev":"Critical","identity":"svc-legacy-etl-01 (Service Principal)","type":"Stale","finding":"Owner role on Production subscription — zero API calls in 127 days","detail":"This SPN was created for a legacy ETL pipeline that was decommissioned in Oct 2025. Owner role provides full subscription control.","rec":"Immediate: Revoke all role assignments. If pipeline needs resurrection, create new SPN with scoped custom role.","risk_score":9.4},
        {"sev":"Critical","identity":"ext-contractor-rajesh@partner.com (Guest)","type":"Anomaly","finding":"Sign-in from Vladivostok, Russia at 3:47 AM + 4 failed MFA attempts","detail":"Contractor is based in Bangalore, India. Impossible travel detected (8,400km in 2 hours). Last legitimate sign-in was from India 4 hours prior.","rec":"Immediate: Block sign-in via Conditional Access. Rotate credentials. Trigger security incident review. Notify contractor's manager.","risk_score":9.8},
        {"sev":"High","identity":"svc-jenkins-deploy (Service Principal)","type":"Over-privileged","finding":"Contributor on 4 subscriptions — deployment logs show activity only in Dev/Test","detail":"This CI/CD service principal has write access to Production, Hub, and Data subscriptions but has never deployed outside Dev/Test in 6 months of logs.","rec":"Scope to Dev/Test only. Create separate 'Prod Deployer' SPN with JIT (PIM) activation for production deployments.","risk_score":7.2},
        {"sev":"High","identity":"CloudOps-Platform-Engineers (Entra Group)","type":"Stale","finding":"3 of 8 members inactive for 60+ days — still have Contributor on all subscriptions","detail":"Members: alex.former@futureminds.cloud (left company), test.user@futureminds.cloud (test account), intern.2025@futureminds.cloud (internship ended).","rec":"Remove 3 inactive members. Trigger quarterly access review. Implement automatic deprovisioning via Entra ID lifecycle workflows.","risk_score":6.8},
        {"sev":"Medium","identity":"dr.chen@futureminds.cloud (User)","type":"Anomaly","finding":"PIM activation for Owner role 14 times this week (baseline: 3x/week)","detail":"Dr. Chen is the ML lead working on Meridian recommendation engine. Elevated activity correlates with GPU VM provisioning sprint.","rec":"Likely legitimate but unusual. Recommend: Convert to standing 'ML Platform Contributor' custom role to avoid repeated PIM elevation. Review after sprint.","risk_score":4.6},
        {"sev":"Low","identity":"18 role assignments","type":"Expiring","finding":"PIM assignments expiring in next 14 days across all subscriptions","detail":"Includes 6 Contributor, 8 Reader, 2 Network Contributor, 2 Storage Blob Data Contributor roles. All have PIM time-bound policies.","rec":"Send renewal reminder via Teams 7 days before expiry. Auto-extend Reader roles. Require re-justification for Contributor+ roles.","risk_score":2.1},
    ]

    # Network posture findings
    st.session_state.net_findings = [
        {"sev":"Critical","cis":"CIS 6.2","finding":"NSG nsg-devtest-default allows SSH (22) inbound from 0.0.0.0/0","sub":"Dev/Test","impact":"Any internet IP can attempt SSH connections to VMs in Dev/Test. Brute-force attacks detected (847 attempts in last 24h).",
         "rec":"Restrict source to AzureBastionSubnet (10.0.3.0/24). Block all other inbound SSH. Enable JIT VM Access via Defender for Cloud.","remediation_code":"az network nsg rule update -g rg-devtest --nsg-name nsg-devtest-default -n AllowSSH --source-address-prefixes 10.0.3.0/24 --priority 100"},
        {"sev":"Critical","cis":"CIS 3.7","finding":"Storage sta-sandbox-analytics has publicNetworkAccess=Enabled","sub":"Sandbox","impact":"Storage account accessible from any internet IP. Contains sample datasets that may include derivative PII data.",
         "rec":"Set publicNetworkAccess=Disabled. Add Private Endpoint in sandbox VNet. Update applications to use PE connection string.","remediation_code":"az storage account update -n stasandboxanalytics -g rg-sandbox --public-network-access Disabled"},
        {"sev":"High","cis":"CIS 6.5","finding":"Azure Firewall allows outbound 0.0.0.0/0:443 from Sandbox spoke","sub":"Hub","impact":"Sandbox workloads can reach any HTTPS endpoint on the internet, enabling potential data exfiltration.",
         "rec":"Replace wildcard with specific FQDN tags: AzureCloud, AzureContainerRegistry, MicrosoftContainerRegistry. Add application rules for approved SaaS (Snowflake, Databricks).","remediation_code":"az network firewall policy rule-collection-group ... --target-fqdns '*.snowflakecomputing.com' '*.azuredatabricks.net'"},
        {"sev":"Medium","cis":"CIS 6.4","finding":"3 NSGs have no flow logs enabled (nsg-sandbox-*, nsg-data-temp, nsg-dev-isolated)","sub":"Multiple","impact":"No network traffic visibility for troubleshooting or security forensics in these subnets.",
         "rec":"Enable NSG flow logs v2 → Log Analytics workspace. Retention: 90 days. Enable Traffic Analytics for visualization.","remediation_code":"az network watcher flow-log create --nsg <nsg-id> --workspace <law-id> --enabled true --format JSON --log-version 2"},
        {"sev":"Medium","cis":"CIS 6.1","finding":"Data Platform spoke VNet missing UDR force-tunnel to Hub Azure Firewall","sub":"Data Platform","impact":"Data Platform resources can route directly to internet bypassing firewall inspection. Informatica Cloud traffic not inspected.",
         "rec":"Create UDR with 0.0.0.0/0 → Azure Firewall private IP (10.0.1.4). Associate with all subnets in Data Platform VNet.","remediation_code":"az network route-table route create -g rg-data --route-table-name rt-data-default -n force-tunnel --address-prefix 0.0.0.0/0 --next-hop-type VirtualAppliance --next-hop-ip-address 10.0.1.4"},
    ]

    # FinOps scenarios
    st.session_state.finops_recs = [
        {"save":"$4,280/mo","action":"Rightsize 8 VMs in Dev/Test — avg CPU 11%, avg memory 23%","detail":"VMs: vm-dev-api-01 through vm-dev-api-04 (D4s→D2s), vm-test-worker-01/02 (D8s→D4s), vm-sandbox-ml-01/02 (NC6→NC4). Based on 30-day P95 metrics.","conf":"High","cat":"Rightsizing","risk":"Low"},
        {"save":"$3,640/mo","action":"Convert 5 Production VMs to 1-year Reserved Instances","detail":"Stable workloads running 24/7 for 6+ months: vm-meridian-api-01/02/03, vm-etl-prod-01, vm-monitor-01. RI vs Pay-as-you-go saves 38%.","conf":"High","cat":"Reserved Instance","risk":"Low"},
        {"save":"$2,190/mo","action":"Delete 6 orphaned managed disks + 2 unattached public IPs in Sandbox","detail":"Disks: disk-sandbox-test-* (created by deleted VMs, unattached 45+ days). Public IPs: pip-sandbox-temp-01/02 (no associated NIC).","conf":"High","cat":"Orphan Cleanup","risk":"None"},
        {"save":"$1,840/mo","action":"Enable auto-pause on Synapse Dedicated SQL Pool (off-hours 8PM-6AM + weekends)","detail":"Current: runs 24/7 ($5,520/mo). Actual query activity: 6AM-8PM weekdays only. Auto-pause saves 10hr/day + 48hr/weekend = 67% idle time.","conf":"High","cat":"Scheduling","risk":"Low"},
        {"save":"$1,096/mo","action":"Switch GPU VM (NC6s_v3) to Spot Instance for ML training workloads","detail":"Dr. Chen's ML training jobs are fault-tolerant (checkpoint every 30 min). Spot pricing: $329/mo vs $1,096/mo on-demand. Add checkpointing + auto-restart.","conf":"Medium","cat":"Spot Instance","risk":"Medium"},
    ]

# ============================================================
# HELPER FUNCTIONS
# ============================================================
def kpi_card(label, value, delta=None, direction="up"):
    d = f'<div class="delta {direction}">{delta}</div>' if delta else ""
    return f'<div class="kpi"><div class="lbl">{label}</div><div class="val">{value}</div>{d}</div>'

def badge(status):
    style_map = {
        "Approved":"bg-green","Deployed":"bg-green","Pass":"bg-green","Clean":"bg-green","Low":"bg-green","OK":"bg-green","Resolved":"bg-green",
        "Pending":"bg-amber","Awaiting Approval":"bg-amber","Medium":"bg-amber","Warning":"bg-amber","Open":"bg-amber","Expiring":"bg-amber",
        "Rejected":"bg-red","Critical":"bg-red","High":"bg-red","Drift":"bg-red","Stale":"bg-red","Over-privileged":"bg-red","Anomaly":"bg-red","Blocked":"bg-red",
        "AI Review":"bg-purple","Auto-Approved":"bg-blue",
    }
    return f'<span class="badge {style_map.get(status, "bg-blue")}">{status}</span>'

def ai_pill(n):
    return f'<span class="ai-pill">🧠 AI Feature #{n}</span>'

def rec_box(text, level="ok"):
    cls = {"ok":"rec-ok","warn":"rec-warn","crit":"rec-crit"}.get(level,"rec-ok")
    return f'<div class="rec-box {cls}">{text}</div>'

def severity_icon(sev):
    return {"Critical":"🔴","High":"🟠","Medium":"🟡","Low":"🟢","Info":"🔵"}.get(sev,"⚪")

def call_claude(prompt, system_prompt="You are an Azure CloudOps AI assistant for FutureMinds. Give concise, technical responses with Azure CLI or Bicep code where relevant. Keep under 300 words."):
    try:
        import anthropic
        key = st.secrets.get("ANTHROPIC_API_KEY", None)
        if not key:
            return None
        client = anthropic.Anthropic(api_key=key)
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=system_prompt,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception:
        return None

# IaC Templates (fallback when no API key)
IAC_TEMPLATES = {
    "Virtual Machine": '''// Bicep — Virtual Machine with Private Endpoint + Diagnostics
// Auto-generated by CloudOps AI Feature #1 | {ORG}
// ─────────────────────────────────────────────────────────

@description('VM for {PROJECT} workload')
param location string = resourceGroup().location
param vmName string = '{name}'
param vmSize string = '{size}'
param subnetId string
param logAnalyticsId string

// Tags — FutureMinds mandatory tagging policy
var tags = {{
  environment: '{env}'
  costCenter: '{cc}'
  project: '{PROJECT}'
  managedBy: 'CloudOps-Portal-AI'
  createdDate: utcNow('yyyy-MM-dd')
}}

resource nic 'Microsoft.Network/networkInterfaces@2024-01-01' = {{
  name: '${{vmName}}-nic'
  location: location
  tags: tags
  properties: {{
    ipConfigurations: [{{
      name: 'ipconfig1'
      properties: {{
        subnet: {{ id: subnetId }}
        privateIPAllocationMethod: 'Dynamic'
      }}
    }}]
  }}
}}

resource vm 'Microsoft.Compute/virtualMachines@2024-03-01' = {{
  name: vmName
  location: location
  tags: tags
  identity: {{ type: 'SystemAssigned' }}  // Managed Identity — zero secrets
  properties: {{
    hardwareProfile: {{ vmSize: vmSize }}
    osProfile: {{
      computerName: vmName
      adminUsername: 'fmadmin'
      linuxConfiguration: {{
        disablePasswordAuthentication: true
        ssh: {{ publicKeys: [{{ path: '/home/fmadmin/.ssh/authorized_keys'; keyData: '<ssh-public-key>' }}] }}
      }}
    }}
    networkProfile: {{ networkInterfaces: [{{ id: nic.id }}] }}
    securityProfile: {{ securityType: 'TrustedLaunch' }}
    diagnosticsProfile: {{ bootDiagnostics: {{ enabled: true }} }}
  }}
}}

// Diagnostic settings → Central Log Analytics
resource diag 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {{
  name: '${{vmName}}-diag'
  scope: vm
  properties: {{
    workspaceId: logAnalyticsId
    metrics: [{{ category: 'AllMetrics'; enabled: true; retentionPolicy: {{ enabled: true; days: 90 }} }}]
  }}
}}

output vmId string = vm.id
output vmPrincipalId string = vm.identity.principalId
''',
    "Azure SQL Database": '''// Bicep — Azure SQL + Private Endpoint + DNS Zone
// Auto-generated by CloudOps AI Feature #1 | {ORG}
// ─────────────────────────────────────────────────────────

param location string = resourceGroup().location
param sqlServerName string = '{name}'
param subnetId string
param logAnalyticsId string

var tags = {{
  environment: '{env}'
  costCenter: '{cc}'
  project: '{PROJECT}'
  managedBy: 'CloudOps-Portal-AI'
}}

resource sqlServer 'Microsoft.Sql/servers@2023-08-01-preview' = {{
  name: sqlServerName
  location: location
  tags: tags
  properties: {{
    administratorLogin: 'fmsqladmin'
    minimalTlsVersion: '1.2'
    publicNetworkAccess: 'Disabled'  // PE only
  }}
}}

resource sqlDb 'Microsoft.Sql/servers/databases@2023-08-01-preview' = {{
  parent: sqlServer
  name: 'MeridianDW'
  location: location
  sku: {{ name: '{size}'; tier: 'GeneralPurpose'; family: 'Gen5'; capacity: 4 }}
  properties: {{
    collation: 'SQL_Latin1_General_CP1_CI_AS'
    zoneRedundant: true
  }}
}}

resource pe 'Microsoft.Network/privateEndpoints@2024-01-01' = {{
  name: '${{sqlServerName}}-pe'
  location: location
  tags: tags
  properties: {{
    subnet: {{ id: subnetId }}
    privateLinkServiceConnections: [{{
      name: '${{sqlServerName}}-plsc'
      properties: {{
        privateLinkServiceId: sqlServer.id
        groupIds: ['sqlServer']
      }}
    }}]
  }}
}}

resource dnsZone 'Microsoft.Network/privateDnsZones@2020-06-01' existing = {{
  name: 'privatelink.database.windows.net'
}}

resource dnsRecord 'Microsoft.Network/privateDnsZones/A@2020-06-01' = {{
  parent: dnsZone
  name: sqlServerName
  properties: {{
    aRecords: [{{ ipv4Address: pe.properties.customDnsConfigs[0].ipAddresses[0] }}]
    ttl: 300
  }}
}}
''',
    "Storage Account": '''// Bicep — ADLS Gen2 with Private Endpoint
// Auto-generated by CloudOps AI Feature #1 | {ORG}
// ─────────────────────────────────────────────────────────

param location string = resourceGroup().location
param storageAccountName string = '{name}'
param subnetId string

var tags = {{
  environment: '{env}'
  costCenter: '{cc}'
  project: '{PROJECT}'
  managedBy: 'CloudOps-Portal-AI'
}}

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' = {{
  name: storageAccountName
  location: location
  kind: 'StorageV2'
  sku: {{ name: '{size}' }}
  tags: tags
  properties: {{
    isHnsEnabled: true            // ADLS Gen2
    publicNetworkAccess: 'Disabled'
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
    supportsHttpsTrafficOnly: true
    networkAcls: {{ defaultAction: 'Deny'; bypass: 'AzureServices' }}
    encryption: {{ services: {{ blob: {{ enabled: true }}; file: {{ enabled: true }} }}; keySource: 'Microsoft.Storage' }}
  }}
}}

resource pe 'Microsoft.Network/privateEndpoints@2024-01-01' = {{
  name: '${{storageAccountName}}-blob-pe'
  location: location
  tags: tags
  properties: {{
    subnet: {{ id: subnetId }}
    privateLinkServiceConnections: [{{
      name: 'blob-plsc'
      properties: {{ privateLinkServiceId: storageAccount.id; groupIds: ['blob'] }}
    }}]
  }}
}}
''',
}

def generate_iac(resource_type, config):
    prompt = f"""Generate production-ready Azure Bicep for: {resource_type}
Config: {json.dumps(config)}
Organization: FutureMinds | Project: Meridian-Analytics
Requirements: Private Endpoint, diagnostic settings to Log Analytics, FutureMinds mandatory tags (environment, costCenter, project, managedBy). Return ONLY Bicep code with comments."""
    result = call_claude(prompt, "You are an Azure IaC expert at FutureMinds. Generate production Bicep templates. Always include: Private Endpoints, diagnostics, mandatory tags, Managed Identity. Code only with comments.")
    if result:
        return result
    template = IAC_TEMPLATES.get(resource_type, f"// Template for {resource_type} — extend as needed\nparam location string = resourceGroup().location")
    return template.format(name=config.get("name","res-001"), size=config.get("size","Standard_D2s_v3"),
                           env=config.get("env","dev"), cc=config.get("cc","IT-Platform"),
                           ORG=ORG, PROJECT=PROJECT)

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown(f"""<div style="text-align:center;padding:16px 12px 12px;margin:-1rem -1rem 12px;background:linear-gradient(180deg,#1E293B,#0F172A);border-bottom:1px solid #334155">
    <div style="font-size:32px;margin-bottom:4px">☁️</div>
    <div style="font-size:15px;font-weight:700;color:#E0F2FE;letter-spacing:-0.3px">CloudOps Portal</div>
    <div style="font-size:10px;color:#64748B;letter-spacing:0.5px;margin-top:2px">{ORG.upper()} · AZURE MULTI-SUBSCRIPTION</div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""<div style="background:#1E293B;border:1px solid #334155;border-radius:8px;padding:10px 14px;margin-bottom:16px">
    <div style="font-size:11px;color:#94A3B8;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px">Signed in as</div>
    <div style="font-size:14px;font-weight:600;color:#F1F5F9">{st.session_state.persona}</div>
    <div style="font-size:10px;color:#64748B;margin-top:2px">{TENANT}</div>
    </div>""", unsafe_allow_html=True)

    st.session_state.persona = st.selectbox("Switch Persona", ["Cloud Engineer","Network Admin","Security Admin","FinOps Analyst","DevOps Engineer","App Owner","Platform Lead"], label_visibility="collapsed")

    page = st.radio("", [
        "📊 Dashboard",
        "🏗️ AI #1 · NL → IaC Generator",
        "🤖 AI #2 · Ops Chatbot",
        "🔄 AI #3 · Drift Detector",
        "🔐 AI #4 · Access Anomaly",
        "🛡️ AI #5 · Network Posture",
        "💰 AI #6 · FinOps AI",
        "⚡ AI #7 · Risk Scorer",
        "📋 Compliance & Audit",
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown(f"""<div style="font-size:10px;color:#64748B;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;font-weight:600">Subscriptions</div>""", unsafe_allow_html=True)
    subs_health = [("Hub-Connectivity","Healthy","🟢"),("Prod-LandingZone","Healthy","🟢"),("Dev-Test","Healthy","🟢"),("Data-Platform","1 Advisory","🟡"),("Sandbox-POC","Healthy","🟢")]
    for name, status, icon in subs_health:
        st.markdown(f"""<div style="display:flex;align-items:center;gap:6px;margin:4px 0;font-size:12px"><span>{icon}</span><span style="color:#E2E8F0;font-weight:500">{name}</span><span style="color:#64748B;font-size:10px;margin-left:auto">{status}</span></div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"""<div style="font-size:9px;color:#475569;text-align:center;padding:8px 0">
    CloudOps v3.0 · AI Engine: Claude (Anthropic)<br>
    © 2026 {ORG} · All rights reserved
    </div>""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================
st.markdown(f"""<div class="portal-header">
<div><h2>☁️ CloudOps Unified Portal</h2><p class="sub">Azure Multi-Subscription Management · 7 Gen AI Features · {ORG}</p></div>
<div class="user-info"><div class="user-name">{st.session_state.persona}</div><div class="user-tenant">{TENANT}</div></div>
</div>""", unsafe_allow_html=True)

# ============================================================
# 📊 DASHBOARD
# ============================================================
if page == "📊 Dashboard":
    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: st.markdown(kpi_card("Subscriptions","5","All Healthy"), unsafe_allow_html=True)
    with c2: st.markdown(kpi_card("Resources","847","↑ 23 this week"), unsafe_allow_html=True)
    with c3: st.markdown(kpi_card("Pending Approvals","3","Action required","dn"), unsafe_allow_html=True)
    with c4: st.markdown(kpi_card("Monthly Spend","$142.3K","↓ 8% vs forecast"), unsafe_allow_html=True)
    with c5: st.markdown(kpi_card("Compliance","96.2%","↑ 1.4% MoM"), unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### Cost Trend by Subscription (6 Mo)")
        np.random.seed(42)
        dates = pd.date_range("2025-09-01", periods=6, freq="MS")
        fig = go.Figure()
        for sub, color, base in [("Production","#0369A1",56),("Data Platform","#7C3AED",34),("Dev/Test","#0891B2",26),("Hub","#DC2626",17),("Sandbox","#D97706",9)]:
            vals = [base + np.random.uniform(-4, 6) for _ in dates]
            fig.add_trace(go.Scatter(x=dates, y=vals, name=sub, mode="lines+markers", line=dict(color=color, width=2.5), marker=dict(size=6)))
        fig.update_layout(height=300, margin=dict(l=0,r=0,t=10,b=0), legend=dict(orientation="h",y=-0.18,font=dict(size=10)), yaxis_title="Cost ($K)", plot_bgcolor="white", yaxis=dict(gridcolor="#F1F5F9"), xaxis=dict(gridcolor="#F1F5F9"))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("##### 7 AI Features — Invocations (30 days)")
        feats = ["#7 Risk Score","#2 Chatbot","#4 Access AI","#3 Drift Detect","#6 FinOps AI","#1 NL→IaC","#5 Net Posture"]
        counts = [523,312,156,89,67,47,34]
        colors = ["#4C1D95","#5B21B6","#6D28D9","#7C3AED","#8B5CF6","#A78BFA","#C4B5FD"]
        fig2 = go.Figure(go.Bar(x=counts, y=feats, orientation="h", marker_color=colors, text=counts, textposition="outside", textfont=dict(size=11,color="#334155")))
        fig2.update_layout(height=300, margin=dict(l=0,r=50,t=10,b=0), plot_bgcolor="white", xaxis=dict(gridcolor="#F1F5F9"), yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("##### Recent Requests")
    for r in st.session_state.requests:
        cols = st.columns([1.2, 1.5, 5, 1.5, 1.5, 1.5])
        cols[0].markdown(f"**{r['id']}**")
        cols[1].markdown(f"`{r['type']}`")
        cols[2].markdown(r['desc'])
        cols[3].markdown(f"📁 {r['sub']}")
        cols[4].markdown(badge(r['status']), unsafe_allow_html=True)
        cols[5].markdown(f"<span style='color:#94A3B8;font-size:12px'>{r['date']}</span>", unsafe_allow_html=True)

# ============================================================
# AI #1: NL → IaC GENERATOR
# ============================================================
elif page == "🏗️ AI #1 · NL → IaC Generator":
    st.markdown(f"### 🏗️ AI Feature #1 — Natural Language → Infrastructure-as-Code")
    st.markdown(f"""{ai_pill(1)} Describe infrastructure in plain English → AI generates production-ready Bicep/Terraform with Private Endpoints, diagnostics, {ORG} mandatory tags, and Managed Identity.""", unsafe_allow_html=True)
    st.markdown("---")

    tab1, tab2 = st.tabs(["📝 Guided Form", "🧠 Natural Language"])

    with tab1:
        st.markdown("**Scenario: Provision resources for the Meridian Analytics platform**")
        with st.form("provision_form", border=True):
            c1, c2 = st.columns(2)
            with c1:
                res_type = st.selectbox("Resource Type", ["Virtual Machine","Azure SQL Database","Storage Account","AKS Cluster","App Service","Function App","Cosmos DB","Redis Cache"])
                target_sub = st.selectbox("Target Subscription", ["Prod-LandingZone","Dev-Test","Data-Platform","Sandbox-POC"])
                res_name = st.text_input("Resource Name", placeholder="e.g., vm-meridian-api-03")
                environment = st.selectbox("Environment", ["Production","Development","Test","Sandbox"])
            with c2:
                sku_map = {"Virtual Machine":["Standard_D2s_v5","Standard_D4s_v5","Standard_D8s_v5","Standard_NC6s_v3 (GPU)"],
                           "Azure SQL Database":["GP_Gen5_2","GP_Gen5_4","GP_Gen5_8","BC_Gen5_4"],
                           "Storage Account":["Standard_LRS","Standard_GRS","Premium_LRS"],
                           "AKS Cluster":["Standard_D4s_v5 (per node)","Standard_D8s_v5 (per node)"],
                           "Cosmos DB":["Serverless","400 RU/s","4000 RU/s"]}
                sku = st.selectbox("SKU / Size", sku_map.get(res_type, ["Standard"]))
                region = st.selectbox("Region", ["East US 2 (Primary)","West Europe (DR)","Central US"])
                cost_center = st.text_input("Cost Center", value="IT-Platform")
                justification = st.text_area("Business Justification", placeholder="e.g., Required for Meridian v2.4 analytics pipeline — data ingestion service needs dedicated compute...", height=80)

            submitted = st.form_submit_button("🚀 Generate IaC + Submit Request", type="primary", use_container_width=True)

            if submitted and res_name:
                config = {"name": res_name, "size": sku.split(" ")[0], "env": environment.lower(), "cc": cost_center}
                with st.spinner("🧠 AI generating IaC template and running policy pre-flight..."):
                    time.sleep(1.5)

                req_id = f"REQ-{random.randint(2700,2999)}"
                risk = "Low" if environment in ["Development","Sandbox"] else "Medium" if environment == "Test" else "High"
                score = round(random.uniform(1.5,3.5) if risk=="Low" else random.uniform(4,6.5) if risk=="Medium" else random.uniform(7,9),1)

                st.success(f"✅ Request **{req_id}** submitted successfully!")

                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("**🛡️ AI Policy Pre-flight Results:**")
                    checks = [
                        ("Region allowed (East US 2 / West Europe)", "✅ Pass"),
                        ("SKU in approved catalog", "✅ Pass"),
                        (f"Naming convention ({ORG} kebab-case)", "✅ Pass" if "-" in res_name else "⚠️ Use kebab-case: vm-meridian-xxx"),
                        ("Mandatory tags (env, costCenter, project)", "✅ Pass"),
                        ("Private Endpoint auto-configured", "✅ Auto-attached"),
                        ("Diagnostics → Log Analytics", "✅ Auto-configured"),
                        ("Managed Identity", "✅ SystemAssigned enabled"),
                    ]
                    for check, result in checks:
                        st.markdown(f"&nbsp;&nbsp;{result} — {check}")

                with col_b:
                    st.markdown("**⚡ AI Risk Assessment:**")
                    st.markdown(f"Risk Score: **{score}/10** → {badge(risk)}", unsafe_allow_html=True)
                    if risk == "Low":
                        st.markdown(rec_box("✅ <strong>Auto-Approved</strong> — Dev/Sandbox + standard template. Pipeline triggered automatically.", "ok"), unsafe_allow_html=True)
                    elif risk == "Medium":
                        st.markdown(rec_box(f"⏳ <strong>L1 Approval Required</strong> — Routed to Platform Lead via Teams adaptive card. SLA: 4 hours.", "warn"), unsafe_allow_html=True)
                    else:
                        st.markdown(rec_box(f"🔒 <strong>Multi-Level Review</strong> — Routed to L1 + L2 + CISO. SLA: 24 hours.", "crit"), unsafe_allow_html=True)

                st.markdown("---")
                st.markdown("**📄 AI-Generated Bicep Template:**")
                st.code(generate_iac(res_type, config), language="bicep")

    with tab2:
        st.markdown("**Describe your infrastructure need in plain English:**")
        nl_input = st.text_area(
            "Natural language prompt",
            placeholder="Example: I need a 3-node AKS cluster in production with private API server, Azure CNI networking, connected to the Meridian SQL database via private endpoint. It should have a system node pool (D4s_v5) and a user pool with autoscale 2-8 nodes. Include monitoring with Container Insights and set up HPA for the API deployment.",
            height=140, label_visibility="collapsed"
        )
        if st.button("🧠 Generate Infrastructure from Description", type="primary", use_container_width=True) and nl_input:
            with st.spinner("AI analyzing requirements, generating resource plan and IaC..."):
                result = call_claude(
                    f"User request: {nl_input}\n\nOrganization: {ORG}, Project: {PROJECT}. Generate: 1) Resource list with estimated monthly cost 2) Risk assessment 3) Full Bicep template. Always include PE, diagnostics, mandatory tags.",
                    f"You are an Azure IaC expert at {ORG}. Parse natural language into production Bicep. Include PE, diagnostics, Managed Identity, mandatory tags. Format: ## Resources, ## Cost Estimate, ## Risk Assessment, ## Bicep Template"
                )
                if result:
                    st.markdown(result)
                else:
                    st.markdown("""**🤖 AI-Generated Resource Plan:**

**Resources Identified:**
| # | Resource | SKU | Est. Cost |
|---|----------|-----|-----------|
| 1 | AKS Cluster (3 system + autoscale user) | D4s_v5 | $876/mo |
| 2 | Private Endpoint (AKS API) | — | $7.30/mo |
| 3 | Container Insights (Log Analytics) | Per-GB | ~$120/mo |
| 4 | Azure CNI networking | — | Included |

**Total Estimate:** ~$1,003/mo

**Risk Assessment:** Score 7.8/10 (High) — Production AKS with custom networking requires L1+L2 approval.""")
                    st.code(generate_iac("Virtual Machine", {"name":"aks-meridian-prod","size":"Standard_D4s_v5","env":"production","cc":"IT-Platform"}), language="bicep")

# ============================================================
# AI #2: OPS CHATBOT / COPILOT
# ============================================================
elif page == "🤖 AI #2 · Ops Chatbot":
    st.markdown("### 🤖 AI Feature #2 — CloudOps Copilot")
    st.markdown(f"""{ai_pill(2)} Ask anything about your Azure environment in natural language. The AI has full context on {ORG}'s subscriptions, policies, cost data, compliance status, and operational history.""", unsafe_allow_html=True)
    st.markdown("---")

    # Chat history display
    for msg in st.session_state.chat_history:
        cls = "chat-u" if msg["role"] == "user" else "chat-a"
        icon = "👤" if msg["role"] == "user" else "🤖"
        st.markdown(f'<div class="{cls}">{icon} &nbsp;{msg["content"]}</div>', unsafe_allow_html=True)

    # Quick action buttons
    st.markdown("**Quick Actions:**")
    quick_prompts = [
        "Show all untagged resources across subscriptions",
        "Which VMs are over-provisioned in Dev/Test?",
        "Generate Bicep for a new Cosmos DB with geo-replication",
        "What PIM roles are expiring this week?",
    ]
    qcols = st.columns(4)
    for i, qp in enumerate(quick_prompts):
        if qcols[i].button(qp, key=f"quick_{i}", use_container_width=True):
            st.session_state.chat_history.append({"role":"user","content":qp})
            st.rerun()

    # Chat input
    user_msg = st.chat_input(f"Ask the {ORG} CloudOps AI Copilot...")
    if user_msg:
        st.session_state.chat_history.append({"role":"user","content":user_msg})
        context = f"""CloudOps AI Copilot for {ORG}.
Environment: 5 Azure subscriptions (Hub 10.0.0.0/16, Prod 10.1.0.0/16, Dev 10.2.0.0/16, Data 10.3.0.0/16, Sandbox).
847 total resources. $142K/mo spend. 96.2% compliance score.
Key project: Meridian Analytics (data pipeline: source systems → ADLS → Synapse → Power BI).
Tech: Azure Firewall in hub, all PaaS via Private Endpoints, AKS for microservices, Managed Identity everywhere.
Current persona: {st.session_state.persona}. Be concise, actionable. Include Azure CLI or Bicep when useful."""

        with st.spinner("🧠 Thinking..."):
            ai_response = call_claude(user_msg, context)
            if not ai_response:
                fallbacks = {
                    "untag": f"""**Untagged Resources Across {ORG} Subscriptions:**

| Resource | Type | Resource Group | Subscription |
|----------|------|---------------|--------------|
| vm-test-scratch-03 | Virtual Machine | rg-sandbox-temp | Sandbox |
| disk-orphan-data-01 | Managed Disk | rg-devtest | Dev/Test |
| pip-unused-02 | Public IP | rg-sandbox-temp | Sandbox |

**Fix:** `az tag create --resource-id <id> --tags costCenter=IT-Platform environment=dev project=Meridian-Analytics managedBy=CloudOps-Portal`

**Recommendation:** Enable Azure Policy `Require tag and its value` in Deny mode on all subscriptions.""",
                    "over": """**Over-Provisioned VMs in Dev/Test (30-day P95 metrics):**

| VM | Current SKU | CPU P95 | Memory P95 | Recommended | Savings |
|----|-------------|---------|------------|-------------|---------|
| vm-dev-api-01 | D4s_v5 | 8% | 22% | D2s_v5 | $73/mo |
| vm-dev-api-02 | D4s_v5 | 12% | 19% | D2s_v5 | $73/mo |
| vm-test-worker-01 | D8s_v5 | 6% | 15% | D4s_v5 | $146/mo |
| vm-sandbox-ml-01 | NC6s_v3 | 3% | 8% | NC4as (Spot) | $767/mo |

**Total potential savings: $1,059/mo**""",
                    "pim": """**PIM Roles Expiring This Week:**

| User | Role | Scope | Expires | Action |
|------|------|-------|---------|--------|
| priya.s@futureminds.cloud | Contributor | Prod sub | Feb 14 | Renewal needed |
| devon.l@futureminds.cloud | Network Contributor | Hub sub | Feb 13 | Renewal needed |
| ext-auditor@pwc.com | Reader | rg-compliance | Feb 12 | Let expire |

Sent Teams reminders automatically. Use: `az role assignment list --scope /subscriptions/<id> --query "[?expires_on < '2026-02-18']"`""",
                    "cosmos": """```bicep
resource cosmos 'Microsoft.DocumentDB/databaseAccounts@2024-02-15-preview' = {
  name: 'cosmos-meridian-prod'
  location: 'East US 2'
  tags: { environment: 'production'; costCenter: 'IT-Platform'; project: 'Meridian-Analytics' }
  properties: {
    databaseAccountOfferType: 'Standard'
    locations: [
      { locationName: 'East US 2'; failoverPriority: 0 }
      { locationName: 'West Europe'; failoverPriority: 1 }
    ]
    consistencyPolicy: { defaultConsistencyLevel: 'Session' }
    publicNetworkAccess: 'Disabled'
    enableMultipleWriteLocations: false
  }
}
```""",
                }
                msg_lower = user_msg.lower()
                ai_response = next((v for k,v in fallbacks.items() if k in msg_lower), f"I can help with that! Ask me about provisioning, networking, access management, cost optimization, compliance, or any Azure operational question. 💡 Add `ANTHROPIC_API_KEY` in Streamlit secrets for full AI-powered responses.")
            st.session_state.chat_history.append({"role":"assistant","content":ai_response})
        st.rerun()

    if st.button("🗑️ Clear conversation"):
        st.session_state.chat_history = []
        st.rerun()

# ============================================================
# AI #3: RESOURCE DRIFT DETECTOR
# ============================================================
elif page == "🔄 AI #3 · Drift Detector":
    st.markdown("### 🔄 AI Feature #3 — Resource Drift Detector")
    st.markdown(f"""{ai_pill(3)} Continuously compares ARM live state against IaC Git repository. Detects unauthorized manual changes, generates auto-fix pull requests, and maintains infrastructure parity across all {ORG} subscriptions.""", unsafe_allow_html=True)
    st.markdown("---")

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(kpi_card("Resources Scanned","847","Hourly cycle"), unsafe_allow_html=True)
    with c2: st.markdown(kpi_card("Drifted Resources","6","↓ 3 from last week"), unsafe_allow_html=True)
    with c3: st.markdown(kpi_card("Auto-Fixed (PRs)","14","This month"), unsafe_allow_html=True)
    with c4: st.markdown(kpi_card("Pending Review","3","Needs human decision","dn"), unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"**🔍 Drift Detection Results** — Last scan: {(datetime.datetime.now()-datetime.timedelta(minutes=random.randint(1,8))).strftime('%H:%M')} UTC")

    for d in st.session_state.drifts:
        icon = severity_icon(d["sev"])
        with st.expander(f"{icon} **{d['res']}** ({d['type']}) — {d['drift'][:70]}... [{d['age']} ago]", expanded=(d["sev"]=="Critical")):
            col1, col2 = st.columns([3,2])
            with col1:
                st.markdown(f"**Subscription:** {d['sub']} &nbsp;|&nbsp; **Severity:** {badge(d['sev'])} &nbsp;|&nbsp; **IaC Source:** `{d['iac']}`", unsafe_allow_html=True)
                st.markdown(f"**Details:** {d['detail']}")
            with col2:
                level = "crit" if d["sev"]=="Critical" else "warn" if d["sev"] in ["High","Medium"] else "ok"
                st.markdown(rec_box(f"🤖 <strong>AI Recommendation:</strong> {d['fix']}", level), unsafe_allow_html=True)

            col_a, col_b, col_c = st.columns(3)
            if col_a.button("🔄 Auto-Fix (Revert to IaC)", key=f"fix_{d['res']}", use_container_width=True):
                st.success(f"✅ PR #{random.randint(200,400)} created → CI pipeline validating → auto-merge on pass")
            if col_b.button("✅ Accept Drift (Update IaC)", key=f"accept_{d['res']}", use_container_width=True):
                st.info("IaC template updated to match live state. PR created for review.")
            if col_c.button("📋 View Full Diff", key=f"diff_{d['res']}", use_container_width=True):
                st.code(f"""--- a/{d['iac']}   (IaC repository)
+++ b/ARM live state   (Azure Resource Manager)

  resource {d['res'].split('-')[0]} ... {{
-   // Original IaC-defined configuration
+   // DRIFT DETECTED: {d['drift']}
+   // Changed by: Portal user (manual) at {d['age']} ago
+   // Detected by: CloudOps AI Feature #3 (hourly scan)
  }}""", language="diff")

# ============================================================
# AI #4: ACCESS ANOMALY / RBAC AI
# ============================================================
elif page == "🔐 AI #4 · Access Anomaly":
    st.markdown("### 🔐 AI Feature #4 — Access Anomaly Detection & RBAC AI")
    st.markdown(f"""{ai_pill(4)} Analyzes Entra ID sign-in logs, RBAC assignments, and PIM activation patterns. Detects stale service principals, over-privileged accounts, impossible travel, and recommends least-privilege roles for {ORG}.""", unsafe_allow_html=True)
    st.markdown("---")

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(kpi_card("Total Identities","234","Users + SPNs + Groups"), unsafe_allow_html=True)
    with c2: st.markdown(kpi_card("Anomalies Found","6","Last 7 days","dn"), unsafe_allow_html=True)
    with c3: st.markdown(kpi_card("Stale Identities","4","90+ days inactive","dn"), unsafe_allow_html=True)
    with c4: st.markdown(kpi_card("Over-Privileged","3","Recommend downgrade","dn"), unsafe_allow_html=True)

    st.markdown("---")
    tab1, tab2, tab3 = st.tabs(["🚨 Anomaly Findings","🔑 RBAC Recommendations","📊 Sign-in Analytics"])

    with tab1:
        for a in st.session_state.access_anomalies:
            icon = severity_icon(a["sev"])
            with st.expander(f"{icon} [{a['type']}] {a['identity']}: {a['finding'][:80]}...", expanded=(a["sev"]=="Critical")):
                st.markdown(f"**Severity:** {badge(a['sev'])} &nbsp;|&nbsp; **Type:** {badge(a['type'])} &nbsp;|&nbsp; **Risk Score:** {a['risk_score']}/10", unsafe_allow_html=True)
                st.markdown(f"**Investigation Details:** {a['detail']}")
                level = "crit" if a["sev"]=="Critical" else "warn" if a["sev"] in ["High","Medium"] else "ok"
                st.markdown(rec_box(f"🤖 <strong>AI Recommendation:</strong> {a['rec']}", level), unsafe_allow_html=True)
                if a["sev"] in ["Critical","High"]:
                    c1, c2 = st.columns(2)
                    if c1.button("🚨 Apply Recommendation", key=f"access_apply_{a['identity'][:12]}", type="primary", use_container_width=True):
                        st.success("✅ Action applied. Audit log entry created. Affected user notified via Teams.")
                    if c2.button("📋 Create Incident", key=f"access_incident_{a['identity'][:12]}", use_container_width=True):
                        st.info("ServiceNow incident INC-4812 created and assigned to Security Operations.")

    with tab2:
        st.markdown(f"**AI-Generated Least-Privilege Recommendations for {ORG}**")
        rbac_data = pd.DataFrame([
            {"Identity":"svc-jenkins-deploy","Current Role":"Contributor (4 subs)","AI Recommendation":"Custom: FutureMinds DevOps Deployer (Dev/Test only)","Permissions Reduction":"75%","Annual Cost Savings":"N/A","Risk Reduction":"High"},
            {"Identity":"svc-meridian-etl","Current Role":"Contributor (Data Platform)","AI Recommendation":"Custom: Meridian Pipeline Operator (SQL + Storage + ADF)","Permissions Reduction":"62%","Annual Cost Savings":"N/A","Risk Reduction":"Medium"},
            {"Identity":"svc-monitoring-agent","Current Role":"Reader (All subscriptions)","AI Recommendation":"Monitoring Reader (scoped to Log Analytics workspace)","Permissions Reduction":"45%","Annual Cost Savings":"N/A","Risk Reduction":"Low"},
            {"Identity":"dr.chen (User)","Current Role":"Owner via PIM (Data Platform)","AI Recommendation":"Custom: ML Platform Contributor (standing) + Owner JIT for emergencies","Permissions Reduction":"30%","Annual Cost Savings":"N/A","Risk Reduction":"Medium"},
        ])
        st.dataframe(rbac_data, use_container_width=True, hide_index=True)

    with tab3:
        st.markdown("**Sign-in Pattern Analysis — All Identities (30 days)**")
        hours = list(range(24))
        np.random.seed(7)
        normal = [3,2,1,1,0,1,6,22,48,44,40,35,32,36,42,44,38,26,14,10,8,6,5,4]
        anomalous = [0,0,0,4,6,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        fig = go.Figure()
        fig.add_trace(go.Bar(x=hours, y=normal, name="Normal", marker_color="#0369A1", opacity=0.85))
        fig.add_trace(go.Bar(x=hours, y=anomalous, name="Anomalous", marker_color="#DC2626"))
        fig.update_layout(height=260, margin=dict(l=0,r=0,t=10,b=0), barmode="stack", xaxis_title="Hour of Day (UTC)", yaxis_title="Sign-in Events", plot_bgcolor="white", legend=dict(orientation="h",y=-0.22), yaxis=dict(gridcolor="#F1F5F9"))
        st.plotly_chart(fig, use_container_width=True)
        st.caption("⚠️ Anomalous activity cluster at 3-5 AM UTC correlates with ext-contractor-rajesh impossible travel incident.")

# ============================================================
# AI #5: NETWORK POSTURE ANALYZER
# ============================================================
elif page == "🛡️ AI #5 · Network Posture":
    st.markdown("### 🛡️ AI Feature #5 — Network Posture Analyzer")
    st.markdown(f"""{ai_pill(5)} Scans all NSG, Azure Firewall, UDR, and Private Endpoint configurations against CIS Azure benchmarks and {ORG} security policies. Detects rule conflicts, open ports, and auto-generates network topology documentation.""", unsafe_allow_html=True)
    st.markdown("---")

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(kpi_card("Posture Score","87/100","↑ 4 this month"), unsafe_allow_html=True)
    with c2: st.markdown(kpi_card("NSGs Scanned","24","All subscriptions"), unsafe_allow_html=True)
    with c3: st.markdown(kpi_card("FW Rules Analyzed","47","5 conflicts found","dn"), unsafe_allow_html=True)
    with c4: st.markdown(kpi_card("Open Findings","5","2 critical","dn"), unsafe_allow_html=True)

    st.markdown("---")
    tab1, tab2, tab3 = st.tabs(["🔍 CIS Findings","🗺️ Auto-Generated Topology","🔥 Firewall Conflict Analysis"])

    with tab1:
        for f in st.session_state.net_findings:
            icon = severity_icon(f["sev"])
            with st.expander(f"""{icon} [{f['cis']}] {f['finding']} — {f['sub']}""", expanded=(f["sev"]=="Critical")):
                st.markdown(f"**Impact:** {f['impact']}")
                level = "crit" if f["sev"]=="Critical" else "warn" if f["sev"]=="High" else "ok"
                st.markdown(rec_box(f"🤖 <strong>AI Recommendation:</strong> {f['rec']}", level), unsafe_allow_html=True)
                st.markdown("**Auto-Generated Remediation Command:**")
                st.code(f["remediation_code"], language="bash")
                if st.button("🔧 Execute Remediation Pipeline", key=f"net_fix_{f['cis']}", use_container_width=True):
                    st.success("✅ Remediation pipeline triggered. PR created with IaC update. Validation running...")

    with tab2:
        st.markdown(f"**AI-Generated Network Topology — {ORG} Azure Landing Zone**")
        st.code(f"""╔══════════════════════════════════════════════════════════════════════╗
║  {ORG} Azure Landing Zone — Hub-Spoke Network Topology              ║
║  Auto-generated by AI Feature #5 from live Azure Network Watcher     ║
╚══════════════════════════════════════════════════════════════════════╝

Hub VNet (10.0.0.0/16) ─── Connectivity Subscription
├── AzureFirewallSubnet (10.0.1.0/24) ──── Azure Firewall [DNAT + App + Network Rules]
│   └── Private IP: 10.0.1.4 (force-tunnel target)
├── GatewaySubnet (10.0.2.0/24) ────────── ExpressRoute (2 Gbps) → On-Prem DC
├── AzureBastionSubnet (10.0.3.0/24) ───── Bastion Host [Secure VM access, no public IPs]
├── AppSubnet (10.0.10.0/24) ───────────── Azure Functions + APIM + OpenAI PE + AI Search PE
│
├── [VNet Peering ✓] → Spoke: Production (10.1.0.0/16)
│   ├── snet-aks (10.1.1.0/24) ──────────── AKS Cluster (private API) [3 system + 2-8 user nodes]
│   ├── snet-pe (10.1.2.0/24) ──────────── SQL MI PE, Cosmos DB PE, Redis PE, Storage PE
│   ├── snet-apps (10.1.3.0/24) ─────────── App Services (VNet integrated)
│   └── NSG: ✅ Compliant (all rules via IaC)
│
├── [VNet Peering ✓] → Spoke: Dev/Test (10.2.0.0/16)
│   ├── snet-dev (10.2.1.0/24) ──────────── Dev VMs, UAT, Sandbox resources
│   ├── snet-sandbox (10.2.2.0/24) ──────── Auto-provisioned sandboxes (14-day TTL)
│   └── ⚠️ NSG: SSH from 0.0.0.0/0 OPEN — REMEDIATE (CIS 6.2)
│
├── [VNet Peering ✓] → Spoke: Data Platform (10.3.0.0/16)
│   ├── snet-data (10.3.1.0/24) ─────────── ADLS Gen2, Synapse, ADF, Informatica agent
│   ├── snet-ml (10.3.2.0/24) ──────────── ML Compute (GPU VMs, ML workspace)
│   └── ⚠️ UDR: Missing force-tunnel to hub FW — REMEDIATE (CIS 6.1)
│
└── On-Premises (via ExpressRoute)
    ├── Source Systems: Oracle R12 EBS, Salesforce, SAP S/4HANA
    └── Corporate Network: Active Directory, DNS, SCCM""", language="text")
        st.info("This topology is live-generated from Azure Resource Graph + Network Watcher. Updated every scan cycle.")

    with tab3:
        st.markdown("**Azure Firewall Rule Conflict Analysis**")
        conflicts = pd.DataFrame([
            {"Rule A":"Allow-SQL-MI (Priority 100)","Rule B":"Deny-All-SQL (Priority 500)","Analysis":"Rule A allows TCP 1433 for SQL MI; Rule B denies all SQL. A wins by priority — correct intent but consider merging with explicit allow-list.","Status":"✅ OK (by priority)"},
            {"Rule A":"Allow-Internet-443 (Priority 200)","Rule B":"Deny-All-Outbound (Priority 65000)","Analysis":"Overly broad 443 outbound from Sandbox. Any HTTPS destination reachable — data exfiltration risk. Restrict to FQDN tags.","Status":"⚠️ Review scope"},
            {"Rule A":"Allow-Snowflake (Priority 200)","Rule B":"Allow-Databricks (Priority 250)","Analysis":"Both rules allow overlapping IP ranges in 52.x.x.x/16 CIDR. Consolidate into single 'Allow-DataPartners' rule for clarity.","Status":"⚠️ Consolidate"},
            {"Rule A":"Allow-ADF-to-OnPrem (Priority 150)","Rule B":"Deny-RFC1918 (Priority 400)","Analysis":"ADF needs on-prem access via ExpressRoute (10.x.x.x). Deny-RFC1918 would block this if ADF priority was higher. Currently correct but fragile.","Status":"⚠️ Document dependency"},
        ])
        st.dataframe(conflicts, use_container_width=True, hide_index=True)

# ============================================================
# AI #6: FINOPS AI ENGINE
# ============================================================
elif page == "💰 AI #6 · FinOps AI":
    st.markdown("### 💰 AI Feature #6 — FinOps AI Engine")
    st.markdown(f"""{ai_pill(6)} Monitors {ORG}'s $142K/mo Azure spend across 5 subscriptions. Detects cost anomalies in real-time, forecasts future spend, recommends rightsizing, Reserved Instances, Spot VMs, and identifies orphaned resources.""", unsafe_allow_html=True)
    st.markdown("---")

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(kpi_card("Feb Spend (MTD)","$68.4K","11 days in, on track"), unsafe_allow_html=True)
    with c2: st.markdown(kpi_card("Full Month Forecast","$138.2K","↓ $3.8K under budget"), unsafe_allow_html=True)
    with c3: st.markdown(kpi_card("AI Savings Found","$13.0K/mo","5 recommendations"), unsafe_allow_html=True)
    with c4: st.markdown(kpi_card("Cost Anomalies","2","1 open, 1 resolved","dn"), unsafe_allow_html=True)

    st.markdown("---")
    tab1, tab2, tab3 = st.tabs(["📊 Cost Breakdown & Forecast","🤖 AI Savings Recommendations","🚨 Anomaly Detection"])

    with tab1:
        col1, col2 = st.columns([3, 2])
        with col1:
            np.random.seed(99)
            subs = ["Production","Dev/Test","Data Platform","Hub","Sandbox"]
            services = ["Compute","Database","Storage","Network","AI/ML","Other"]
            data = []
            for s in subs:
                mult = 3.2 if s=="Production" else 2.0 if s=="Data Platform" else 1.5 if s=="Dev/Test" else 0.9 if s=="Hub" else 0.5
                for v in services:
                    data.append({"Subscription":s,"Service":v,"Cost ($K)":round(np.random.uniform(0.5, 8) * mult, 1)})
            fig = px.bar(pd.DataFrame(data), x="Subscription", y="Cost ($K)", color="Service",
                         color_discrete_sequence=["#0369A1","#7C3AED","#059669","#DC2626","#D97706","#64748B"])
            fig.update_layout(height=320, margin=dict(l=0,r=0,t=10,b=0), plot_bgcolor="white", legend=dict(orientation="h",y=-0.2,font=dict(size=10)), yaxis=dict(gridcolor="#F1F5F9"))
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("**Chargeback by Cost Center**")
            chargeback = pd.DataFrame({
                "Cost Center": ["IT-Platform","IT-Data","IT-DevOps","BU-Analytics","IT-Security"],
                "MTD ($K)": ["28.4","18.9","8.2","7.6","5.3"],
                "Budget ($K)": ["32.0","22.0","10.0","9.0","6.0"],
                "Utilization": ["89%","86%","82%","84%","88%"],
                "Status": ["✅","✅","✅","✅","✅"],
            })
            st.dataframe(chargeback, use_container_width=True, hide_index=True)

            st.markdown("**30-Day Spend Forecast**")
            forecast_dates = pd.date_range("2026-02-01", periods=28, freq="D")
            actual = [4.8 + np.random.uniform(-0.3, 0.5) for _ in range(11)]
            forecast = [actual[-1] + (i * 0.12) + np.random.uniform(-0.2, 0.2) for i in range(17)]
            fig3 = go.Figure()
            fig3.add_trace(go.Scatter(x=forecast_dates[:11], y=actual, name="Actual", mode="lines+markers", line=dict(color="#0369A1", width=2.5), marker=dict(size=5)))
            fig3.add_trace(go.Scatter(x=forecast_dates[10:], y=[actual[-1]]+forecast, name="AI Forecast", mode="lines", line=dict(color="#7C3AED", width=2, dash="dash")))
            fig3.add_hline(y=5.1, line_dash="dot", line_color="#DC2626", annotation_text="Daily Budget", annotation_position="top right")
            fig3.update_layout(height=180, margin=dict(l=0,r=0,t=10,b=0), plot_bgcolor="white", legend=dict(orientation="h",y=-0.3), yaxis_title="$/day (K)", yaxis=dict(gridcolor="#F1F5F9"))
            st.plotly_chart(fig3, use_container_width=True)

    with tab2:
        st.markdown(f"**AI-Generated Savings Recommendations — Total: $13.0K/mo ({ORG})**")
        total_savings = 0
        for rec in st.session_state.finops_recs:
            save_num = float(rec["save"].replace("$","").replace(",","").replace("/mo",""))
            total_savings += save_num
            conf_color = "green" if rec["conf"]=="High" else "amber"
            st.markdown(f"""<div class="scenario-card" style="border-left-color:{'var(--green)' if rec['conf']=='High' else 'var(--amber)'}">
            <div style="display:flex;justify-content:space-between;align-items:center">
                <h4>{rec['action'][:80]}</h4>
                <span style="font-size:18px;font-weight:700;color:var(--green)">{rec['save']}</span>
            </div>
            <div class="meta">{rec['cat']} · Confidence: {badge(rec['conf'])} · Risk: {badge(rec['risk'])}</div>
            <div class="desc">{rec['detail']}</div>
            </div>""", unsafe_allow_html=True)
            if st.button(f"✅ Apply: {rec['cat']}", key=f"finops_{rec['save']}", use_container_width=True):
                st.success(f"Optimization applied. Tracking in FinOps dashboard. Estimated annual savings: ${save_num*12:,.0f}")

    with tab3:
        st.markdown("**AI-Powered Cost Anomaly Detection**")
        st.markdown(rec_box("""🚨 <strong>OPEN Anomaly — Data Platform Subscription</strong><br>
<strong>When:</strong> Feb 9, 2026 at 11:32 PM UTC<br>
<strong>What:</strong> Synapse Dedicated SQL Pool spend spiked 42% ($187 → $266 in 24h)<br>
<strong>Root Cause (AI):</strong> Scheduled auto-pause job failed due to expired Managed Identity credential. Pool ran 24 hours instead of 10 hours.<br>
<strong>Impact:</strong> Excess cost: ~$340 for that day<br>
<strong>AI Fix:</strong> Credential auto-rotated. Auto-pause job re-enabled. Alert set for pause failures.""", "crit"), unsafe_allow_html=True)

        st.markdown(rec_box("""✅ <strong>RESOLVED — Sandbox Subscription</strong><br>
<strong>When:</strong> Feb 7, 2026<br>
<strong>What:</strong> Sandbox spend dropped to $0 (from avg $28/day)<br>
<strong>Root Cause (AI):</strong> Auto-cleanup job removed all sandbox resources per 14-day TTL policy. Expected behavior — all sandbox resources had exceeded their time-to-live.<br>
<strong>Status:</strong> Confirmed as expected. No action needed.""", "ok"), unsafe_allow_html=True)

# ============================================================
# AI #7: RISK SCORER + AUTO-APPROVE
# ============================================================
elif page == "⚡ AI #7 · Risk Scorer":
    st.markdown("### ⚡ AI Feature #7 — AI Risk Scorer + Automated Approvals")
    st.markdown(f"""{ai_pill(7)} Every change request in {ORG} is AI-scored on a 1-10 scale. Low-risk changes auto-approve instantly. Medium and high-risk changes route through tiered approval chains with SLA tracking and Teams adaptive cards.""", unsafe_allow_html=True)
    st.markdown("---")

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(kpi_card("Requests Scored","523","This month"), unsafe_allow_html=True)
    with c2: st.markdown(kpi_card("Auto-Approved","387","74% of all requests"), unsafe_allow_html=True)
    with c3: st.markdown(kpi_card("Manual Review","136","26% — Med + High"), unsafe_allow_html=True)
    with c4: st.markdown(kpi_card("Avg Approval Time","1.8 hrs","↓ from 18 hrs legacy"), unsafe_allow_html=True)

    st.markdown("---")

    # Risk tier visualization
    st.markdown("**AI Risk Scoring Model**")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""<div class="risk-tier" style="background:var(--green-light);border:2px solid #6EE7B7">
        <div class="score" style="color:var(--green-dark)">Low (1-3)</div>
        <div class="label" style="color:var(--green-dark)">✅ Auto-Approved Instantly</div>
        <div class="detail" style="color:var(--green-dark)">Zero human touch · Pipeline triggers automatically</div>
        <div style="color:var(--green);font-size:10px;margin-top:8px;font-weight:500">Dev/Sandbox · Reader/tags · Known templates · Low blast radius</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="risk-tier" style="background:var(--amber-light);border:2px solid #FCD34D">
        <div class="score" style="color:var(--amber-dark)">Medium (4-6)</div>
        <div class="label" style="color:var(--amber-dark)">⏳ L1 Approver (Teams Card)</div>
        <div class="detail" style="color:var(--amber-dark)">SLA: 4 hours · Auto-escalate if breached</div>
        <div style="color:var(--amber);font-size:10px;margin-top:8px;font-weight:500">Test env · Contributor roles · FW rule changes · Standard templates</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="risk-tier" style="background:var(--red-light);border:2px solid #FCA5A5">
        <div class="score" style="color:var(--red-dark)">High (7-10)</div>
        <div class="label" style="color:var(--red-dark)">🔒 L1 + L2 + CISO Chain</div>
        <div class="detail" style="color:var(--red-dark)">SLA: 24 hours · VP escalation if breached</div>
        <div style="color:var(--red);font-size:10px;margin-top:8px;font-weight:500">Production · Owner role · NSG 0.0.0.0/0 · PE deletion · GPU provisioning</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Pending Approvals")
    pending = [a for a in st.session_state.approvals if a["status"]=="Awaiting Approval"]
    if not pending:
        st.success("🎉 All approvals processed! No pending items.")
    else:
        for a in pending:
            icon = "🔴" if a["risk_level"]=="High" else "🟡" if a["risk_level"]=="Medium" else "🟢"
            with st.expander(f"""{icon} {a['id']} — {a['desc']} (Score: {a['risk_score']}/10 · {a['risk_level']})""", expanded=True):
                col1, col2 = st.columns([3, 2])
                with col1:
                    st.markdown(f"**Request:** {a['req']} &nbsp;|&nbsp; **Type:** `{a['type']}` &nbsp;|&nbsp; **Risk:** {badge(a['risk_level'])} **{a['risk_score']}/10**", unsafe_allow_html=True)
                    st.markdown("**Score Breakdown:**")
                    for factor, value in a["factors"].items():
                        st.markdown(f"&nbsp;&nbsp;· **{factor}:** {value}")
                with col2:
                    st.markdown(rec_box(f"🤖 <strong>AI Analysis:</strong><br>{a['ai_rec']}", "warn" if a["risk_level"]=="Medium" else "crit"), unsafe_allow_html=True)

                btn1, btn2, btn3 = st.columns(3)
                if btn1.button("✅ Approve", key=f"approve_{a['id']}", type="primary", use_container_width=True):
                    a["status"] = "Approved"
                    st.success(f"✅ Approved! IaC pipeline triggered. Requestor notified via Teams.")
                    st.rerun()
                if btn2.button("❌ Reject", key=f"reject_{a['id']}", use_container_width=True):
                    a["status"] = "Rejected"
                    st.error("Rejected. Requestor notified with AI-generated explanation.")
                    st.rerun()
                if btn3.button("💬 Request More Info", key=f"info_{a['id']}", use_container_width=True):
                    st.info("Teams message sent to requestor asking for additional justification.")

    st.markdown("---")
    st.markdown("##### Recent Scoring Activity")
    scoring_log = pd.DataFrame([
        {"ID":"REQ-2605","Type":"Sandbox Provision","Sub":"Dev/Test","Score":"1.9","Level":"Low","Decision":"✅ Auto-Approved","Time":"< 1 min","By":"AI Engine"},
        {"ID":"REQ-2604","Type":"FW Rule Add","Sub":"Hub","Score":"4.8","Level":"Medium","Decision":"✅ L1 Approved","Time":"47 min","By":"Platform Lead"},
        {"ID":"REQ-2601","Type":"AKS Production","Sub":"Production","Score":"7.4","Level":"High","Decision":"✅ L1+L2+CISO","Time":"5.2 hrs","By":"Multi-level chain"},
        {"ID":"REQ-2606","Type":"Reader (Auditor)","Sub":"Production","Score":"2.1","Level":"Low","Decision":"✅ Auto-Approved","Time":"< 1 min","By":"AI Engine"},
        {"ID":"REQ-2599","Type":"NSG 0.0.0.0/0","Sub":"Production","Score":"9.8","Level":"High","Decision":"❌ Rejected by AI","Time":"Instant","By":"AI Policy Engine"},
    ])
    st.dataframe(scoring_log, use_container_width=True, hide_index=True)

# ============================================================
# 📋 COMPLIANCE & AUDIT
# ============================================================
elif page == "📋 Compliance & Audit":
    st.markdown("### 📋 Compliance & Audit Trail")
    st.markdown(f"""Full compliance monitoring and immutable audit trail across all {ORG} subscriptions. Every AI decision, approval, deployment, and configuration change is logged.""", unsafe_allow_html=True)
    st.markdown("---")

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(kpi_card("Compliance Score","96.2%","↑ 1.4% MoM"), unsafe_allow_html=True)
    with c2: st.markdown(kpi_card("Policy Violations","7","↓ 3 from last week"), unsafe_allow_html=True)
    with c3: st.markdown(kpi_card("Resources Scanned","847","100% coverage"), unsafe_allow_html=True)
    with c4: st.markdown(kpi_card("Auto-Remediated","14","This month"), unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("##### Compliance by Category")
        categories = ["Logging & Monitoring","Data Protection","Network Security","Compute Security","Identity & Access","Tagging & Organization"]
        scores = [100, 97, 94, 95, 93, 92]
        colors = ["#059669" if s >= 95 else "#D97706" if s >= 90 else "#DC2626" for s in scores]
        fig = go.Figure(go.Bar(x=scores, y=categories, orientation="h", marker_color=colors,
                               text=[f"{s}%" for s in scores], textposition="outside", textfont=dict(size=11, color="#334155")))
        fig.update_layout(height=280, margin=dict(l=0,r=50,t=10,b=0), plot_bgcolor="white",
                         xaxis=dict(range=[80, 105], gridcolor="#F1F5F9"), yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("##### Active Violations")
        violations = [
            ("🔴","2 Storage accounts with public access","Dev/Test + Sandbox"),
            ("🟡","3 VMs missing diagnostic settings","Sandbox"),
            ("🟡","1 NSG allows SSH from 0.0.0.0/0","Dev/Test"),
            ("🟢","1 resource missing mandatory tags","Data Platform"),
        ]
        for icon, desc, sub in violations:
            st.markdown(f"""<div style="padding:8px 12px;margin:4px 0;background:#F8FAFC;border-radius:6px;border-left:3px solid {'#DC2626' if icon=='🔴' else '#D97706' if icon=='🟡' else '#059669'};font-size:12px">
            {icon} <strong>{sub}:</strong> {desc}</div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("##### Audit Trail — Latest 25 Events")
    actions = ["AI risk scored request","Resource deployed via pipeline","FW rule added (IaC)","PIM role activated","Policy evaluated (deny)","Access approved (auto)","PE created","NSG modified (IaC)","Drift detected (auto-fix PR)","Cost anomaly flagged","Compliance scan completed","Sandbox auto-cleanup"]
    actors = ["CloudOps AI Engine","Priya S. (Pipeline)","Marcus W.","Anika R.","AI-AutoRemediation","AI-RiskScorer","Jordan K. (Pipeline)","System (Scheduled)"]
    subs = ["Production","Dev/Test","Hub","Data Platform","Sandbox"]
    results = ["Success","Success","Success","Success","Denied by Policy","Success"]

    events = []
    for i in range(25):
        dt = datetime.datetime.now() - datetime.timedelta(hours=random.randint(1, 200), minutes=random.randint(0, 59))
        events.append({
            "Timestamp": dt.strftime("%Y-%m-%d %H:%M UTC"),
            "Action": random.choice(actions),
            "Actor": random.choice(actors),
            "Subscription": random.choice(subs),
            "Result": random.choice(results),
        })
    events.sort(key=lambda x: x["Timestamp"], reverse=True)
    st.dataframe(pd.DataFrame(events), use_container_width=True, hide_index=True)
