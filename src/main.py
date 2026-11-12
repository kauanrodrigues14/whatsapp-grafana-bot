import os

from pathlib import Path

from dotenv import load_dotenv
from grafana import GrafanaError, capturar_painel

load_dotenv()

BASE_URL = os.getenv("GRAFANA_URL", "http://localhost:3000")
TOKEN = os.getenv("GRAFANA_TOKEN")

PAINEIS = [
    {"nome":"fid-geral","uid":"katkfng", "slug":"fid-geral", "panel_id": 1}, 
    {"nome":"apis","uid":"kag9dcv", "slug":"apis","panel_id": 1}, 
]

for i, p in enumerate(PAINEIS, start= 1):
    destino = Path("output") / f"{i:02d}+{p['nome']}.png"
    try: 
        capturar_painel(BASE_URL, TOKEN, p["uid"], p["slug"], p["panel_id"], destino)
        print (f"OK {destino} ({destino.stat().st_size / 1024:.0f}KB)")
    except GrafanaError as e :
        print(f"Falhou {p["nome"]}: {e}")