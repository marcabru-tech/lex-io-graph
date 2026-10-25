"""Cartão HTML de uma norma na página Grafo (modo Lista).

Todo texto vindo dos dados é escapado antes de entrar no HTML (A6-d).
"""
from html import escape

from lib.constants import rotulo_status


def _esc(valor) -> str:
    return escape("" if valor is None else str(valor))


def html_cartao_norma(nid: str, nd: dict, conexoes: int, destaque: bool) -> str:
    border_color = "#d4a853" if destaque else "rgba(255,255,255,0.08)"
    return f"""
    <div style="background:rgba(255,255,255,0.03);border:1px solid {border_color};
    border-radius:6px;padding:12px 16px;margin-bottom:8px;">
    <span style="color:#d4a853;font-family:monospace;font-weight:bold;">{_esc(nd.get("label", nid))}</span>
    <span style="color:#706a60;font-size:11px;margin-left:8px;">
    {_esc(nd.get("tipo_label", ""))} · {_esc(rotulo_status(nd.get("status", "")))} · {int(conexoes)} conexão(ões)</span><br>
    <span style="color:#8a8478;font-size:12px;">{_esc(nd.get("ementa", ""))}</span>
    </div>"""
