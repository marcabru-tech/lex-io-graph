"""Aviso de enquadramento do Decreto 12.976/2026 para IA em serviço online (decisão da Luna, 25/10/2026)."""
import itertools
import json
import unittest
from contextlib import contextmanager
from pathlib import Path
from unittest import mock

import lib.conformidade as conformidade
from lib.conformidade import (ENQUADRAMENTO_DECRETO_12976, ENQUADRAMENTO_DECRETO_12976_IA, PERGUNTAS,
                              TAGS_DECRETO_12976, gerar_radar, gerar_relatorio_html)

RAIZ = Path(__file__).resolve().parent.parent
NORMAS = json.loads((RAIZ / "data" / "normas.json").read_text(encoding="utf-8"))["nodes"]
ARESTAS = json.loads((RAIZ / "data" / "arestas.json").read_text(encoding="utf-8"))["edges"]
MARCA = "Verifique o enquadramento"


def _tela(radar):
    chamadas = []

    class _Col:
        def metric(self, *a, **k):
            pass

    @contextmanager
    def _expander(*a, **k):
        yield

    st_falso = mock.MagicMock()
    for nome in ("markdown", "info", "caption"):
        getattr(st_falso, nome).side_effect = lambda t, *a, **k: chamadas.append(t)
    st_falso.columns.side_effect = lambda n: [_Col() for _ in range(n)]
    st_falso.expander.side_effect = _expander
    with mock.patch.object(conformidade, "st", st_falso):
        conformidade.render_radar(radar)
    return chamadas


class TestTexto(unittest.TestCase):
    def test_conteudo_exigido(self):
        t = ENQUADRAMENTO_DECRETO_12976_IA
        for trecho in ("não determina a incidência jurídica", "aplicação de internet",
                       "funcionalidades de IA", "hipóteses específicas", "art. 9º", "art. 10",
                       "não atrai, por si só"):
            self.assertIn(trecho, t)
        self.assertTrue(t.startswith(MARCA))


class TestRegra(unittest.TestCase):
    def test_ia_em_site_institucional_recebe_o_aviso_sem_acao(self):
        for usa_ia in ("Sim", "Estou avaliando"):
            perfil = {"setor": "Outro", "usa_ia": usa_ia, "online": "Sim — site institucional"}
            r = gerar_radar(perfil, NORMAS, ARESTAS)
            self.assertEqual(r["aviso_decreto_12976"], ENQUADRAMENTO_DECRETO_12976_IA, usa_ia)
            self.assertFalse({a["tag_origem"] for a in r["acoes"]} & TAGS_DECRETO_12976)

    def test_plataforma_continua_com_o_aviso_das_acoes(self):
        for usa_ia in ("Sim", "Estou avaliando", "Não"):
            perfil = {"setor": "Outro", "usa_ia": usa_ia, "online": "Sim — plataforma / app"}
            self.assertEqual(gerar_radar(perfil, NORMAS, ARESTAS)["aviso_decreto_12976"],
                             ENQUADRAMENTO_DECRETO_12976, usa_ia)

    def test_sem_ia_ou_sem_servico_online_nao_ha_aviso(self):
        for perfil in ({"usa_ia": "Não", "online": "Sim — site institucional"},
                       {"usa_ia": "Sim", "online": "Não"},
                       {"usa_ia": "Estou avaliando", "online": "Não"}):
            self.assertIsNone(gerar_radar(dict(perfil, setor="Outro"), NORMAS, ARESTAS)["aviso_decreto_12976"])

    def test_todos_os_perfis_um_aviso_no_maximo_e_na_regra(self):
        chaves = list(PERGUNTAS)
        for combo in itertools.product(*[PERGUNTAS[k]["opcoes"] for k in chaves]):
            perfil = dict(zip(chaves, combo))
            r = gerar_radar(perfil, NORMAS, ARESTAS)
            com_acao = any(a["tag_origem"] in TAGS_DECRETO_12976 for a in r["acoes"])
            ia_online = (perfil["usa_ia"] in ("Sim", "Estou avaliando")
                         and perfil["online"] in ("Sim — site institucional", "Sim — plataforma / app"))
            esperado = (ENQUADRAMENTO_DECRETO_12976 if com_acao
                        else ENQUADRAMENTO_DECRETO_12976_IA if ia_online else None)
            self.assertEqual(r["aviso_decreto_12976"], esperado, perfil)
            html = gerar_relatorio_html(r, perfil)
            self.assertEqual(html.count(MARCA), 1 if esperado else 0, perfil)


class TestApresentacao(unittest.TestCase):
    PERFIL = {"setor": "Outro", "usa_ia": "Sim", "online": "Sim — site institucional"}

    def test_tela_uma_vez_antes_das_acoes(self):
        r = gerar_radar(self.PERFIL, NORMAS, ARESTAS)
        textos = _tela(r)
        avisos = [i for i, t in enumerate(textos) if MARCA in t]
        self.assertEqual(len(avisos), 1)
        titulo = textos.index("#### Ações recomendadas")
        primeira = next(i for i, t in enumerate(textos) if r["acoes"][0]["acao"] in t)
        self.assertLess(titulo, avisos[0])
        self.assertLess(avisos[0], primeira)

    def test_relatorio_uma_vez_antes_das_acoes(self):
        r = gerar_radar(self.PERFIL, NORMAS, ARESTAS)
        html = gerar_relatorio_html(r, self.PERFIL)
        self.assertEqual(html.count(MARCA), 1)
        self.assertLess(html.index("Ações Recomendadas"), html.index(MARCA))
        from html import escape
        self.assertLess(html.index(MARCA), html.index(escape(r["acoes"][0]["acao"])))


if __name__ == "__main__":
    unittest.main()
