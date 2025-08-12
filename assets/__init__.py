import os
import base64
from pathlib import Path


class AssetManager(object):
    def __init__(self, base_dir: Path | None = None):
        if base_dir is None:
            base_dir = Path(__file__).parent
        
        self.base_dir = base_dir
        
    def get_encoded(self, category: str, filename: str, encoding:str = 'ascii'):
        path = self.base_dir / category / filename
        if not path.exists():
            raise FileExistsError(f"{filename} not found")
        with path.open("rb") as file:
            return base64.b64encode(file.read()).decode(encoding)