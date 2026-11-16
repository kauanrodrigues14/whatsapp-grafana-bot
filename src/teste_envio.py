import os

from pathlib import Path
from dotenv import load_dotenv
from whatsapp import WhatsAppError, enviar_imagem

load_dotenv()

URL = os.getenv("EVOLUTION_URL", "http://localhost:8080")
API_KEY = os.getenv("EVOLUTION_API_KEY")
INSTANCIA = os.getenv("EVOLUTIN_INSTANCE")  
DESTINO = os.getenv("WHATSAPP_DESTINO")

imagem = Path("output")/"01+fid-geral.png"

try:
    enviar_imagem(URL, API_KEY, INSTANCIA, DESTINO, imagem, "1 Grafana - FID Geral")
    print("Enviado com sucesso")
except WhatsAppError as e:
    print(f"Falha")