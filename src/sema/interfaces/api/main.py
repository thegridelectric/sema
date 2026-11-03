from pathlib import Path

import yaml
from fastapi import FastAPI

app = FastAPI()

# Load registry from YAML at startup
registry_path = Path("../type_definitions/registry.yaml")
with open(registry_path) as f:
    REGISTRY = yaml.safe_load(f)


@app.get("/types")
async def list_types():
    return REGISTRY["types"]
