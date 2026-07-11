from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
creds=Credentials.from_authorized_user_file(str(Path.home()/".gdocs_creds/biz_cockpit_token.json"),["https://www.googleapis.com/auth/spreadsheets"])
if creds.expired and creds.refresh_token: creds.refresh(Request())
svc=build("sheets","v4",credentials=creds)
HDR=["Niche (beauty / lifestyle / tech)","Creator Name","Portfolio URL","Instagram handle (no @)","YouTube URL (optional)"]
rows=[HDR]
def r(niche,name="",pf="",ig="",yt=""): return [niche,name,pf,ig,yt]
# tech (have 2)
rows.append(r("tech","Andrea B","","ugcbyandreab",""))
rows.append(r("tech","Stacy Parks","","stacyparks.ugc",""))
for _ in range(3): rows.append(r("tech"))
# lifestyle (have 1)
rows.append(r("lifestyle","Angela Recine","https://angelarecine.my.canva.site/","angelar.fit","https://www.youtube.com/watch?v=RIo2zNt-7wE&t=5s"))
for _ in range(4): rows.append(r("lifestyle"))
# beauty (have 0)
for _ in range(5): rows.append(r("beauty"))
ss=svc.spreadsheets().create(body={"properties":{"title":"UGC Niche Pages — Creators (fill me)"},
  "sheets":[{"properties":{"title":"Creators","gridProperties":{"frozenRowCount":1}}}]}).execute()
sid=ss["spreadsheetId"]; gid=ss["sheets"][0]["properties"]["sheetId"]
svc.spreadsheets().values().update(spreadsheetId=sid,range="Creators!A1",valueInputOption="RAW",body={"values":rows}).execute()
svc.spreadsheets().batchUpdate(spreadsheetId=sid,body={"requests":[
 {"repeatCell":{"range":{"sheetId":gid,"startRowIndex":0,"endRowIndex":1},"cell":{"userEnteredFormat":{"backgroundColor":{"red":0.11,"green":0.14,"blue":0.2},"textFormat":{"foregroundColor":{"red":1,"green":1,"blue":1},"bold":True},"wrapStrategy":"WRAP"}},"fields":"userEnteredFormat"}},
 {"updateDimensionProperties":{"range":{"sheetId":gid,"dimension":"COLUMNS","startIndex":1,"endIndex":5},"properties":{"pixelSize":230},"fields":"pixelSize"}},
 # color rows by niche is manual; just tint the have-so-far rows green
 {"repeatCell":{"range":{"sheetId":gid,"startRowIndex":1,"endRowIndex":3},"cell":{"userEnteredFormat":{"backgroundColor":{"red":0.9,"green":0.97,"blue":0.9}}},"fields":"userEnteredFormat.backgroundColor"}},
 {"repeatCell":{"range":{"sheetId":gid,"startRowIndex":6,"endRowIndex":7},"cell":{"userEnteredFormat":{"backgroundColor":{"red":0.9,"green":0.97,"blue":0.9}}},"fields":"userEnteredFormat.backgroundColor"}},
]}).execute()
url=f"https://docs.google.com/spreadsheets/d/{sid}/edit"
open("creators_sheet_url.txt","w").write(url); print(url)
