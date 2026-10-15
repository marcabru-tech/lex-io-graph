"""Testes de validar_jurisprudencia. Uso: python -m unittest discover tests"""

import contextlib
import copy
import io
import sys
import unittest
from unittest import mock
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib import validacao  # noqa: E402
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


def rodar_main(argv, erros_jur=(), avisos_jur=()):
    """Executa validacao.main com todas as validações substituídas; devolve (código, saída, chamadas)."""
    chamadas = []

    def falso(nome, retorno):
        def f(*a, **k):
            chamadas.append(nome)
            return retorno
        return f

    with mock.patch.object(validacao, "validar_corpus", falso("corpus", [])),          mock.patch.object(validacao, "validar_radar", falso("radar", [])),          mock.patch.object(validacao, "validar_jurisprudencia",
                           falso("jurisprudencia", (list(erros_jur), list(avisos_jur)))):
        saida = io.StringIO()
        with contextlib.redirect_stdout(saida):
            codigo = validacao.main(argv)
    return codigo, saida.getvalue(), chamadas


class TestMain(unittest.TestCase):
    def test_modo_normal_executa_jurisprudencia(self):
        codigo, _, chamadas = rodar_main([])
        self.assertEqual(codigo, 0)
        self.assertEqual(sorted(chamadas), ["corpus", "jurisprudencia", "radar"])

    def test_modo_radar_nao_executa_jurisprudencia(self):
        codigo, _, chamadas = rodar_main(["--radar"])
        self.assertEqual(codigo, 0)
        self.assertEqual(chamadas, ["radar"])

    def test_erro_de_jurisprudencia_bloqueia(self):
        codigo, saida, _ = rodar_main([], erros_jur=["boom"])
        self.assertEqual(codigo, 1)
        self.assertIn("boom", saida)

    def test_advertencia_nao_bloqueia_e_e_impressa(self):
        codigo, saida, _ = rodar_main([], avisos_jur=["aviso x"])
        self.assertEqual(codigo, 0)
        self.assertIn("aviso x", saida)
        self.assertIn("não bloqueiam", saida)


if __name__ == "__main__":
    unittest.main()
