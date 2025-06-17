from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import List
from config.database import init_db,get_connection
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from services.directory import getDirectoriesList
from services.gitoperations import switch_branch
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
    
    
    
    