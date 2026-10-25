"""A6-c: score, classificação, tier e filtros do IPII concordam entre si."""
import itertools
import json
import re
import unittest
from pathlib import Path

from lib.ipii import matcher
from lib.ipii.matcher import THRESHOLD_FRACA, calcular_intersecao, calcular_todas_intersecoes, classificar
from lib.ipii.tokenizer import tokenizar_corpus
from lib.ipii.validator import filtrar_por_tier as filtrar_validator
from lib.ipii_pagina import TIER_LABELS, filtrar_por_tier as filtrar_pagina

RAIZ = Path(__file__).resolve().parent.parent
NORMAS = json.loads((RAIZ / "data" / "normas.json").read_text(encoding="utf-8"))["nodes"]
TOKENS = tokenizar_corpus(NORMAS)


class TestCasoMedido(unittest.TestCase):
    def test_lgpd_anpd_no_limiar_e_fraca_tier_5(self):
        r = calcular_intersecao(TOKENS["lgpd"], TOKENS["anpd"])
        self.assertEqual((r["score"], r["classificacao"], r["tier"]), (0.4, "fraca", 5))


class TestConsistencia(unittest.TestCase):
    def test_todos_os_pares_do_corpus(self):
        ids = [i for i, t in TOKENS.items() if not matcher.excluida_do_ipii(t)]
        for a, b in itertools.combinations(ids, 2):
            r = calcular_intersecao(TOKENS[a], TOKENS[b])
            with self.subTest(par=(a, b)):
                self.assertEqual((r["classificacao"], r["tier"]), classificar(r["score"]))
                self.assertEqual(r["score"] >= THRESHOLD_FRACA, r["tier"] >= 1)

    def test_sugeridas_nunca_sao_irrelevantes(self):
        for r in calcular_todas_intersecoes(TOKENS):
            self.assertNotEqual(r["classificacao"], "irrelevante", (r["source"], r["target"]))
            self.assertIn(r["tier"], range(1, 6))


class TestFaixas(unittest.TestCase):
    CASOS = ((0.399, "irrelevante", 0), (0.4, "fraca", 5), (0.499, "fraca", 5), (0.5, "fraca", 4),
             (0.549, "fraca", 4), (0.55, "moderada", 3), (0.649, "moderada", 3), (0.65, "moderada", 2),
             (0.749, "moderada", 2), (0.75, "forte", 1), (1.0, "forte", 1))

    def test_cortes(self):
        for score, cls, tier in self.CASOS:
            self.assertEqual(classificar(score), (cls, tier), score)

    def test_rotulos_batem_com_o_motor(self):
        for score, cls, tier in self.CASOS:
            if tier == 0:
                continue
            rotulo = TIER_LABELS[tier][1]
            self.assertIn(cls.upper(), rotulo, (score, rotulo))
            nums = [float(x) for x in re.findall(r"\d\.\d{3}", rotulo)]
            self.assertTrue(nums, f"faixa ausente no rótulo: {rotulo}")
            self.assertGreaterEqual(score, nums[0], rotulo)
            if len(nums) > 1:
                self.assertLessEqual(score, nums[1], rotulo)


class TestFiltros(unittest.TestCase):
    NOVAS = [{"tier": 0, "classificacao": "irrelevante"}, {"tier": 1}, {"tier": 3}, {"tier": 5},
             {"tier": None}, {"tier": "1"}, {}]

    def test_validator_exclui_tier_0_e_invalidos(self):
        self.assertEqual([n["tier"] for n in filtrar_validator(self.NOVAS, 5)], [1, 3, 5])
        self.assertEqual([n["tier"] for n in filtrar_validator(self.NOVAS, 3)], [1, 3])

    def test_pagina_exclui_irrelevante(self):
        tiers = [n.get("tier") for n in filtrar_pagina(self.NOVAS, 5)]
        self.assertNotIn(0, tiers)
        self.assertEqual(len(filtrar_pagina([{"tier": 2, "classificacao": "irrelevante"}], 5)), 0)
        # Os tiers válidos e os malformados seguem visíveis conforme o contrato da A4.
        sobreviventes = filtrar_pagina(self.NOVAS, 5)
        self.assertEqual(sobreviventes, self.NOVAS[1:])
        self.assertTrue(all(n.get("classificacao") != "irrelevante" for n in sobreviventes))


if __name__ == "__main__":
    unittest.main()
