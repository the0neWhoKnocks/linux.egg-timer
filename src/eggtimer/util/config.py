import json
from pathlib import Path

from platformdirs import user_config_path


class Config:
    def __init__(self, name: str) -> None:
        self.dir = user_config_path(name)
        self.file = self.dir / "config.json"
        self.data = {}
        self.load()
    
    def load(self) -> None:
        if self.file.is_file():
            with open(self.file, encoding="utf-8") as file:
                self.data = json.load(file)
        else:
            self.save()

    def save(self) -> None:
        if not self.dir.is_dir():
            Path(self.dir).mkdir(parents=True, exist_ok=True)
        
        with open(self.file, mode="w", encoding="utf-8") as file:
            json.dump(self.data, file, sort_keys=True, indent=2)
