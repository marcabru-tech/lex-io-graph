"""Testes de lib.formato. Uso: python -m unittest discover tests"""

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.formato import quantidade, resumo_verificacao  # noqa: E402


def reg(estado):
    """Registro mínimo: resumo_verificacao só lê estado_verificacao."""
    return {"id": "x", "estado_verificacao": estado}


class TestQuantidade(unittest.TestCase):
    def test_zero_fica_no_plural(self):
        self.assertEqual(quantidade(0, "verificado", "verificados"), "0 verificados")

    def test_um_fica_no_singular(self):
        self.assertEqual(quantidade(1, "verificado", "verificados"), "1 verificado")

    def test_dois_ou_mais_ficam_no_plural(self):
        self.assertEqual(quantidade(2, "pendente", "pendentes"), "2 pendentes")
        self.assertEqual(quantidade(17, "pendente", "pendentes"), "17 pendentes")


class TestResumoVerificacao(unittest.TestCase):
    def test_corpus_vazio(self):
        self.assertEqual(
            resumo_verificacao([]),
            "0 verificados · 0 pendentes · 0 contestados",
        )

    def test_distribuicao_atual_do_corpus_em_plural(self):
        registros = [reg("pendente")] * 3 + [reg("contestado")] * 2
        self.assertEqual(
            resumo_verificacao(registros),
            "0 verificados · 3 pendentes · 2 contestados",
        )

    def test_um_de_cada_fica_no_singular(self):
        registros = [reg("verificado"), reg("pendente"), reg("contestado")]
        self.assertEqual(
            resumo_verificacao(registros),
            "1 verificado · 1 pendente · 1 contestado",
        )

    def test_sem_estado_nao_aparece_quando_zero(self):
        self.assertNotIn("sem estado", resumo_verificacao([reg("pendente")]))

    def test_sem_estado_aparece_quando_houver(self):
        registros = [reg("verificado"), reg(None), {"id": "y"}]
        self.assertEqual(
            resumo_verificacao(registros),
            "1 verificado · 0 pendentes · 0 contestados · 2 sem estado",
        )

    def test_estado_invalido_conta_como_sem_estado(self):
        self.assertIn("1 sem estado", resumo_verificacao([reg("verificadoo")]))


class TestResumoComCorpusReal(unittest.TestCase):
    def test_legenda_que_a_home_exibe_hoje(self):
        caminho = Path(__file__).resolve().parent.parent / "data" / "jurisprudencia.json"
        with open(caminho, encoding="utf-8") as f:
            registros = json.load(f)["jurisprudencia"]
        self.assertEqual(
            resumo_verificacao(registros),
            "0 verificados · 3 pendentes · 2 contestados",
        )


if __name__ == "__main__":
    unittest.main()
