"""
Contador de visitas sem cookies e sem dados pessoais.

Cada vez que uma sessão abre uma página pela primeira vez, uma linha JSON
é escrita na saída padrão. No Google Cloud Run, o Cloud Logging guarda essa
linha como registro estruturado, consultável e agregável em painel.

O que é registrado: página, data e hora (UTC), um código aleatório da sessão
e o ambiente (gcp ou outro). O que NÃO é registrado: IP, navegador, cookies,
localização ou qualquer dado que identifique a pessoa. O código de sessão é
gerado ao acaso no servidor e morre com a sessão: não liga visitas de dias
diferentes à mesma pessoa.

Interações dentro da mesma página (filtros, botões) não geram nova linha:
o Streamlit reexecuta a página a cada clique, e o registro é feito uma vez
por página por sessão.
"""

import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

import streamlit as st


def _nome_da_pagina(arquivo: str) -> str:
    nome = Path(arquivo).stem
    if nome == "app":
        return "home"
    # "8_📡_Radar_Legislativo" -> "Radar_Legislativo"
    partes = [p for p in nome.split("_") if p and not p.isdigit() and p.isascii()]
    return "_".join(partes) or nome


def registrar_visita(arquivo_da_pagina: str) -> None:
    """Registra a primeira abertura de uma página nesta sessão. Nunca levanta erro."""
    try:
        pagina = _nome_da_pagina(arquivo_da_pagina)
        if "_tel_sessao" not in st.session_state:
            st.session_state["_tel_sessao"] = uuid.uuid4().hex[:12]
            st.session_state["_tel_vistas"] = set()
        vistas = st.session_state["_tel_vistas"]
        if pagina in vistas:
            return
        vistas.add(pagina)
        linha = {
            "severity": "INFO",
            "evento": "visita",
            "pagina": pagina,
            "sessao": st.session_state["_tel_sessao"],
            "ambiente": "gcp" if os.environ.get("K_SERVICE") else "outro",
            "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        }
        print(json.dumps(linha, ensure_ascii=False), file=sys.stdout, flush=True)
    except Exception:
        # Telemetria nunca pode derrubar uma página.
        pass
