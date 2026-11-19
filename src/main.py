import sys
import time
from pathlib import Path

from config import Config, ConfigError, Painel, carregar_config
from grafana import GrafanaError, capturar_painel
from whatsapp import WhatsAppError, enviar_imagem


PASTA_SAIDA = Path("output")

def processar_painel(cfg:Config, painel: Painel ) -> None:
    """ Captura"""
    arquivo = PASTA_SAIDA / f"{painel.ordem:02d}_{painel.slug}.png"
    try:
        capturar_painel(
            cfg.grafana_url,
            cfg.grafana_token,
            painel.uid,
            painel.slug,
            painel.panel_id,
            arquivo,
            periodo_de=cfg.periodo_de,
            periodo_ate=cfg.periodo_ate,
        )
        enviar_imagem(
            cfg.evolution_url,
            cfg.evolution_api_key,
            cfg.evolution_instance,
            cfg.destino,
            arquivo,
            painel.legenda_completa,
        )
    finally:
        arquivo.unlink(missing_ok=True)
        
        
def main():
    try:
        cfg = carregar_config()
    except ConfigError as e:
        print(f"Erro de configuracao{e}")
        return 2 
    
    falhas = []
    
    for i, painel in enumerate(cfg.paineis):
        if i > 0:
            time.sleep(cfg.pausa)
        try:
            processar_painel(cfg, painel)
            print(f"OK     {painel.legenda_completa}")
        except (GrafanaError, WhatsAppError) as e:
            falhas.append(painel.legenda_completa)
            print(f"FALHOU {painel.legenda_completa}: {e}")

    enviados = len(cfg.paineis) - len(falhas)
    print(f"\nConcluído: {enviados} enviado(s), {len(falhas)} falha(s)")
    return 1 if falhas else 0

if __name__ == "__main__":
    sys.exit(main())
    
