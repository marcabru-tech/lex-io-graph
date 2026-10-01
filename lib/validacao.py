"""
Validação de integridade do corpus e dos dados derivados.

Regra de arquitetura: o corpus (normas.json + arestas.json) é a fonte de
verdade. Tudo que cita uma norma por id — teoria, radar, arestas — precisa
apontar para um nó existente ou para uma referência externa declarada em
data/referencias_externas.json.

Uso:
    python -m lib.validacao            # valida tudo
    python -m lib.validacao --radar    # só o snapshot do radar (usado pelo workflow)

Retorna código 1 se houver erro, para que o CI e o workflow do radar parem.
Sem dependências além da biblioteca padrão: roda no runner do radar, que só
instala `requests`.
"""

import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DATA = RAIZ / "data"
TEORIA_HTML = RAIZ / "docs" / "teoria-conjuntos-juridicos-v3.html"

CAMPOS_NORMA = ("id", "nome", "sigla", "tipo", "ementa", "status", "temas", "orgao", "ano")
CAMPOS_ARESTA = ("source", "target", "tipo")
FONTES_RADAR = ("senado", "camara", "lexml")

_TAG_TEORIA = re.compile(r'int-norma-tag">([^<]+)<')


def _ler(nome: str) -> dict:
    with open(DATA / nome, encoding="utf-8") as f:
        return json.load(f)


def ids_externos() -> dict[str, dict]:
    p = DATA / "referencias_externas.json"
    if not p.exists():
        return {}
    return _ler("referencias_externas.json").get("referencias", {})


def ids_citados_na_teoria(html: str | None = None) -> set[str]:
    if html is None:
        html = TEORIA_HTML.read_text(encoding="utf-8")
    return {t.strip() for t in _TAG_TEORIA.findall(html)}


def validar_corpus() -> list[str]:
    from lib.constants import THEMES, STATUS_LABELS

    erros = []
    normas = _ler("normas.json")["nodes"]
    arestas = _ler("arestas.json")["edges"]

    ids = [n.get("id") for n in normas]
    duplicados = {i for i in ids if ids.count(i) > 1}
    if duplicados:
        erros.append(f"normas.json: ids duplicados {sorted(duplicados)}")
    ids = set(ids)

    for n in normas:
        for c in CAMPOS_NORMA:
            if c not in n:
                erros.append(f"normas.json [{n.get('id')}]: campo obrigatório ausente '{c}'")
        if n.get("status") not in STATUS_LABELS:
            erros.append(f"normas.json [{n.get('id')}]: status desconhecido '{n.get('status')}'")
        for t in n.get("temas") or []:
            if t not in THEMES:
                erros.append(f"normas.json [{n.get('id')}]: tema desconhecido '{t}'")

    for i, e in enumerate(arestas):
        for c in CAMPOS_ARESTA:
            if c not in e:
                erros.append(f"arestas.json #{i}: campo obrigatório ausente '{c}'")
        for lado in ("source", "target"):
            if e.get(lado) and e[lado] not in ids:
                erros.append(f"arestas.json #{i}: {lado} '{e[lado]}' não existe no corpus")

    externos = ids_externos()
    sobrepostos = ids & set(externos)
    if sobrepostos:
        erros.append(f"referencias_externas.json: ids que já são nós do corpus {sorted(sobrepostos)}")

    fantasmas = ids_citados_na_teoria() - ids - set(externos)
    if fantasmas:
        erros.append(
            "teoria: ids citados que não estão no corpus nem em referencias_externas.json "
            f"{sorted(fantasmas)}"
        )
    return erros


def validar_radar(radar: dict | None = None) -> list[str]:
    erros = []
    if radar is None:
        radar = _ler("radar_legislativo.json")
    if not radar.get("ultima_atualizacao"):
        erros.append("radar: 'ultima_atualizacao' ausente")
    temas = radar.get("temas")
    if not isinstance(temas, dict) or not temas:
        erros.append("radar: 'temas' ausente ou vazio")
        return erros
    total = 0
    for tema, dados in temas.items():
        for f in FONTES_RADAR:
            itens = dados.get(f, [])
            if not isinstance(itens, list):
                erros.append(f"radar [{tema}]: fonte '{f}' não é lista")
                continue
            for it in itens:
                if not str(it.get("id", "")).strip():
                    erros.append(f"radar [{tema}/{f}]: item sem id")
            total += len(itens)
    if total == 0:
        erros.append("radar: nenhum item em nenhuma fonte (coleta vazia não substitui snapshot)")
    return erros


def main(argv: list[str]) -> int:
    sys.path.insert(0, str(RAIZ))
    erros = validar_radar() if "--radar" in argv else validar_corpus() + validar_radar()
    if erros:
        print(f"✗ {len(erros)} erro(s) de integridade:")
        for e in erros:
            print(f"  - {e}")
        return 1
    print("✓ Integridade OK")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
