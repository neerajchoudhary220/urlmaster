from pathlib import Path
from services.gitoperations import get_git_branches
from services.herd import get_herd_link

def getDirectoriesList(path: str):
    parent_dir = Path(path)
    directories = []
    
    for d in parent_dir.iterdir():
        if d.is_dir():
            sub_dir_path = str(d)
            directories.append({
                "name": d.name,
                "path": sub_dir_path,
                "git_branches": get_git_branches(sub_dir_path),
                "herd_link":get_herd_link(sub_dir_path)
            })
    
    return {"directories": directories}

# def generateUrl(path:str):
#     path = Path(path)
    