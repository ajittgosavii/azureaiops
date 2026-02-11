import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json, random, datetime, time

st.set_page_config(page_title="CloudOps Unified Portal", page_icon="☁️", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    .main-header{background:linear-gradient(135deg,#0078D4 0%,#005A9E 100%);padding:12px 24px;border-radius:8px;margin-bottom:16px;display:flex;justify-content:space-between;align-items:center}
    .main-header h2{color:white;margin:0;font-size:20px} .main-header p{color:rgba(255,255,255,0.8);margin:0;font-size:11px}
    .kpi-card{background:white;border:1px solid #E5E7EB;border-radius:10px;padding:14px 18px;text-align:center;box-shadow:0 1px 3px rgba(0,0,0,0.06)}
    .kpi-card .value{font-size:26px;font-weight:700;color:#0078D4;margin:2px 0} .kpi-card .label{font-size:11px;color:#6B7280;text-transform:uppercase;letter-spacing:0.5px}
    .kpi-card .delta{font-size:10px;padding:2px 8px;border-radius:10px;display:inline-block;margin-top:2px}
    .kpi-card .delta.up{background:#D1FAE5;color:#065F46} .kpi-card .delta.down{background:#FEE2E2;color:#991B1B}
    .badge{padding:3px 10px;border-radius:12px;font-size:11px;font-weight:600;display:inline-block}
    .badge-active{background:#D1FAE5;color:#065F46} .badge-pending{background:#FEF3C7;color:#92400E}
    .badge-error{background:#FEE2E2;color:#991B1B} .badge-info{background:#DBEAFE;color:#1E40AF}
    .ai-tag{background:linear-gradient(135deg,#EDE7F6,#E8D5F5);border:1px solid #B39DDB;border-radius:6px;padding:3px 10px;font-size:10px;font-weight:700;color:#5C2D91;display:inline-block}
    .chat-user{background:#EFF6FF;border-radius:12px 12px 2px 12px;padding:10px 14px;margin:6px 0;margin-left:40px;font-size:13px}
    .chat-ai{background:#F0FDF4;border-radius:12px 12px 12px 2px;padding:10px 14px;margin:6px 0;margin-right:40px;font-size:13px;border-left:3px solid #22C55E}
    .ai-rec{background:#F0FDF4;border-left:3px solid #22C55E;padding:10px 14px;margin:6px 0;border-radius:0 6px 6px 0;font-size:13px}
    .ai-warn{background:#FFFBEB;border-left:3px solid #F59E0B;padding:10px 14px;margin:6px 0;border-radius:0 6px 6px 0;font-size:13px}
    .ai-alert{background:#FEF2F2;border-left:3px solid #EF4444;padding:10px 14px;margin:6px 0;border-radius:0 6px 6px 0;font-size:13px}
    #MainMenu{visibility:hidden} footer{visibility:hidden} .stDeployButton{display:none} div[data-testid="stToolbar"]{display:none}
</style>
""", unsafe_allow_html=True)

if "initialized" not in st.session_state:
    st.session_state.update({"initialized":True,"persona":"Cloud Engineer","chat_history":[],"prov_history":[],
        "requests":[
            {"id":"REQ-001","type":"Environment","desc":"New dev sandbox for Atlas POC","status":"Approved","risk":"Low","date":"2026-02-10","sub":"Dev/Test"},
            {"id":"REQ-002","type":"Network","desc":"Private endpoint for SQL MI (Prod)","status":"Pending","risk":"High","date":"2026-02-11","sub":"Production"},
            {"id":"REQ-003","type":"Access","desc":"Contributor role on Data Platform RG","status":"AI Review","risk":"Medium","date":"2026-02-11","sub":"Data Platform"},
            {"id":"REQ-004","type":"Firewall","desc":"Allow outbound to Informatica IPs","status":"Approved","risk":"Medium","date":"2026-02-09","sub":"Hub"},
            {"id":"REQ-005","type":"Environment","desc":"Prod sub for Atlas migration","status":"Deployed","risk":"High","date":"2026-02-05","sub":"Production"},
        ],
        "approvals":[
            {"id":"APR-001","req":"REQ-002","type":"Network","desc":"Private endpoint for SQL MI","risk_score":8.2,"risk_level":"High","ai_rec":"PE config matches standards. Requires Network + Security Admin.","status":"Awaiting Approval"},
            {"id":"APR-002","req":"REQ-003","type":"Access","desc":"Contributor on Data Platform RG","risk_score":5.5,"risk_level":"Medium","ai_rec":"Contributor broad. Suggest custom: Data Pipeline Operator. 90-day expiry.","status":"Awaiting Approval"},
        ]})

def K(label,value,delta=None,d="up"):
    dh=f'<div class="delta {d}">{delta}</div>' if delta else ""
    return f'<div class="kpi-card"><div class="label">{label}</div><div class="value">{value}</div>{dh}</div>'

def B(s):
    m={"Approved":"badge-active","Deployed":"badge-active","Pending":"badge-pending","AI Review":"badge-info","Awaiting Approval":"badge-pending","Rejected":"badge-error","Low":"badge-active","Medium":"badge-pending","High":"badge-error","Critical":"badge-error","Open":"badge-pending","Pass":"badge-active","Drift":"badge-error","Stale":"badge-error","Over-privileged":"badge-pending","Anomaly":"badge-error","OK":"badge-active"}
    return f'<span class="badge {m.get(s,"badge-info")}">{s}</span>'

def AI(n): return f'<span class="ai-tag">🧠 AI Feature #{n}</span>'

def call_claude(prompt, sys="You are an Azure CloudOps AI. Concise technical responses with CLI/Bicep. Under 300 words."):
    try:
        import anthropic
        k=st.secrets.get("ANTHROPIC_API_KEY",None)
        if not k: return None
        return anthropic.Anthropic(api_key=k).messages.create(model="claude-sonnet-4-20250514",max_tokens=1024,system=sys,messages=[{"role":"user","content":prompt}]).content[0].text
    except: return None

IAC={"Virtual Machine":"""param location string = resourceGroup().location
param vmName string = '{name}'
resource vm 'Microsoft.Compute/virtualMachines@2024-03-01' = {{
  name: vmName; location: location
  tags: {{ environment: '{env}'; costCenter: '{cc}'; project: 'Atlas-Migration'; managedBy: 'CloudOps-Portal' }}
  identity: {{ type: 'SystemAssigned' }}
  properties: {{ hardwareProfile: {{ vmSize: '{size}' }}; osProfile: {{ computerName: vmName; adminUsername: 'azureAdmin' }} }}
}}
resource diag 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {{
  name: '${{vmName}}-diag'; scope: vm
  properties: {{ workspaceId: logAnalyticsId; metrics: [{{ category: 'AllMetrics'; enabled: true }}] }}
}}""",
"Azure SQL Database":"""param sqlName string = '{name}'
resource sql 'Microsoft.Sql/servers@2023-08-01-preview' = {{
  name: sqlName; location: location
  tags: {{ environment: '{env}'; costCenter: '{cc}'; project: 'Atlas-Migration' }}
  properties: {{ administratorLogin: 'sqladmin'; minimalTlsVersion: '1.2'; publicNetworkAccess: 'Disabled' }}
}}
resource pe 'Microsoft.Network/privateEndpoints@2024-01-01' = {{
  name: '${{sqlName}}-pe'; location: location
  properties: {{ subnet: {{ id: subnetId }}; privateLinkServiceConnections: [{{ name: 'plsc'; properties: {{ privateLinkServiceId: sql.id; groupIds: ['sqlServer'] }} }}] }}
}}""",
"Storage Account":"""param storageName string = '{name}'
resource storage 'Microsoft.Storage/storageAccounts@2023-05-01' = {{
  name: storageName; location: location; kind: 'StorageV2'
  sku: {{ name: '{size}' }}
  tags: {{ environment: '{env}'; costCenter: '{cc}'; project: 'Atlas-Migration' }}
  properties: {{ isHnsEnabled: true; publicNetworkAccess: 'Disabled'; minimumTlsVersion: 'TLS1_2' }}
}}"""}

def gen_iac(rt,cfg):
    r=call_claude(f"Generate Bicep for {rt}: {json.dumps(cfg)}. Include PE, diagnostics, tags. Code only.","Azure IaC expert. Production Bicep. PE+diagnostics+tags. Code only.")
    if r: return r
    return IAC.get(rt,f"// Template for {rt}").format(**cfg)

def header():
    st.markdown(f'<div class="main-header"><div><h2>☁️ CloudOps Unified Portal</h2><p>Azure Multi-Subscription · 7 Gen AI Features · Stryker</p></div><div style="text-align:right"><p style="font-size:13px;color:white;font-weight:600">{st.session_state.persona}</p><p style="font-size:10px;color:rgba(255,255,255,0.7)">stryker.onmicrosoft.com</p></div></div>',unsafe_allow_html=True)

with st.sidebar:
    st.markdown(f'<div style="background:linear-gradient(135deg,#EFF6FF,#DBEAFE);border:1px solid #BFDBFE;border-radius:8px;padding:12px;text-align:center;margin-bottom:12px"><div style="font-size:28px">👤</div><div style="font-weight:700;color:#1E40AF">{st.session_state.persona}</div><div style="color:#6B7280;font-size:11px">Stryker · Azure</div></div>',unsafe_allow_html=True)
    st.session_state.persona=st.selectbox("Persona",["Cloud Engineer","Network Admin","Security Admin","FinOps Analyst","DevOps Engineer","App Owner"])
    st.divider()
    page=st.radio("Navigation",["📊 Dashboard","🏗️ AI#1: NL→IaC Generator","🤖 AI#2: Ops Chatbot","🔄 AI#3: Drift Detector","🔐 AI#4: Access Anomaly","🛡️ AI#5: Network Posture","💰 AI#6: FinOps AI","⚡ AI#7: Risk Scorer","📋 Compliance & Audit"])
    st.divider()
    for n,s in [("Hub","🟢"),("Prod","🟢"),("Dev/Test","🟢"),("Data","🟡"),("Sandbox","🟢")]: st.markdown(f"{s} **{n}**")
    st.caption("CloudOps v2.0 · AI: Claude")

header()

if page=="📊 Dashboard":
    c1,c2,c3,c4,c5=st.columns(5)
    with c1: st.markdown(K("Subscriptions","5","All Healthy"),unsafe_allow_html=True)
    with c2: st.markdown(K("Resources","847","↑23 week"),unsafe_allow_html=True)
    with c3: st.markdown(K("Approvals","2","2 high","down"),unsafe_allow_html=True)
    with c4: st.markdown(K("Spend","$142K","↓8%"),unsafe_allow_html=True)
    with c5: st.markdown(K("Compliance","96.2%","↑1.4%"),unsafe_allow_html=True)
    st.markdown("---")
    col1,col2=st.columns(2)
    with col1:
        st.subheader("Cost Trend")
        dates=pd.date_range("2025-09",periods=6,freq="MS")
        fig=go.Figure()
        for sub,c,b in [("Prod","#107C10",55),("Dev","#0078D4",28),("Data","#5C2D91",35),("Hub","#D83B01",18)]:
            fig.add_trace(go.Scatter(x=dates,y=[b+random.uniform(-5,8) for _ in dates],name=sub,mode="lines+markers",line=dict(color=c,width=2)))
        fig.update_layout(height=280,margin=dict(l=0,r=0,t=10,b=0),legend=dict(orientation="h",y=-0.15),yaxis_title="$K",plot_bgcolor="white")
        st.plotly_chart(fig,use_container_width=True)
    with col2:
        st.subheader("7 AI Features — Activity")
        feats=["#1 NL→IaC","#2 Chatbot","#3 Drift","#4 Access AI","#5 Net Posture","#6 FinOps","#7 Risk Score"]
        fig2=go.Figure(go.Bar(x=[47,312,89,156,34,67,523],y=feats,orientation="h",marker_color="#7C3AED",text=[47,312,89,156,34,67,523],textposition="outside"))
        fig2.update_layout(height=280,margin=dict(l=0,r=40,t=10,b=0),plot_bgcolor="white",yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig2,use_container_width=True)
    st.subheader("Recent Requests")
    for r in st.session_state.requests[:5]:
        cols=st.columns([1,2,4,2,2,2])
        cols[0].markdown(f"**{r['id']}**");cols[1].markdown(r['type']);cols[2].markdown(r['desc']);cols[3].markdown(r['sub']);cols[4].markdown(B(r['status']),unsafe_allow_html=True);cols[5].markdown(r['date'])

elif page=="🏗️ AI#1: NL→IaC Generator":
    st.subheader("🏗️ AI Feature #1 — NL → IaC Generator")
    st.markdown(f"{AI(1)} Describe infrastructure in English → AI generates Bicep/Terraform with PE, diagnostics, tags.",unsafe_allow_html=True)
    tab1,tab2=st.tabs(["📝 Form","🧠 Natural Language"])
    with tab1:
        with st.form("pf"):
            c1,c2=st.columns(2)
            with c1:
                rt=st.selectbox("Type",["Virtual Machine","Azure SQL Database","Storage Account","AKS Cluster","App Service"])
                tgt=st.selectbox("Sub",["Prod-LandingZone","Dev-Test","Data-Platform","Sandbox-POC"])
                rn=st.text_input("Name",placeholder="vm-atlas-etl-01")
                env=st.selectbox("Env",["Production","Development","Test","Sandbox"])
            with c2:
                sz=st.selectbox("SKU",{"Virtual Machine":["Standard_D2s_v3","Standard_D4s_v3"],"Azure SQL Database":["GP_Gen5_2","GP_Gen5_4"],"Storage Account":["Standard_LRS","Standard_GRS"]}.get(rt,["Standard"]))
                rg=st.selectbox("Region",["East US 2","Central US"])
                cc=st.text_input("Cost Center",value="IT-CloudOps")
                jst=st.text_area("Justification",height=68)
            if st.form_submit_button("🚀 Generate IaC",use_container_width=True) and rn:
                cfg={"name":rn,"size":sz,"env":env.lower(),"cc":cc}
                with st.spinner("🧠 AI generating..."): time.sleep(1.2)
                st.success(f"✅ REQ-{random.randint(100,999)} submitted")
                for c,r in [("Region","✅"),("SKU","✅"),("Naming","✅" if "-" in rn else "⚠️"),("Tags","✅"),("PE","✅ Auto")]: st.markdown(f"  {r} — {c}")
                st.code(gen_iac(rt,cfg),language="bicep")
                risk="Low" if env in ["Development","Sandbox"] else "Medium" if env=="Test" else "High"
                st.markdown(f"**Risk:** {B(risk)} — {'Auto-approved' if risk=='Low' else 'Routed to approval'}",unsafe_allow_html=True)
    with tab2:
        nl=st.text_area("Describe:",placeholder="I need an AKS cluster in prod with 3 nodes, private API, Azure CNI...",height=100)
        if st.button("🧠 Generate",use_container_width=True) and nl:
            with st.spinner("AI analyzing..."):
                r=call_claude(f"Generate Bicep for: {nl}. Include PE, diagnostics, tags.","Azure IaC expert. Parse NL→Bicep. 1)Resources 2)Cost 3)Code")
                st.markdown(r if r else "**Resources:** SQL MI (GP_Gen5_4), PE, DNS\n**Cost:** ~$580/mo")
                if not r: st.code(gen_iac("Azure SQL Database",{"name":"sql-atlas","size":"GP_Gen5_4","env":"prod","cc":"IT-Data"}),language="bicep")

elif page=="🤖 AI#2: Ops Chatbot":
    st.subheader("🤖 AI Feature #2 — Ops Chatbot / Copilot")
    st.markdown(f"{AI(2)} Ask anything about your Azure environment in natural language.",unsafe_allow_html=True)
    for m in st.session_state.chat_history:
        st.markdown(f'<div class="{"chat-user" if m["role"]=="user" else "chat-ai"}">{"👤" if m["role"]=="user" else "🤖"} {m["content"]}</div>',unsafe_allow_html=True)
    qc=st.columns(4)
    for i,q in enumerate(["Show untagged resources","Generate AKS Bicep","Budget status?","Expiring PIM roles?"]):
        if qc[i].button(q,key=f"q{i}",use_container_width=True): st.session_state.chat_history.append({"role":"user","content":q});st.rerun()
    ui=st.chat_input("Ask CloudOps AI...")
    if ui:
        st.session_state.chat_history.append({"role":"user","content":ui})
        with st.spinner("🧠"):
            ai=call_claude(ui,f"CloudOps Copilot. 5 subs, 847 resources, $142K/mo. Persona: {st.session_state.persona}. Concise + CLI/Bicep.")
            if not ai:
                fb={"tag":"**Untagged:** vm-test-03, disk-orphan-01 in Dev/Test\n\n`az tag create --resource-id <id> --tags costCenter=IT-DevOps`","budget":"**Prod:** $58K/$65K ✅ | **Data:** $18K/$20K ⚠️ (Synapse off-hours)","pim":"**Expiring:** Sarah K. Owner Prod (Feb 14), Mike T. Contrib Data (Feb 13)","aks":"```bicep\nresource aks 'Microsoft.ContainerService/managedClusters@2024-02-01' = {\n  name: 'aks-atlas-prod'; properties: { apiServerAccessProfile: { enablePrivateCluster: true } }\n}\n```"}
                ai=next((v for k,v in fb.items() if k in ui.lower()),"Ask about provisioning, network, access, cost, or compliance. 💡 Add ANTHROPIC_API_KEY in secrets for full AI.")
            st.session_state.chat_history.append({"role":"assistant","content":ai})
        st.rerun()
    if st.button("🗑️ Clear"): st.session_state.chat_history=[];st.rerun()

elif page=="🔄 AI#3: Drift Detector":
    st.subheader("🔄 AI Feature #3 — Resource Drift Detector")
    st.markdown(f"{AI(3)} Compares ARM live state vs IaC repo. Detects drift, generates fix PRs, maintains parity.",unsafe_allow_html=True)
    c1,c2,c3,c4=st.columns(4)
    with c1: st.markdown(K("Scanned","847","Hourly"),unsafe_allow_html=True)
    with c2: st.markdown(K("Drifted","12","↓3","up"),unsafe_allow_html=True)
    with c3: st.markdown(K("Auto-Fixed","8","via PR"),unsafe_allow_html=True)
    with c4: st.markdown(K("Pending","4","Review","down"),unsafe_allow_html=True)
    st.markdown("---")
    drifts=[
        {"res":"nsg-prod-default","type":"NSG","sub":"Prod","drift":"Rule added manually (port 8443)","sev":"Critical","age":"2h"},
        {"res":"vm-atlas-etl-02","type":"VM","sub":"Prod","drift":"Size changed D4s→D8s manually","sev":"Medium","age":"6h"},
        {"res":"kv-cloudops-hub","type":"KeyVault","sub":"Hub","drift":"Soft delete disabled","sev":"Critical","age":"1d"},
        {"res":"sql-atlas-prod","type":"SQL","sub":"Prod","drift":"TLS min version to 1.0","sev":"Critical","age":"3h"},
        {"res":"sta-sandbox-01","type":"Storage","sub":"Sandbox","drift":"Public access enabled","sev":"Critical","age":"12h"},
        {"res":"aks-atlas-prod","type":"AKS","sub":"Prod","drift":"Nodes scaled 3→5 manually","sev":"Low","age":"4h"},
    ]
    for d in drifts:
        ic={"Critical":"🔴","High":"🟠","Medium":"🟡","Low":"🟢"}.get(d["sev"],"⚪")
        with st.expander(f"{ic} **{d['res']}** — {d['drift']} [{d['age']}]"):
            st.markdown(f"**Sub:** {d['sub']} | **Severity:** {B(d['sev'])}",unsafe_allow_html=True)
            cls="ai-alert" if d["sev"]=="Critical" else "ai-warn" if d["sev"] in ["High","Medium"] else "ai-rec"
            msg="Immediate fix. Security risk." if d["sev"]=="Critical" else "Review recommended." if d["sev"] in ["High","Medium"] else "Low risk. Update IaC if intentional."
            st.markdown(f'<div class="{cls}">🤖 {msg}</div>',unsafe_allow_html=True)
            c1,c2,c3=st.columns(3)
            if c1.button("🔄 Auto-Fix",key=f"fx_{d['res']}"): st.success("PR created → pipeline triggered")
            if c2.button("✅ Accept",key=f"ac_{d['res']}"): st.info("IaC updated to match")
            if c3.button("📋 Diff",key=f"df_{d['res']}"): st.code(f"- // IaC state\n+ // Live: {d['drift']}",language="diff")

elif page=="🔐 AI#4: Access Anomaly":
    st.subheader("🔐 AI Feature #4 — Access Anomaly / RBAC AI")
    st.markdown(f"{AI(4)} Analyzes Entra ID logs, detects stale SPNs, over-privilege, recommends least-privilege.",unsafe_allow_html=True)
    c1,c2,c3,c4=st.columns(4)
    with c1: st.markdown(K("Identities","234","Users+SPNs"),unsafe_allow_html=True)
    with c2: st.markdown(K("Anomalies","7","7 days","down"),unsafe_allow_html=True)
    with c3: st.markdown(K("Stale SPNs","4","90+ days","down"),unsafe_allow_html=True)
    with c4: st.markdown(K("Over-Priv","6","Downgrade","down"),unsafe_allow_html=True)
    st.markdown("---")
    tab1,tab2,tab3=st.tabs(["🚨 Anomalies","🔑 RBAC Recs","📊 Login Analytics"])
    with tab1:
        for sev,ident,find,rec in [
            ("🔴","legacy-svc-01 (SPN)","Owner on Prod — no activity 94 days","Revoke. Create scoped role if needed."),
            ("🔴","ext-contractor-02","Login from Russia + 3x failed MFA","Block sign-in. CA review."),
            ("🟠","jenkins-deploy-svc","Contributor on 4 subs — only uses Dev","Scope to Dev/Test. Custom role."),
            ("🟡","CloudOps-Engineers","3 members inactive 60+ days","Access review. Remove inactive."),
            ("🟡","data-team-lead","PIM Owner 12x this week (3x normal)","Investigate. Consider Reader + scoped PIM."),
        ]:
            with st.expander(f"{sev} {ident}: {find}"):
                cls="ai-alert" if sev=="🔴" else "ai-warn"
                st.markdown(f'<div class="{cls}">🤖 {rec}</div>',unsafe_allow_html=True)
                if st.button("Apply",key=f"rb_{ident[:8]}"): st.success("Applied + logged")
    with tab2:
        st.dataframe(pd.DataFrame([
            {"Identity":"jenkins-deploy-svc","Current":"Contributor (4 subs)","Recommended":"Custom: DevOps Deployer (Dev only)","Reduction":"75%"},
            {"Identity":"data-pipeline-svc","Current":"Contributor (Data)","Recommended":"Custom: Pipeline Operator","Reduction":"60%"},
            {"Identity":"monitoring-svc","Current":"Reader (All)","Recommended":"Monitoring Reader (Log Analytics)","Reduction":"40%"},
        ]),use_container_width=True,hide_index=True)
    with tab3:
        hrs=list(range(24));norm=[2,1,1,0,0,1,5,18,42,38,35,30,28,32,36,38,34,22,12,8,6,5,4,3];anom=[0,0,0,3,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        fig=go.Figure()
        fig.add_trace(go.Bar(x=hrs,y=norm,name="Normal",marker_color="#0078D4"))
        fig.add_trace(go.Bar(x=hrs,y=anom,name="Anomalous",marker_color="#EF4444"))
        fig.update_layout(height=240,margin=dict(l=0,r=0,t=10,b=0),barmode="stack",xaxis_title="Hour (UTC)",plot_bgcolor="white",legend=dict(orientation="h",y=-0.2))
        st.plotly_chart(fig,use_container_width=True)

elif page=="🛡️ AI#5: Network Posture":
    st.subheader("🛡️ AI Feature #5 — Network Posture Analyzer")
    st.markdown(f"{AI(5)} Scans NSG/FW/UDR against CIS benchmarks. Detects conflicts, open ports, auto-generates topology.",unsafe_allow_html=True)
    c1,c2,c3,c4=st.columns(4)
    with c1: st.markdown(K("Posture","87/100","↑4"),unsafe_allow_html=True)
    with c2: st.markdown(K("NSGs","24","All subs"),unsafe_allow_html=True)
    with c3: st.markdown(K("FW Rules","47","5 conflicts","down"),unsafe_allow_html=True)
    with c4: st.markdown(K("Issues","6","2 critical","down"),unsafe_allow_html=True)
    st.markdown("---")
    tab1,tab2,tab3=st.tabs(["🔍 Findings","🗺️ Topology","🔥 FW Conflicts"])
    with tab1:
        for sev,find,cis,sub,rec in [
            ("🔴","NSG allows 0.0.0.0/0 inbound SSH","CIS 6.2","Dev/Test","Restrict to bastion 10.0.3.0/24"),
            ("🔴","Storage public access Enabled","CIS 3.7","Sandbox","Disable + add PE"),
            ("🟠","FW allows 0.0.0.0/0:443 from Sandbox","CIS 6.5","Sandbox","Restrict to service tags"),
            ("🟡","3 NSGs no flow logs","CIS 6.4","Multiple","Enable flow logs → Log Analytics"),
            ("🟡","Data spoke missing force-tunnel UDR","CIS 6.1","Data","Add route → Azure FW"),
        ]:
            with st.expander(f"{sev} [{cis}] {find} — {sub}"):
                cls="ai-alert" if sev=="🔴" else "ai-warn" if sev=="🟠" else "ai-rec"
                st.markdown(f'<div class="{cls}">🤖 {rec}</div>',unsafe_allow_html=True)
                if st.button("🔧 Remediate",key=f"np_{cis}"): st.success("Pipeline triggered")
    with tab2:
        st.code("""Hub VNet (10.0.0.0/16) ─── Connectivity
├── AzureFirewallSubnet (10.0.1.0/24)
├── GatewaySubnet (10.0.2.0/24) → ExpressRoute → On-Prem
├── BastionSubnet (10.0.3.0/24)
├── AppSubnet (10.0.10.0/24) → Functions+APIM+OpenAI PE
│
├── [Peering] → Spoke-Prod (10.1.0.0/16)
│   ├── default (10.1.1.0/24) VMs, AKS
│   └── pe-subnet (10.1.2.0/24) SQL MI PE
│
├── [Peering] → Spoke-Dev (10.2.0.0/16)
│   └── ⚠️ NSG allows SSH 0.0.0.0/0
│
└── [Peering] → Spoke-Data (10.3.0.0/16)
    └── ⚠️ Missing force-tunnel UDR""")
        st.info("Auto-generated from live Network Watcher + Resource Graph")
    with tab3:
        st.dataframe(pd.DataFrame([
            {"Rule A":"Allow-SQL (P:100)","Rule B":"Deny-All-SQL (P:500)","Conflict":"A allows 1433, B denies — A wins (correct)","Status":"OK"},
            {"Rule A":"Allow-Internet-443 (P:200)","Rule B":"Deny-Outbound (P:65000)","Conflict":"Broad 443 may expose sandbox","Status":"⚠️ Review"},
            {"Rule A":"Allow-Informatica (P:200)","Rule B":"Allow-ADF (P:250)","Conflict":"Overlapping dest IPs","Status":"⚠️ Consolidate"},
        ]),use_container_width=True,hide_index=True)

elif page=="💰 AI#6: FinOps AI":
    st.subheader("💰 AI Feature #6 — FinOps AI Engine")
    st.markdown(f"{AI(6)} Cost anomalies, forecast, rightsizing, RI recommendations, orphan cleanup.",unsafe_allow_html=True)
    c1,c2,c3,c4=st.columns(4)
    with c1: st.markdown(K("Feb MTD","$68.4K","↓8%"),unsafe_allow_html=True)
    with c2: st.markdown(K("Forecast","$138K","Under ✓"),unsafe_allow_html=True)
    with c3: st.markdown(K("AI Savings","$12.8K/mo","Actionable"),unsafe_allow_html=True)
    with c4: st.markdown(K("Anomalies","2","1 open","down"),unsafe_allow_html=True)
    st.markdown("---")
    tab1,tab2,tab3=st.tabs(["📊 Cost","🤖 Recommendations","🚨 Anomalies"])
    with tab1:
        data=[{"Sub":s,"Svc":v,"Cost":round(random.uniform(1,20)*(3 if s=="Prod" else 1.5 if s=="Data" else 1),1)} for s in ["Prod","Dev","Data","Hub","Sandbox"] for v in ["Compute","DB","Storage","Network","AI"]]
        fig=px.bar(pd.DataFrame(data),x="Sub",y="Cost",color="Svc",color_discrete_sequence=["#0078D4","#5C2D91","#107C10","#D83B01","#B4009E"])
        fig.update_layout(height=300,margin=dict(l=0,r=0,t=10,b=0),plot_bgcolor="white",legend=dict(orientation="h",y=-0.2))
        st.plotly_chart(fig,use_container_width=True)
    with tab2:
        for save,act,cat in [("$4,200","Rightsize 6 VMs Dev/Test D4s→D2s (12% CPU)","Rightsizing"),("$3,100","Convert 3 Prod VMs to 1yr RI","RI"),("$2,800","Delete 4 orphaned disks Sandbox (30+ days)","Orphan"),("$1,500","Downgrade Dev SQL GP_Gen5_8→4 (40% DTU)","Rightsizing"),("$1,200","Auto-pause Synapse off-hours","Scheduling")]:
            st.markdown(f'<div class="ai-rec"><strong style="color:#15803D">{save}/mo</strong> — {act} <span style="color:#6B7280;font-size:11px">[{cat}]</span></div>',unsafe_allow_html=True)
    with tab3:
        st.markdown('<div class="ai-alert">🚨 <strong>Open:</strong> Data Platform +42% Feb 9 — Synapse 24hr (normally 8hr). Excess: $340. Root cause: pause job credential expired.</div>',unsafe_allow_html=True)
        st.markdown('<div class="ai-rec">✅ <strong>Resolved:</strong> Sandbox $0 Feb 7 — auto-cleanup per 14-day TTL. Expected.</div>',unsafe_allow_html=True)

elif page=="⚡ AI#7: Risk Scorer":
    st.subheader("⚡ AI Feature #7 — Risk Scorer + Auto-Approvals")
    st.markdown(f"{AI(7)} Every change scored 1-10. Low=auto-approve. Med/High=approval chain with SLA.",unsafe_allow_html=True)
    c1,c2,c3,c4=st.columns(4)
    with c1: st.markdown(K("Scored","523","Month"),unsafe_allow_html=True)
    with c2: st.markdown(K("Auto-Approved","387","74%"),unsafe_allow_html=True)
    with c3: st.markdown(K("Manual","136","26%"),unsafe_allow_html=True)
    with c4: st.markdown(K("Avg Time","1.8h","↓ from 18h"),unsafe_allow_html=True)
    st.markdown("---")
    col1,col2,col3=st.columns(3)
    with col1: st.markdown('<div style="background:#D1FAE5;border:2px solid #6EE7B7;border-radius:10px;padding:16px;text-align:center"><div style="font-size:24px;font-weight:700;color:#065F46">Low (1-3)</div><div style="color:#065F46;font-size:12px">Auto-Approved</div><div style="color:#6B7280;font-size:11px;margin-top:6px">Dev/Sandbox, Reader, tags, known templates</div></div>',unsafe_allow_html=True)
    with col2: st.markdown('<div style="background:#FEF3C7;border:2px solid #FCD34D;border-radius:10px;padding:16px;text-align:center"><div style="font-size:24px;font-weight:700;color:#92400E">Med (4-6)</div><div style="color:#92400E;font-size:12px">L1 Approval</div><div style="color:#6B7280;font-size:11px;margin-top:6px">Test, Contributor, FW rules</div></div>',unsafe_allow_html=True)
    with col3: st.markdown('<div style="background:#FEE2E2;border:2px solid #FCA5A5;border-radius:10px;padding:16px;text-align:center"><div style="font-size:24px;font-weight:700;color:#991B1B">High (7-10)</div><div style="color:#991B1B;font-size:12px">L1+L2+CISO</div><div style="color:#6B7280;font-size:11px;margin-top:6px">Prod, Owner, NSG 0.0.0.0/0, PE deletion</div></div>',unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("Pending Approvals")
    pending=[a for a in st.session_state.approvals if a["status"]=="Awaiting Approval"]
    if not pending: st.success("🎉 All clear!")
    for a in pending:
        ic="🔴" if a["risk_level"]=="High" else "🟡"
        with st.expander(f"{ic} {a['id']} — {a['desc']} (Score: {a['risk_score']}/10)",expanded=True):
            c1,c2=st.columns([3,2])
            with c1: st.markdown(f"**{a['req']}** | {a['type']} | {B(a['risk_level'])} | {a['risk_score']}/10",unsafe_allow_html=True)
            with c2: st.markdown(f'<div class="ai-warn">🤖 {a["ai_rec"]}</div>',unsafe_allow_html=True)
            ca,cb,cc=st.columns(3)
            if ca.button("✅ Approve",key=f"a_{a['id']}"): a["status"]="Approved";st.success("Pipeline triggered");st.rerun()
            if cb.button("❌ Reject",key=f"r_{a['id']}"): a["status"]="Rejected";st.rerun()
            if cc.button("💬 Info",key=f"i_{a['id']}"): st.info("Teams notification sent")
    st.markdown("---")
    st.dataframe(pd.DataFrame([
        {"ID":"REQ-089","Type":"VM Provision","Sub":"Dev","Score":"2.1","Level":"Low","Decision":"✅ Auto","Time":"<1min"},
        {"ID":"REQ-088","Type":"FW Rule","Sub":"Hub","Score":"5.8","Level":"Med","Decision":"✅ L1","Time":"42min"},
        {"ID":"REQ-087","Type":"Owner PIM","Sub":"Prod","Score":"9.1","Level":"High","Decision":"✅ L1+L2+CISO","Time":"6.2hr"},
        {"ID":"REQ-085","Type":"NSG 0.0.0.0/0","Sub":"Prod","Score":"9.8","Level":"High","Decision":"❌ AI Rejected","Time":"Instant"},
    ]),use_container_width=True,hide_index=True)

elif page=="📋 Compliance & Audit":
    st.subheader("📋 Compliance & Audit")
    c1,c2,c3,c4=st.columns(4)
    with c1: st.markdown(K("Score","96.2%","↑1.4%"),unsafe_allow_html=True)
    with c2: st.markdown(K("Violations","7","↓3"),unsafe_allow_html=True)
    with c3: st.markdown(K("Resources","847","100%"),unsafe_allow_html=True)
    with c4: st.markdown(K("Remediated","12","Month"),unsafe_allow_html=True)
    st.markdown("---")
    col1,col2=st.columns([2,1])
    with col1:
        cats=["Network","Identity","Data","Compute","Logging","Tagging"];scores=[98,94,97,95,100,92]
        fig=go.Figure(go.Bar(x=scores,y=cats,orientation="h",marker_color=["#107C10" if s>=95 else "#FFB900" for s in scores],text=[f"{s}%" for s in scores],textposition="outside"))
        fig.update_layout(height=240,margin=dict(l=0,r=40,t=10,b=0),plot_bgcolor="white",xaxis=dict(range=[80,105]),yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig,use_container_width=True)
    with col2:
        for s,i,sub in [("🔴","2 Storage public access","Dev/Test"),("🟡","3 VMs no diagnostics","Sandbox"),("🟡","1 NSG SSH open","Dev/Test"),("🟢","1 missing tag","Data")]:
            st.markdown(f"{s} **{sub}**: {i}")
    st.markdown("---")
    actions=["Role assigned","Resource deployed","FW rule added","PIM activated","AI risk scored","Drift detected","Access approved"]
    actors=["Ajit P.","Sarah K.","System","AI-AutoRemediation","AI-RiskScorer"]
    events=[{"Time":(datetime.datetime.now()-datetime.timedelta(hours=random.randint(1,168))).strftime("%m-%d %H:%M"),"Action":random.choice(actions),"Actor":random.choice(actors),"Sub":random.choice(["Prod","Dev","Hub","Data"]),"Result":random.choice(["Success"]*4+["Denied"])} for _ in range(20)]
    st.dataframe(pd.DataFrame(sorted(events,key=lambda x:x["Time"],reverse=True)),use_container_width=True,hide_index=True)
