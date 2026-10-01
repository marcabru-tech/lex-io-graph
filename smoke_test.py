"""
smoke_test.py — verificação mínima antes de publicar.

Roda em três camadas, da mais barata para a mais cara:
  1. Integridade dos dados (lib/validacao.py): ids, arestas, status, temas,
     ids citados na teoria, snapshot do radar.
  2. Import de todos os módulos de lib/ (pega o ImportError antes do deploy).
  3. Execução de cada página com o AppTest do Streamlit, sem navegador.

Uso local:   python smoke_test.py          (~10 s, pouca memória)
No CI:       .github/workflows/ci.yml roda o mesmo arquivo em cada PR.
Saída 1 se qualquer camada falhar.
"""

import importlib
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ))

falhas: list[str] = []


def etapa(titulo: str):
    print(f"\n== {titulo} ==")


etapa("1. Integridade dos dados")
from lib.validacao import validar_corpus, validar_radar  # noqa: E402

for erro in validar_corpus() + validar_radar():
    falhas.append(f"dados: {erro}")
    print(f"  ✗ {erro}")
if not falhas:
    print("  ✓ corpus, teoria e radar consistentes")

etapa("2. Módulos de lib/")
for arq in sorted((RAIZ / "lib").glob("*.py")):
    if arq.stem == "__init__":
        continue
    try:
        importlib.import_module(f"lib.{arq.stem}")
        print(f"  ✓ lib.{arq.stem}")
    except Exception as e:  # noqa: BLE001
        falhas.append(f"import lib.{arq.stem}: {e!r}")
        print(f"  ✗ lib.{arq.stem}: {e!r}")

etapa("3. Páginas (AppTest)")
from streamlit.testing.v1 import AppTest  # noqa: E402

paginas = [RAIZ / "app.py"] + sorted((RAIZ / "pages").glob("*.py"))
for p in paginas:
    try:
        at = AppTest.from_file(str(p), default_timeout=90).run()
        if at.exception:
            msg = at.exception[0].message
            falhas.append(f"página {p.name}: {msg}")
            print(f"  ✗ {p.name}: {msg}")
        else:
            print(f"  ✓ {p.name}")
    except Exception as e:  # noqa: BLE001
        falhas.append(f"página {p.name}: {e!r}")
        print(f"  ✗ {p.name}: {e!r}")

print()
if falhas:
    print(f"FALHOU — {len(falhas)} problema(s).")
    sys.exit(1)
print("OK — pronto para publicar.")
