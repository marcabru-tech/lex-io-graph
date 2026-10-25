"""A6-e: fusão entre Casas só com ementas normalizadas iguais; ementa nula na coleta."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import lib.radar as radar
import updater
from lib.radar import consolidar_tema, ementa_normalizada


def _item(casa, sigla, ementa, id_=None, termo="dados pessoais", **extra):
    return {"id": id_ or f"{casa}-{sigla}", "sigla": sigla, "ementa": ementa, "termo_busca": termo,
            "url": f"https://www.{'senado' if casa == 'senado' else 'camara'}.leg.br/x", **extra}


def _tema(senado=(), camara=()):
    return {"senado": list(senado), "camara": list(camara), "lexml": []}


def _todos(c):
    return c["principal"] + c["conferir"]


class TestNormalizacao(unittest.TestCase):
    def test_conservadora(self):
        self.assertEqual(ementa_normalizada("Dispõe sobre  DADOS pessoais."),
                         ementa_normalizada("dispõe sobre dados pessoais"))
        self.assertEqual(ementa_normalizada("Altera a Lei nº 11.196, de 2005"),
                         ementa_normalizada("Altera a Lei n.º 11.196 de 2005"))
        self.assertEqual(ementa_normalizada("Lei nº 1"), ementa_normalizada("Lei N.º 1"))
        self.assertEqual(ementa_normalizada("Lei nº 1"), ementa_normalizada("Lei n° 1"))
        # Pontuação vira separador: palavras coladas continuam diferentes.
        self.assertNotEqual(ementa_normalizada("ab-cd"), ementa_normalizada("abcd"))
        self.assertNotEqual(ementa_normalizada("a/b"), ementa_normalizada("ab"))
        self.assertEqual(ementa_normalizada("ab-cd"), ementa_normalizada("ab cd"))
        self.assertNotEqual(ementa_normalizada("Lei 11.196"), ementa_normalizada("Lei 11 196"))
        # Acento e palavra diferente continuam diferentes (sem aproximação).
        self.assertNotEqual(ementa_normalizada("Dispõe sobre dados"), ementa_normalizada("Dispoe sobre dados"))
        self.assertNotEqual(ementa_normalizada("Dispõe sobre dados pessoais"),
                            ementa_normalizada("Dispõe sobre dados pessoais sensíveis"))
        self.assertEqual(ementa_normalizada(None), "")


class TestFusao(unittest.TestCase):
    def test_ementas_iguais_fundem_e_preservam_proveniencia(self):
        t = _tema([_item("senado", "PL 9/2026", "Trata de dados pessoais.")],
                  [_item("camara", "PL 9/2026", "TRATA de dados  pessoais", termo_na_ementa=True)])
        cartoes = _todos(consolidar_tema(t, "dados"))
        self.assertEqual(len(cartoes), 1)
        self.assertEqual([(f["casa"], f["id"]) for f in cartoes[0]["fontes"]],
                         [("senado", "senado-PL 9/2026"), ("camara", "camara-PL 9/2026")])
        self.assertEqual(cartoes[0]["identidades"], [("PL 9/2026", "camara"), ("PL 9/2026", "senado")])

    def test_ementas_diferentes_separam_com_sufixo_da_casa(self):
        t = _tema([_item("senado", "PL 9/2026", "Trata de dados pessoais")],
                  [_item("camara", "PL 9/2026", "Dispõe sobre dados pessoais de crianças", termo_na_ementa=True)])
        cartoes = _todos(consolidar_tema(t, "dados"))
        self.assertEqual([c["chave"] for c in cartoes], ["PL 9/2026", "PL 9/2026@camara"])
        self.assertEqual([len(c["fontes"]) for c in cartoes], [1, 1])

    def test_ementa_vazia_ou_nula_nao_serve_de_prova(self):
        for vazia in ("", None, "  "):
            t = _tema([_item("senado", "PL 9/2026", vazia)],
                      [_item("camara", "PL 9/2026", vazia, termo_na_ementa=True)])
            self.assertEqual(len(_todos(consolidar_tema(t, "dados"))), 2, repr(vazia))

    def test_mesma_casa_dois_registros_continua_um_cartao(self):
        t = _tema(camara=[_item("camara", "PL 9/2026", "Trata de dados pessoais", id_="1", termo="dados pessoais"),
                          _item("camara", "PL 9/2026", "Trata de dados pessoais", id_="1", termo="privacidade")])
        self.assertEqual(len(_todos(consolidar_tema(t, "dados"))), 1)


class TestNovidadesComNovaIdentidade(unittest.TestCase):
    def test_separar_cartao_ja_visto_nao_cria_novidade(self):
        antes = {"temas": {"dados": _tema([_item("senado", "PL 9/2026", "Trata de dados pessoais")],
                                          [_item("camara", "PL 9/2026", "Trata de dados pessoais",
                                                 termo_na_ementa=True)])}}
        depois = {"temas": {"dados": _tema([_item("senado", "PL 9/2026", "Trata de dados pessoais")],
                                           [_item("camara", "PL 9/2026", "Trata de dados pessoais e crédito",
                                                  termo_na_ementa=True)])}}
        self.assertEqual(updater.detectar_novidades(depois, antes), [])

    def test_fundir_registros_ja_vistos_nao_cria_novidade(self):
        antes = {"temas": {"dados": _tema([_item("senado", "PL 9/2026", "Trata de dados pessoais")],
                                          [_item("camara", "PL 9/2026", "Outro texto sobre dados pessoais",
                                                 termo_na_ementa=True)])}}
        depois = {"temas": {"dados": _tema([_item("senado", "PL 9/2026", "Trata de dados pessoais")],
                                           [_item("camara", "PL 9/2026", "Trata de dados pessoais",
                                                  termo_na_ementa=True)])}}
        self.assertEqual(updater.detectar_novidades(depois, antes), [])

    def test_camara_distinta_com_mesma_designacao_e_novidade(self):
        antes = {"temas": {"dados": _tema([_item("senado", "PL 9/2026", "Trata de dados pessoais")])}}
        depois = {"temas": {"dados": _tema([_item("senado", "PL 9/2026", "Trata de dados pessoais")],
                                           [_item("camara", "PL 9/2026", "Dispõe sobre dados pessoais no crédito",
                                                  termo_na_ementa=True)])}}
        nov = updater.detectar_novidades(depois, antes)
        self.assertEqual([(n["chave"], n["fonte"]) for n in nov], [("PL 9/2026@camara", "Câmara dos Deputados")])


    def test_senado_antigo_e_camara_nova_com_ementa_igual(self):
        # Caso da revisão da Luna: Senado conhecido, Câmara ausente antes, ementas
        # iguais -> um cartão consolidado, e o registro novo da Câmara alerta.
        antes = {"temas": {"dados": _tema([_item("senado", "PL 9/2026", "Trata de dados pessoais")])}}
        depois = {"temas": {"dados": _tema([_item("senado", "PL 9/2026", "Trata de dados pessoais")],
                                           [_item("camara", "PL 9/2026", "Trata de dados pessoais.",
                                                  termo_na_ementa=True)])}}
        self.assertEqual(len(_todos(consolidar_tema(depois["temas"]["dados"], "dados"))), 1)
        nov = updater.detectar_novidades(depois, antes)
        self.assertEqual(len(nov), 1)
        self.assertEqual(nov[0]["identidades_novas"], [["PL 9/2026", "camara"]])
        self.assertEqual(nov[0]["fonte"], "Câmara dos Deputados")
        self.assertTrue(nov[0]["url"].startswith("https://www.camara.leg.br"))
        # Na coleta seguinte, nada se repete.
        self.assertEqual(updater.detectar_novidades(depois, depois), [])

    def test_duas_casas_novas_na_mesma_coleta_um_alerta(self):
        depois = {"temas": {"dados": _tema([_item("senado", "PL 9/2026", "Trata de dados pessoais")],
                                           [_item("camara", "PL 9/2026", "Trata de dados pessoais",
                                                  termo_na_ementa=True)])}}
        nov = updater.detectar_novidades(depois, {})
        self.assertEqual(len(nov), 1)
        self.assertEqual(nov[0]["identidades_novas"], [["PL 9/2026", "camara"], ["PL 9/2026", "senado"]])


class TestEmentaNula(unittest.TestCase):
    def test_coleta_da_camara_com_ementa_nula(self):
        resp = mock.Mock()
        resp.json.return_value = {"dados": [{"id": 7, "siglaTipo": "PL", "numero": 9, "ano": 2026,
                                             "ementa": None}]}
        resp.raise_for_status.return_value = None
        with mock.patch.object(radar.requests, "get", return_value=resp):
            itens = radar.buscar_camara("dados pessoais")
        self.assertEqual(itens[0]["ementa"], "")
        self.assertFalse(itens[0]["termo_na_ementa"])

    def test_salvar_radar_com_novidade_sem_ementa(self):
        with tempfile.TemporaryDirectory() as pasta, \
             mock.patch.object(updater, "RADAR_PATH", Path(pasta) / "radar.json"):
            updater.salvar_radar({"ultima_atualizacao": "2026-10-26T09:00:00", "temas": {}}, [{"tema": "t", "fonte": "f", "sigla": "PL 1/2026",
                                                  "ementa": None, "url": ""}])
            dados = json.loads((Path(pasta) / "radar.json").read_text(encoding="utf-8"))
        self.assertEqual(dados["total_novidades"], 1)


class TestLinks(unittest.TestCase):
    def test_links_do_cartao_com_rel(self):
        from lib.radar_cartao import html_cartao
        t = _tema([_item("senado", "PL 9/2026", "Trata de dados pessoais")],
                  [_item("camara", "PL 9/2026", "Trata de dados pessoais", termo_na_ementa=True)])
        html = html_cartao(_todos(consolidar_tema(t, "dados"))[0])
        self.assertEqual(html.count('target="_blank"'), html.count('rel="noopener noreferrer"'))
        self.assertEqual(html.count('rel="noopener noreferrer"'), 2)


if __name__ == "__main__":
    unittest.main()
