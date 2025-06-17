from pathlib import Path
from services.gitoperations import get_git_branches
from services.herd import get_herd_link
from services.cloudflared import get_tunnel

def getDirectoriesList(path: str):
    parent_dir = Path(path)
    directories = []
    
    for d in parent_dir.iterdir():
        if d.is_dir():
            sub_dir_path = str(d)
            herd_link = get_herd_link(sub_dir_path)
            directories.append({
                "name": d.name,
                "path": sub_dir_path,
                "git_branches": get_git_branches(sub_dir_path),
                "herd_link":herd_link,
                "public_url":get_tunnel(herd_link)
            })
    
    return {"directories": directories}

# def generateUrl(path:str):
#     path = Path(path)
    