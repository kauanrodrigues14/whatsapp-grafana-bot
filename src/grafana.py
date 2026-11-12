from pathlib import Path

import requests

class GrafanaError(Exception):
    """Falha ao capturar um painel do Grafana."""
    

def capturar_painel(
    base_url: str,
    token: str,
    uid: str,
    slug: str,
    painel_id: int,
    destino: Path,
    periodo_de: str = "now-6h",
    periodo_ate: str = "now",
    largura:int = 1200,
    altura: int = 600,
    tz: str = "America/Sao_Paulo",
    timeout: int = 60,    
) -> Path: 
    url = f"{base_url.rstrip('/')}/render/d/{uid}/{slug}"
    params = {
        
        "orgId": 1,
        "panelId":painel_id,
        "width": largura,
        "height": altura,
        "from": periodo_de,
        "to": periodo_ate,
        "tz":tz,
        "timeout": timeout, 
    }
    headers = {"Authorization": f"Bearer {token}"}
    
    try: 
        resp = requests.get(url, headers=headers, params=params, timeout=timeout +15)
    except requests.exceptions.Timeout as e:
        raise GrafanaError(f"Tempo esgotado ao renderizar painel {uid}/{painel_id}") from e
    except requests.exceptions.ConnectionError as e:
        raise GrafanaError (f" Nao consegui encontrar em {base_url}") from e
    if resp.status_code != 200:
        raise GrafanaError (f" HTTP {resp.status_code} ao renderizar {uid}/{painel_id}: {resp.text[:200]}")
    if "image/png" not in resp.headers.get("Content-Type",""):
         raise GrafanaError (f" Nao e uma imagem PNG{resp.text[:200]}")
    if len (resp.content) < 1000:
        raise GrafanaError(f"A imagem com menso de 1kb")
    
    destino.parent.mkdir(parents=True, exist_ok= True)
    destino.write_bytes(resp.content)
    return destino