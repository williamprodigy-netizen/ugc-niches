# Reads the creators Sheet -> rebuilds the 3 niche pages -> commits + pushes live.
import json, subprocess, re
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
creds=Credentials.from_authorized_user_file(str(Path.home()/".gdocs_creds/biz_cockpit_token.json"),["https://www.googleapis.com/auth/spreadsheets"])
if creds.expired and creds.refresh_token: creds.refresh(Request())
svc=build("sheets","v4",credentials=creds)
SID=open("creators_sheet_url.txt").read().strip().split("/d/")[1].split("/")[0]
vals=svc.spreadsheets().values().get(spreadsheetId=SID,range="Creators!A2:E100").execute().get("values",[])
META={
 "beauty":{"title":"Beauty &amp; Fashion UGC","accent":"#db2777","eyebrow":"Beauty &amp; Fashion","lede":"Beauty and fashion brands pay real, relatable creators to make short phone videos. See the ones getting paid in this niche."},
 "lifestyle":{"title":"Travel, Lifestyle &amp; Wellness UGC","accent":"#0d9488","eyebrow":"Travel &middot; Lifestyle &middot; Wellness","lede":"Travel, lifestyle and wellness brands pay creators to show real life, real routines, real places. See who is getting paid here."},
 "tech":{"title":"Tech UGC","accent":"#2563eb","eyebrow":"AI Apps &amp; Software","lede":"Brands like Perplexity, Adobe and Cluely pay creators to make honest videos about their apps. No following needed. See the creators doing it."},
}
buckets={k:[] for k in META}
for row in vals:
    row=(row+["","","","",""])[:5]
    niche=row[0].strip().lower(); name=row[1].strip()
    if niche not in META or not name: continue
    buckets[niche].append({"name":name,"portfolio":row[2].strip(),"ig":row[3].strip().lstrip("@"),"youtube":row[4].strip()})
# import the page() builder from gen.py by exec
g=open("gen.py").read()
# reuse page() defn: exec gen.py's function only
ns={}
exec(g.split("NICHES=")[0]+"\n"+g.split("def page",1)[1].join(["def page","",]) if False else g[:g.index("for slug")], ns)  # loads CREATOR_ALL,REG,page
page=ns["page"]
for slug,meta in META.items():
    meta2=dict(meta); meta2["creators"]=buckets[slug] or [{"name":"[ add creator ]","portfolio":"","ig":"","youtube":""}]
    open(f"{slug}.html","w").write(page(slug,meta2))
    print(slug, "->", len(buckets[slug]), "creators")
subprocess.run(["git","add","-A"]); subprocess.run(["git","commit","-q","-m","sync creators from sheet"])
subprocess.run(["git","push","-q","origin","master"])
print("pushed live")
