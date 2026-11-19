import os

from dataclasses import dataclass, field    
from pathlib import Path

import yaml
from dotenv import load_dotenv




class ConfigError(Exception):
    """ Config ausente ou invalida"""
    
@dataclass (frozen=True)

class Painel:
    ordem: int
    legenda: str
    uid: str 
    slug: str
    panel_id: str
    
    @property
    def legenda_completa(self)-> str:
           """ Legenda enviada com sucesso"""
           return f"{self.ordem}{self.legenda}" 
       
@dataclass(frozen=True)
class Config:
    grafana_url: str
    grafana_token: str = field(repr=False)
    evolution_url: str
    evolution_api_key: str = field(repr=False)
    evolution_instance: str
    destino: str
    periodo_de: str
    periodo_ate: str
    pausa: float
    paineis: list[Painel]
    
    
def _obrigatoria(nome:str) -> str:
    valor = os.environ.get(nome, "").strip()
    if not valor: 
        raise ConfigError(f"Variavel {nome} ")
    return valor

def carregar_config(caminho_yaml: Path = Path("config/paineis.yaml")) -> Config:
    load_dotenv(override=True)
    
    if not caminho_yaml.exists():
        raise ConfigError(f"Arquivo {caminho_yaml} não encontrado (rode na raiz do projeto)")

    with caminho_yaml.open(encoding="utf-8") as f:
        dados = yaml.safe_load(f)

    if not isinstance(dados, dict):
        raise ConfigError(f"{caminho_yaml} está vazio ou mal formatado")
    
    paineis = []
    for item in dados.get("paineis") or []:
        try:
            paineis.append(
                Painel(
                    ordem=int(item["ordem"]),
                    legenda=str(item["legenda"]),
                    uid=str(item["uid"]),
                    slug=str(item["slug"]),
                    panel_id=int(item["panel_id"])
                )
            )        
        except (KeyError, TypeError, ValueError) as e:
            raise ConfigError(f"Painel inválido no YAML ({e!r}): {item}") from e

    if not paineis:
        raise ConfigError("Nenhum painel encontrado em paineis.yaml")
    
    paineis.sort(key=lambda p: p.ordem)
    periodo = dados.get("periodo") or {}
    
    return Config(
        grafana_url=os.environ.get("GRAFANA_URL", "http://localhost:3000"),
        grafana_token=_obrigatoria("GRAFANA_TOKEN"),
        evolution_url=os.environ.get("EVOLUTION_URL", "http://localhost:8080"),
        evolution_api_key=_obrigatoria("EVOLUTION_API_KEY"),
        evolution_instance=_obrigatoria("EVOLUTION_INSTANCE"),
        destino= _obrigatoria("WHATSAPP_DESTINO"),
        periodo_de=str(periodo.get("de", "now-6h")),
        periodo_ate=str(periodo.get("ate", "now")),
        pausa=float(dados.get("pausa_entre_envios", 3)),
        paineis=paineis,
    )