from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,validator
from typing import Optional
from config.database import init_db,get_connection
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from services.directory import getDirectoriesList
from services.gitoperations import switch_branch
from services.herd import link_with_herd
from services.cloudflared import get_cloudflared_public_url,kill_tunnel_by_url
app = FastAPI()
init_db() #Initialize Database

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def raiseError(msg:str):
    raise HTTPException(status_code=400,detail=msg)

 
class ParentDirectories(BaseModel):
    path: str
    status: bool
# class DirectoryPath(BaseModel):
#     path: str
#     @validator('path')
#     def check_path(cls, value: str) -> str:
#         p = Path(value)
#         if not p.exists() or not p.is_dir():
#             raise ValueError("Invalid directory path!")
#         return value
        
        
    
@app.get("/")
def read_root():
    return "working"

@app.post("/directory/")
def set_parent_directory(directory: ParentDirectories):
    path = Path(directory.path)
    if not path.exists() and not path.is_dir():
        raiseError("Invalid directory path!")
        
    conn = get_connection()
    cursor = conn.cursor()
    normalize_path = directory.path
    # Check if normalized name already exists (case-insensitive)
    cursor.execute("SELECT id FROM parent_directories WHERE path = ?", (normalize_path,))
    existing = cursor.fetchone()
    if existing:
        conn.close()
        raiseError("This name is already used.")

    # Insert normalized name
    q = "INSERT INTO parent_directories (path, status) VALUES (?, ?)"
    cursor.execute(q, (normalize_path, directory.status))
    conn.commit()
    directory_id = cursor.lastrowid
    conn.close()
    return {"id": directory_id, "path": normalize_path, "status": directory.status}

@app.get('/directory/')
def get_branch_listing():
    conn = get_connection()
    cursor = conn.cursor()
    q = """SELECT path FROM parent_directories WHERE status=1"""
    cursor.execute(q)
    row = cursor.fetchone()
    conn.close()
    if row:
        path = row[0]
        directories = getDirectoriesList(path)
        
        return {"data":directories}
    else:
        raiseError("Directories is not found!")

@app.get('/git/switch/')
def git_switch_branch(path,branch):
    msg = switch_branch(path,branch)
    return {"msg":msg}
    
    
@app.get('/herd/')
def add_herd_link(directory_path:str):
    link_with_herd(Path(directory_path))
    return {'msg':"New link has been created"}

@app.get('/cloudflared/')
def add_herd_link(herd_link:str):
    public_url = get_cloudflared_public_url(herd_link)
    return {'msg':'Public URL generated successfully','public_url':public_url}

@app.delete('/cloudflared/')
def delete_cloudflared_tunnel(herd_link:str):
    kill_tunnel_by_url(herd_link)
    return {"msg":"Dleted Public URL successfully"}
    
    
    
    