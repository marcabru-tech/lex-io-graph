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


def ids_em_teoria_json() -> set[str]:
    """Todos os ids listados em 'exemplos_corpus' de data/teoria.json."""
    p = DATA / "teoria.json"
    if not p.exists():
        return set()
    achados: set[str] = set()

    def varrer(x):
        if isinstance(x, dict):
            for k, v in x.items():
                if k == "exemplos_corpus" and isinstance(v, list):
                    achados.update(v)
                else:
                    varrer(v)
        elif isinstance(x, list):
            for v in x:
                varrer(v)

    varrer(_ler("teoria.json"))
    return achados


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

    # Instrumento não incorporado não retira validade da CF nem fundamenta outra
    # norma: não pode participar de aresta de hierarquia.
    nao_incorporados = {n["id"] for n in normas if n.get("status") == "instrumento_externo"}
    for i, e in enumerate(arestas):
        if e.get("tipo") == "hierarquia" and {e.get("source"), e.get("target")} & nao_incorporados:
            erros.append(f"arestas.json #{i}: aresta de hierarquia com instrumento não incorporado "
                         f"({e.get('source')} → {e.get('target')})")

    externos = ids_externos()
    sobrepostos = ids & set(externos)
    if sobrepostos:
        erros.append(f"referencias_externas.json: ids que já são nós do corpus {sorted(sobrepostos)}")

    if (DATA / "teoria.json").exists():
        from lib.natureza import SELOS
        naturezas = set(re.findall(r'"natureza":\s*"([^"]+)"',
                                   (DATA / "teoria.json").read_text(encoding="utf-8")))
        if naturezas - set(SELOS):
            erros.append(f"teoria.json: natureza desconhecida {sorted(naturezas - set(SELOS))}")

    fantasmas = (ids_citados_na_teoria() | ids_em_teoria_json()) - ids - set(externos)
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


ESTADOS_VERIFICACAO = ("verificado", "pendente", "contestado")
CAMPOS_JURISPRUDENCIA_NOVOS = (
    "estado_verificacao", "fonte_oficial_url", "orgao_julgador", "relator",
    "data_julgamento", "data_publicacao", "nivel_autoridade", "proveniencia",
)
CAMPOS_PROVENIENCIA = ("origem", "data_consulta", "observacao")
EXIGIDOS_SE_VERIFICADO = (
    "fonte_oficial_url", "orgao_julgador", "relator", "data_julgamento",
)

_NUMERO_CNJ = re.compile(r"\b(\d{7})-(\d{2})\.(\d{4})\.(\d)\.(\d{2})\.(\d{4})\b")


def digito_cnj(sequencial: str, ano: str, segmento: str, tribunal: str, origem: str) -> int:
    """Dígito verificador do padrão CNJ: 98 − (NNNNNNNAAAAJTROOOO00 mod 97)."""
    return 98 - int(f"{sequencial}{ano}{segmento}{tribunal}{origem}00") % 97


def validar_jurisprudencia(juris: dict | None = None, normas: dict | None = None
                           ) -> tuple[list[str], list[str]]:
    """Valida data/jurisprudencia.json. Retorna (erros, advertencias).

    Erros bloqueiam; advertências não. Divergência de dígito CNJ é erro em
    registro verificado e advertência nos demais. As assimetrias entre
    jurisprudencia.json e normas.json são sempre advertências.
    """
    erros: list[str] = []
    avisos: list[str] = []
    registros = (juris if juris is not None else _ler("jurisprudencia.json"))["jurisprudencia"]
    nos = (normas if normas is not None else _ler("normas.json"))["nodes"]

    for r in registros:
        rid = r.get("id")
        pref = f"jurisprudencia.json [{rid}]"
        ausentes = [c for c in CAMPOS_JURISPRUDENCIA_NOVOS if c not in r]
        for c in ausentes:
            erros.append(f"{pref}: campo obrigatório ausente '{c}'")

        estado = r.get("estado_verificacao")
        if "estado_verificacao" in r and estado not in ESTADOS_VERIFICACAO:
            erros.append(f"{pref}: estado_verificacao inválido '{estado}'")

        prov = r.get("proveniencia")
        if "proveniencia" in r:
            if not isinstance(prov, dict):
                erros.append(f"{pref}: proveniencia deve ser objeto")
            else:
                for c in CAMPOS_PROVENIENCIA:
                    if c not in prov:
                        erros.append(f"{pref}: proveniencia sem '{c}'")

        if estado == "verificado":
            for c in EXIGIDOS_SE_VERIFICADO:
                if not r.get(c):
                    erros.append(f"{pref}: registro verificado exige '{c}' não nulo")
            if r.get("nivel_autoridade") in (None, "desconhecido"):
                erros.append(f"{pref}: registro verificado exige nivel_autoridade diferente de 'desconhecido'")

        for m in _NUMERO_CNJ.finditer(str(r.get("numero", ""))):
            seq, dv, ano, seg, tr, org = m.groups()
            esperado = digito_cnj(seq, ano, seg, tr, org)
            if int(dv) != esperado:
                msg = (f"{pref}: número '{m.group(0)}' com dígito verificador {dv} "
                       f"divergente do padrão CNJ (esperado {esperado:02d})")
                if estado == "verificado":
                    erros.append(msg)
                else:
                    avisos.append(msg + f" — registro {estado or 'sem estado'}, não bloqueante")

    ids_juris = {r.get("id") for r in registros}
    ids_nos = {n.get("id") for n in nos if n.get("tipo") == "jurisprudencia"}
    for i in sorted(ids_juris - ids_nos, key=str):
        avisos.append(f"assimetria: registro de jurisprudência '{i}' sem nó em normas.json")
    for i in sorted(ids_nos - ids_juris, key=str):
        avisos.append(f"assimetria: nó de jurisprudência '{i}' sem registro em jurisprudencia.json")
    return erros, avisos


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
