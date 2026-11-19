import base64
from pathlib import Path

import requests

class WhatsAppError(Exception):
    """ Falha ao enviar pelo Whatsapp"""
    

def enviar_imagem(
    base_url: str,
    api_key: str,
    instancia: str,
    destino:  str,
    caminho: Path,
    legenda: str,
    timeout: int = 60,    
) -> None:
    """Envia imagem com legenada """
    url = f"{base_url.rstrip('/')}/message/sendMedia/{instancia}"
    headers =  {"apikey": api_key}
    imagem_b64 = base64.b64encode(caminho.read_bytes()).decode("ascii")
    payload = {
        "number": destino,
        "mediatype": "image",
        "mimetype": "image/png",
        "caption": legenda,
        "media": imagem_b64,
        "fileName": caminho.name,
        "filename": caminho.name,
    }
    
    
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=timeout)
    except requests.exceptions.Timeout as e:
        raise WhatsAppError("Tempo esgotado") from e
    except requests.exceptions.ConnectionError as e:
        raise WhatsAppError(f" Não consegui conectar em {base_url}. A Evolution está no ar?")
    
    if resp.status_code not in (200, 201):
        raise WhatsAppError(f"HTTP {resp.status_code} ao enviar '{legenda}': {resp.text[:300]}")
        
    
    
    