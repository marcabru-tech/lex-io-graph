# Copyright © 2026 Hubstry Deep Tech — Guilherme Gonçalves Machado
# IPII Engine — implementação proprietária para Lex-IO-Graph / Lexiograph
# Todos os direitos reservados.
# Uso comercial, reprodução ou distribuição sem autorização escrita
# da Hubstry Deep Tech é expressamente proibido.
# Contato: globaldeeptechecosystem@hubstry.dev
# hubstry.dev/lex-io-graph
"""
Runner principal do IPII Engine para Lex-IO-Graph / Lexiograph.

Executa matching em todo o corpus normativo e gera relatório
de arestas sugeridas para revisão do curador.

Princípio: o engine alerta, o curador decide.
Nenhuma aresta é adicionada automaticamente ao grafo.

Uso:
    python ipii_engine.py
    python ipii_engine.py --threshold 0.55
    python ipii_engine.py --tier 2

Propriedade intelectual: Hubstry Deep Tech © 2026.
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from lib.ipii.tokenizer import tokenizar_corpus
from lib.ipii.matcher import calcular_todas_intersecoes, THRESHOLD_FRACA
from lib.ipii.validator import validar_arestas, filtrar_por_tier

DATA_DIR = Path("data")
RESULTADO_PATH = DATA_DIR / "ipii_resultado.json"


def main():
    parser = argparse.ArgumentParser(description="IPII Engine — Lex-IO-Graph")
    parser.add_argument("--threshold", type=float, default=THRESHOLD_FRACA,
                        help="Score mínimo para sugerir aresta (padrão: 0.40)")
    parser.add_argument("--tier", type=int, default=5,
                        help="Tier máximo nas novas (1=mais forte, 5=todos)")
    args = parser.parse_args()

    print(f"\n{'='*60}")
    print("IPII ENGINE — Lex-IO-Graph / Lexiograph")
    print("© 2026 Hubstry Deep Tech — Guilherme Gonçalves Machado")
    print(f"{'='*60}\n")

    # Carregar corpus
    with open(DATA_DIR / "normas.json", encoding="utf-8") as f:
        normas = json.load(f)["nodes"]

    with open(DATA_DIR / "arestas.json", encoding="utf-8") as f:
        arestas = json.load(f)["edges"]

    print(f"Corpus: {len(normas)} normas")
    print(f"Arestas existentes: {len(arestas)}")
    print(f"Threshold: {args.threshold}")
    print(f"Pares possíveis: {len(normas) * (len(normas)-1) // 2}\n")

    # 1. Tokenizar
    print("Tokenizando corpus (GuruMatrix 5D)...")
    tokens = tokenizar_corpus(normas)
    print(f"  Tokens gerados: {len(tokens)}")

    # 2. Matching
    print("\nCalculando interseções par-a-par...")
    sugeridas = calcular_todas_intersecoes(tokens, threshold=args.threshold)
    print(f"  Sugeridas (score ≥ {args.threshold}): {len(sugeridas)}")

    # 3. Validar
    print("\nValidando contra arestas existentes...")
    resultado = validar_arestas(sugeridas, arestas)

    # 4. Relatório
    print(f"\n{'='*60}")
    print("RESULTADOS")
    print(f"{'='*60}")
    print(f"  Arestas sugeridas:    {resultado['total_sugeridas']}")
    print(f"  Confirmadas (match):  {resultado['confirmadas']}")
    print(f"  Novas (descobertas):  {resultado['novas']}")
    print(f"  Não detectadas:       {resultado['faltando']}")
    print(f"  Precisão:             {resultado['precisao']:.1%}")
    print(f"  Cobertura:            {resultado['cobertura']:.1%}")

    # 5. Novas por tier
    novas_filtradas = filtrar_por_tier(resultado["detalhe_novas"], args.tier)

    if novas_filtradas:
        print(f"\n{'='*60}")
        print(f"NOVAS ARESTAS — Tier ≤ {args.tier} ({len(novas_filtradas)} pares)")
        print("Princípio: o engine alerta, o curador decide.")
        print(f"{'='*60}")
        for n in novas_filtradas:
            print(f"\n  [{n['tier']}] {n['source']} ↔ {n['target']}")
            print(f"       Score: {n['score']} | {n['classificacao'].upper()}")
            print(f"       Tipo sugerido: {n['tipo_sugerido']}")
            if n['temas_comuns']:
                print(f"       Temas comuns: {', '.join(n['temas_comuns'])}")

    # 6. Gap do engine
    if resultado["gap_engine"]:
        print(f"\n{'='*60}")
        print(f"GAP DO ENGINE ({len(resultado['gap_engine'])} arestas não detectadas)")
        print(f"{'='*60}")
        for g in resultado["gap_engine"]:
            print(f"  {g['par']} [{g['tipo']}]")

    # 7. Salvar resultado
    resultado["metadata"] = {
        "gerado_em": datetime.now().isoformat(),
        "threshold": args.threshold,
        "tier_filtro": args.tier,
        "engine": "IPII Engine v1.0",
        "propriedade": "Hubstry Deep Tech © 2026",
        "principio": "O engine alerta, o curador decide.",
    }

    with open(RESULTADO_PATH, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)

    print(f"\n✓ Resultado salvo em {RESULTADO_PATH}")
    print(f"  {len(resultado['detalhe_novas'])} arestas aguardando revisão do curador.\n")


if __name__ == "__main__":
    main()
