from pathlib import Path
from services.gitoperations import get_git_branches
from services.herd import get_herd_link
from services.cloudflared import get_tunnel
from fastapi import HTTPException
import shutil
import json
import platform
import subprocess
import os


def getParentDirectory():
    with open("data.json") as f:
        data = json.load(f)
    return data.get('parent_directory')

def getDirectoriesList():
    parent_dir = Path(getParentDirectory())
    directories = []
    
    for d in parent_dir.iterdir():
        if d.is_dir():
            sub_dir_path = str(d)
            herd_link = get_herd_link(sub_dir_path)
            directories.append({
                "name": d.name,
                "parent_dir":parent_dir,
                "path": sub_dir_path,
                "git_branches": get_git_branches(sub_dir_path),
                "herd_link":herd_link,
                "public_url":get_tunnel(herd_link)
            })
    
    return {"directories": directories}




def cloneDirectory(path: str, new_directory_name: str):
    source_path = Path(path)
    destination_path = Path(getParentDirectory()) / new_directory_name

    if destination_path.exists():
        raise HTTPException(status_code=400, detail=f"This directory '{destination_path}' already exists!")

    if not source_path.is_dir():
        raise HTTPException(status_code=400, detail=f"Source directory '{source_path}' does not exist!")

    shutil.copytree(source_path, destination_path)
    return f"Directory cloned to {destination_path}"

def open_directory(path: str):
    path = Path(path).expanduser().resolve()

    if not path.is_dir():
        raise HTTPException(400,detail=f"Error: '{path}' is not a valid directory.")
        return

    system_name = platform.system()

    try:
        if system_name == "Windows":
            # Works only on Windows
            os.startfile(path)
        elif system_name == "Darwin":  # macOS
            subprocess.run(["open", str(path)])
        else:  # Linux and other Unix-like systems
            subprocess.run(["xdg-open", str(path)])
        print(f"Opened directory: {path}")
    except Exception as e:
       raise HTTPException(400,"Invalid action!")
        

