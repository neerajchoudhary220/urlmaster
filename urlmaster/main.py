from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,validator
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from urlmaster.services.directory import getDirectoriesList,cloneDirectory,open_directory,addParentDirectory
from urlmaster.services.gitoperations import switch_branch
from urlmaster.services.herd import link_with_herd
from urlmaster.services.cloudflared import get_cloudflared_public_url,kill_tunnel_by_url,replace_env_values
import os
app = FastAPI()
# public_dir = Path(__file__).resolve().parent / "public"
# app.mount("/", StaticFiles(directory=public_dir, html=True), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def raiseError(msg:str):
    raise HTTPException(status_code=400,detail=msg)

 
class DirectoryPath(BaseModel):
    path: str
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
def set_parent_directory(directory: DirectoryPath):
    addParentDirectory(directory.path)
    return {"msg":"Added Parent Directory Successfully!"}

@app.get('/directory/')
def get_branch_listing():
    return {"data":getDirectoriesList()}

@app.get('/directory/clone/')
def clone_directory(directory_path:str, new_folder_name:str):
    cloneDirectory(directory_path,new_folder_name)
    return {'msg':'Clone successfully'}

@app.get('/directory/open/')
def open_directory_by_path(path:str):
    open_directory(path)
    return {'msg':'Opened'}
    
@app.get('/git/switch/')
def git_switch_branch(path,branch):
    msg = switch_branch(path,branch)
    return {"msg":msg}
    
    
@app.get('/herd/')
def add_herd_link(directory_path:str):
    link_with_herd(Path(directory_path))
    return {'msg':"New link has been created"}

@app.get('/cloudflared/')
def add_herd_link(herd_link:str,dir_path:str):
    if not os.path.exists(dir_path):
        raiseError("Invalid Directory Path")
        
    public_url = get_cloudflared_public_url(herd_link)
    replace_env_values(dir_path,public_url)
    return {'msg':'Public URL generated successfully','public_url':public_url}

@app.delete('/cloudflared/')
def delete_cloudflared_tunnel(herd_link:str):
    kill_tunnel_by_url(herd_link)
    return {"msg":"Dleted Public URL successfully"}
    
    
    
    