from pathlib import Path
from services.gitoperations import get_git_branches
def getDirectoriesList(path: str):
    parent_dir = Path(path)
    directories = []
    
    for d in parent_dir.iterdir():
        if d.is_dir():
            directories.append({
                "name": d.name,
                "path": str(d),
                "git_branches": get_git_branches(str(d))
            })
    
    return {"directories": directories}

# def generateUrl(path:str):
#     path = Path(path)
    