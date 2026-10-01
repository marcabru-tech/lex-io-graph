"""
updater.py — Atualiza o radar legislativo do Lex-IO-Graph.

Chamado pelo GitHub Actions (.github/workflows/update-radar.yml), toda segunda 09h BRT.
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

FONTES = ("senado", "camara", "lexml")

# Estado declarado de cada coletor. Mudar aqui quando um coletor for
# desligado ou religado em lib/radar.py, para que o snapshot diga a verdade.
ESTADO_FONTES = {
    "senado": "parcial",      # API ignora palavra-chave; filtro local sobre ~564 itens
    "camara": "ativa",
    "lexml": "desativada",    # verificacao anti-bot desde ago/2026
}


def montar_proveniencia(radar: dict, coletados: dict, preservados: dict) -> dict:
    """
    Proveniencia do snapshot (ADR 006): quem coletou, quando, o que cada
    fonte respondeu e o que foi herdado do snapshot anterior. O hash cobre
    o conteudo dos temas, para que duas coletas identicas sejam reconheciveis.
    """
    import hashlib
    import os

    run_id = os.environ.get("GITHUB_RUN_ID")
    repo = os.environ.get("GITHUB_REPOSITORY")
    conteudo = json.dumps(radar.get("temas", {}), ensure_ascii=False, sort_keys=True)
    return {
        "coletado_em": radar.get("ultima_atualizacao"),
        "executor": "github-actions" if os.environ.get("GITHUB_ACTIONS") else "local",
        "execucao_url": f"https://github.com/{repo}/actions/runs/{run_id}" if run_id and repo else None,
        "sha256_temas": hashlib.sha256(conteudo.encode("utf-8")).hexdigest(),
        "fontes": {
            f: {
                "estado": ESTADO_FONTES.get(f, "desconhecido"),
                "itens_coletados": coletados.get(f, 0),
                "temas_herdados_do_snapshot_anterior": sorted(preservados.get(f, [])),
            }
            for f in FONTES
        },
    }


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

    # Falha de rede nao e ausencia de norma. A blindagem e POR FONTE:
    # se o Senado respondeu e a Camara nao (caso tipico quando o robo roda
    # fora do Brasil), a lista da Camara anterior e preservada em vez de
    # ser apagada. Antes a regra era por tema e deixava passar esse caso.
    # Contagem coletada ANTES da blindagem: e o que a fonte respondeu de fato.
    _coletados = {
        f: sum(len(d.get(f, [])) for t, d in radar_novo.get("temas", {}).items() if t in TEMAS_RADAR)
        for f in FONTES
    }
    _preservados = {f: [] for f in FONTES}

    for _tema, _antes in radar_anterior.get("temas", {}).items():
        if _tema not in radar_novo.get("temas", {}):
            continue
        _agora = radar_novo["temas"][_tema]
        for _fonte in FONTES:
            _n_antes = len(_antes.get(_fonte, []))
            if _n_antes > 0 and not _agora.get(_fonte):
                _agora[_fonte] = _antes[_fonte]
                if _tema in TEMAS_RADAR:
                    _preservados[_fonte].append(_tema)
                print(f"  [preservado] {_fonte} vazio nesta coleta, mantido anterior: {_tema} ({_n_antes} itens)")

    # Saneamento: item sem id nao identifica proposicao (resposta da API em
    # formato inesperado). Remove de todas as fontes antes de salvar.
    _descartados = 0
    for _dados in radar_novo.get("temas", {}).values():
        for _f in ("senado", "camara", "lexml"):
            _antes = _dados.get(_f, [])
            _dados[_f] = [i for i in _antes if str(i.get("id", "")).strip()]
            _descartados += len(_antes) - len(_dados[_f])
    if _descartados:
        print(f"  [saneamento] {_descartados} item(ns) sem id descartado(s)")

    novidades = detectar_novidades(radar_novo, radar_anterior)

    # Proposicao que ja virou no do grafo (ou originou uma norma do corpus)
    # nao e novidade para a curadoria.
    try:
        from lib.taxonomia import indice_corpus, norma_no_corpus
        with open(DATA_DIR / "normas.json", encoding="utf-8") as _f:
            _idx = indice_corpus(json.load(_f)["nodes"])
        _antes = len(novidades)
        novidades = [n for n in novidades if not norma_no_corpus(n, _idx)]
        if _antes != len(novidades):
            print(f"  [corpus] {_antes - len(novidades)} novidade(s) ja presentes no grafo")
    except Exception as _e:
        print(f"  [corpus] verificacao ignorada: {_e}")
    radar_novo["proveniencia"] = montar_proveniencia(radar_novo, _coletados, _preservados)
    salvar_radar(radar_novo, novidades)

    # Exit code 0 = sucesso, mesmo sem novidades
    sys.exit(0)


if __name__ == "__main__":
    main()
