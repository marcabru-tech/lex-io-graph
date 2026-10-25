"""
HTML e leitura de dados da página do IPII Engine.

Funções puras, separadas da página para serem testáveis. Todo valor vindo do
relatório do motor passa por html.escape antes de entrar num bloco HTML: o
fato de o dado ser gerado pelo próprio motor não elimina o risco de um valor
inesperado ou malformado.
"""

import json
from html import escape
from pathlib import Path

TIER_LABELS = {
    1: ("tier-1", "TIER 1 — FORTE (≥ 0.75)"),
    2: ("tier-2", "TIER 2 — FORTE (0.65–0.74)"),
    3: ("tier-3", "TIER 3 — MODERADA (0.55–0.64)"),
    4: ("tier-3", "TIER 4 — MODERADA (0.45–0.54)"),
    5: ("tier-3", "TIER 5 — FRACA (0.40–0.44)"),
}
TIPO_LABELS = {
    "hierarquia": "Hierarquia normativa",
    "interpreta": "Interpretação judicial",
    "regulamenta": "Regulamentação",
    "intersecao": "Interseção temática",
    "complementaridade": "Complementaridade",
    "antinomia": "Antinomia",
}
_CLASSES_TIER = {"tier-1", "tier-2", "tier-3"}


def esc(valor) -> str:
    return escape("" if valor is None else str(valor))


def pct(valor) -> str:
    """Percentual inteiro; valor ausente ou não numérico vira travessão."""
    try:
        return f"{float(valor):.0%}"
    except (TypeError, ValueError):
        return "—"


def _lista(valores) -> str:
    if not isinstance(valores, (list, tuple)):
        return ""
    return ", ".join(esc(v) for v in valores)


def html_aresta_nova(n: dict) -> str:
    tier = n.get("tier", 5)
    css_class, tier_label = TIER_LABELS.get(tier, ("tier-3", f"TIER {tier}"))
    css_class = css_class if css_class in _CLASSES_TIER else "tier-3"
    tipo = n.get("tipo_sugerido", "")
    temas = _lista(n.get("temas_comuns", []))
    jurs = _lista(n.get("jurisdicoes_comuns", []))
    return f"""
<div class="tier-card {css_class}">
  <div class="tier-label">{esc(tier_label)}</div>
  <div class="aresta-par">{esc(n.get('source'))} ↔ {esc(n.get('target'))}</div>
  <div class="aresta-score">Score: {esc(n.get('score'))} · {esc(str(n.get('classificacao', '')).upper())}</div>
  <div class="aresta-tipo">Tipo sugerido: {esc(TIPO_LABELS.get(tipo, tipo))}</div>
  <div class="aresta-temas">Temas comuns: {temas or '—'}</div>
  {f'<div class="aresta-temas">Jurisdições: {jurs}</div>' if jurs else ''}
</div>"""


def html_aresta_confirmada(c: dict) -> str:
    sug, ex = c.get("tipo_sugerido", ""), c.get("tipo_existente", "")
    marca = "✓ match" if c.get("match_tipo", False) else "≠ divergente"
    return f"""
<div class="tier-card tier-3">
  <div class="aresta-par">{esc(c.get('source'))} ↔ {esc(c.get('target'))}</div>
  <div class="aresta-score">Score: {esc(c.get('score'))}</div>
  <div class="aresta-tipo">Tipo sugerido: {esc(TIPO_LABELS.get(sug, sug))} · Tipo existente: {esc(TIPO_LABELS.get(ex, ex))} · {marca}</div>
</div>"""


def ler_total_normas(caminho: Path) -> tuple[int | None, str | None]:
    """(quantidade de normas, None) ou (None, mensagem de erro legível)."""
    try:
        with open(caminho, encoding="utf-8") as f:
            dados = json.load(f)
    except FileNotFoundError:
        return None, f"Arquivo do corpus não encontrado: {caminho.name}."
    except json.JSONDecodeError as e:
        return None, f"Arquivo do corpus inválido ({caminho.name}, linha {e.lineno})."
    except OSError as e:
        return None, f"Não foi possível ler o corpus ({caminho.name}): {e.strerror or e}."
    nodes = dados.get("nodes") if isinstance(dados, dict) else None
    if not isinstance(nodes, list):
        return None, f"Arquivo do corpus sem a lista de normas ({caminho.name})."
    return len(nodes), None
