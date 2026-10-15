"""Testes de validar_jurisprudencia. Uso: python -m unittest discover tests"""

import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.validacao import digito_cnj, validar_jurisprudencia  # noqa: E402

NUMERO_VALIDO = "5012345-32.2022.4.04.7100"
NUMERO_DIVERGENTE = "5012345-67.2022.4.04.7100"


def registro(estado, numero):
    return {
        "id": "x", "tribunal": "TRF-4", "numero": numero,
        "estado_verificacao": estado,
        "fonte_oficial_url": None, "orgao_julgador": None, "relator": None,
        "data_julgamento": None, "data_publicacao": None,
        "nivel_autoridade": "desconhecido",
        "proveniencia": {"origem": None, "data_consulta": None, "observacao": "teste"},
    }


def rodar(reg):
    juris = {"jurisprudencia": [reg]}
    normas = {"nodes": [{"id": reg["id"], "tipo": "jurisprudencia"}]}
    return validar_jurisprudencia(juris, normas)


class TestDigitoCNJ(unittest.TestCase):
    def test_calculo(self):
        self.assertEqual(digito_cnj("5012345", "2022", "4", "04", "7100"), 32)


class TestDivergenciaDeDigito(unittest.TestCase):
    def test_contestado_gera_advertencia_nao_bloqueante(self):
        erros, avisos = rodar(registro("contestado", NUMERO_DIVERGENTE))
        self.assertEqual(erros, [])
        self.assertTrue(any("esperado 32" in a and "não bloqueante" in a for a in avisos))

    def test_verificado_gera_erro_bloqueante(self):
        reg = registro("verificado", NUMERO_DIVERGENTE)
        reg.update(fonte_oficial_url="https://exemplo.test", orgao_julgador="X",
                   relator="Y", data_julgamento="2022-01-01", nivel_autoridade="vinculante")
        erros, _ = rodar(reg)
        self.assertTrue(any("esperado 32" in e for e in erros))

    def test_numero_valido_nao_gera_nada(self):
        erros, avisos = rodar(registro("contestado", NUMERO_VALIDO))
        self.assertEqual((erros, avisos), ([], []))


class TestEstados(unittest.TestCase):
    def test_estado_invalido(self):
        erros, _ = rodar(registro("talvez", NUMERO_VALIDO))
        self.assertTrue(any("estado_verificacao inválido" in e for e in erros))

    def test_campo_ausente(self):
        reg = registro("pendente", NUMERO_VALIDO)
        del reg["relator"]
        erros, _ = rodar(reg)
        self.assertTrue(any("'relator'" in e for e in erros))

    def test_verificado_exige_campos(self):
        erros, _ = rodar(registro("verificado", NUMERO_VALIDO))
        for c in ("fonte_oficial_url", "orgao_julgador", "relator", "data_julgamento", "nivel_autoridade"):
            self.assertTrue(any(c in e for e in erros), c)


class TestAssimetrias(unittest.TestCase):
    def test_nos_dois_sentidos_sao_advertencias(self):
        juris = {"jurisprudencia": [registro("pendente", NUMERO_VALIDO)]}
        normas = {"nodes": [{"id": "outro", "tipo": "jurisprudencia"}]}
        erros, avisos = validar_jurisprudencia(copy.deepcopy(juris), normas)
        self.assertEqual(erros, [])
        self.assertTrue(any("registro de jurisprudência 'x' sem nó" in a for a in avisos))
        self.assertTrue(any("nó de jurisprudência 'outro' sem registro" in a for a in avisos))


class TestDadosReais(unittest.TestCase):
    def test_sem_erros_e_assimetrias_conhecidas(self):
        erros, avisos = validar_jurisprudencia()
        self.assertEqual(erros, [])
        self.assertEqual(sum("sem nó em normas.json" in a for a in avisos), 2)
        self.assertEqual(sum("sem registro em jurisprudencia.json" in a for a in avisos), 1)


if __name__ == "__main__":
    unittest.main()
