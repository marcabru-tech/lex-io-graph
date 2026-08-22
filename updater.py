"""
updater.py — Atualiza o radar legislativo do Lex-IO-Graph.

Chamado pelo GitHub Action (.github/workflows/update-radar.yml).
Consulta APIs públicas via lib/radar.py e salva data/radar_legislativo.json.

Arquitetura:
  - Não modifica normas.json ou arestas.json automaticamente
  - Curadoria humana preservada: novos PLs detectados são alertas, não inserções
  - O curador (Guilherme) decide o que entra no grafo após revisão do radar
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Adicionar raiz ao path para importar lib/
sys.path.insert(0, str(Path(__file__).parent))

from lib.radar import coletar_radar, TEMAS_RADAR

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

RADAR_PATH = DATA_DIR / "radar_legislativo.json"


def carregar_radar_anterior() -> dict:
    """Carrega o radar anterior para comparação."""
    if RADAR_PATH.exists():
        try:
            with open(RADAR_PATH, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def detectar_novidades(radar_novo: dict, radar_anterior: dict) -> list[dict]:
    """
    Compara radares e detecta itens novos.
    Retorna lista de novidades para log.
    """
    novidades = []

    ids_anteriores = set()
    for tema_data in radar_anterior.get("temas", {}).values():
        for fonte in ["senado", "camara", "lexml"]:
            for item in tema_data.get(fonte, []):
                ids_anteriores.add(item.get("id", ""))

    for tema, tema_data in radar_novo.get("temas", {}).items():
        for fonte in ["senado", "camara", "lexml"]:
            for item in tema_data.get(fonte, []):
                if item.get("id", "") not in ids_anteriores and item.get("id", ""):
                    novidades.append({
                        "tema": tema,
                        "fonte": fonte,
                        "sigla": item.get("sigla", ""),
                        "ementa": item.get("ementa", ""),
                        "url": item.get("url", ""),
                        "data_deteccao": item.get("data_deteccao", ""),
                    })

    return novidades


def salvar_radar(radar: dict, novidades: list[dict]) -> None:
    """Salva radar com metadados de novidades."""
    radar["novidades_detectadas"] = novidades
    radar["total_novidades"] = len(novidades)

    with open(RADAR_PATH, "w", encoding="utf-8") as f:
        json.dump(radar, f, ensure_ascii=False, indent=2)

    print(f"\n✓ Radar salvo: {RADAR_PATH}")
    print(f"  Última atualização: {radar['ultima_atualizacao']}")
    print(f"  Novidades detectadas: {len(novidades)}")

    if novidades:
        print("\n📋 Novidades para revisão:")
        for n in novidades[:10]:
            print(f"  [{n['tema']}] {n['fonte']}: {n['sigla']}")
            print(f"    {n['ementa'][:80]}...")
            print(f"    URL: {n['url']}")


def main():
    print(f"[{datetime.now().isoformat()}] Iniciando radar legislativo...")
    print(f"Temas monitorados: {', '.join(TEMAS_RADAR.keys())}\n")

    radar_anterior = carregar_radar_anterior()
    anterior_data = radar_anterior.get("ultima_atualizacao", "nunca")
    print(f"Última execução: {anterior_data}\n")

    print("Coletando dados das APIs...\n")
    radar_novo = coletar_radar()

    # Temas fora de TEMAS_RADAR sao CURADOS: entram a mao e nao podem ser
    # sobrescritos pela coleta automatica. Principio de curadoria aplicado
    # a infraestrutura: o robo coleta, o curador decide o que permanece.
    for _tema, _dados in radar_anterior.get("temas", {}).items():
        if _tema not in TEMAS_RADAR:
            radar_novo["temas"][_tema] = _dados
            print(f"  [curado] tema preservado: {_tema}")

    novidades = detectar_novidades(radar_novo, radar_anterior)
    salvar_radar(radar_novo, novidades)

    # Exit code 0 = sucesso, mesmo sem novidades
    sys.exit(0)


if __name__ == "__main__":
    main()
