import requests
from pathlib import Path


def download_to_local(url:str, dest_path:Path, parent_mkdir:bool=True):
    if not isinstance(dest_path, Path):
        raise ValueError(f"{dest_path} should be valid pathlib Path object")
    
    if parent_mkdir:
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            response = requests.get(url)
            response.raise_for_status()
            dest_path.write_bytes(response.content)
            return True
        except requests.RequestException as e:
            print(f'Failed to download {url}: {e}')
            return False