"""LAN file transfer MVP. Run: pip install fastapi uvicorn python-multipart; uvicorn server:app --host 0.0.0.0"""
from fastapi import FastAPI,UploadFile,File,HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from uuid import uuid4
app=FastAPI(title="LAN File Transfer");ROOT=Path("shared");ROOT.mkdir(exist_ok=True);MAX=25*1024*1024
@app.get("/files")
def files():return [{"name":p.name,"bytes":p.stat().st_size} for p in ROOT.iterdir() if p.is_file()]
@app.post("/upload")
async def upload(file:UploadFile=File(...)):
 data=await file.read(MAX+1)
 if len(data)>MAX:raise HTTPException(413,"Maximum file size is 25 MB.")
 suffix=Path(file.filename or "upload.bin").suffix[:12];name=uuid4().hex+suffix;(ROOT/name).write_bytes(data)
 return {"id":name,"bytes":len(data),"download":f"/download/{name}"}
@app.get("/download/{file_id}")
def download(file_id:str):
 if not file_id.replace(".","").replace("-","").isalnum():raise HTTPException(400,"Invalid file id.")
 p=(ROOT/file_id).resolve()
 if p.parent!=ROOT.resolve() or not p.is_file():raise HTTPException(404,"File not found.")
 return FileResponse(p,filename=p.name)