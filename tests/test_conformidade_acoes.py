"""Quadro de conformidade: ações alcançáveis e escopo explícito da interseção temática.

Fonte das ações do Decreto 12.976/2026 (arts. 3º, I; 4º; 5º, § 1º; 6º; 7º, § 1º; 8º; 9º; 10;
12, I e II), conferida em 25/10/2026 no texto oficial publicado pela Câmara dos Deputados
(Legislação Informatizada, publicação original, DOU de 21/05/2026):
https://www2.camara.leg.br/legin/fed/decret/2026/decreto-12976-20-maio-2026-799137-publicacaooriginal-179397-pe.html
O art. 12, I fixa 6 horas "nos casos de conteúdo manifestamente ilegal" e o II, 24 horas
"nos demais casos de violência contra a mulher em ambiente digital".
"""
import json
import unittest
from contextlib import contextmanager
from pathlib import Path
from unittest import mock

import lib.conformidade as conformidade

from lib.conformidade import (ACOES_POR_TAG, ENQUADRAMENTO_DECRETO_12976, FORA_DA_PONTUACAO, NORMA_TAGS,
                              PERFIL_TEMA_MAP, TAGS_OBSERVAVEIS, _gerar_acoes, _score_norma, _tags_norma,
                              gerar_radar, gerar_relatorio_html)

RAIZ = Path(__file__).resolve().parent.parent
NORMAS = json.loads((RAIZ / "data" / "normas.json").read_text(encoding="utf-8"))["nodes"]
ARESTAS = json.loads((RAIZ / "data" / "arestas.json").read_text(encoding="utf-8"))["edges"]


def _acoes(perfil: dict) -> set:
    return {a["tag_origem"] for a in _gerar_acoes(perfil)}


class TestAcoesAlcancaveis(unittest.TestCase):
    def test_toda_acao_e_gerada_por_alguma_resposta(self):
        self.assertEqual(sorted(set(ACOES_POR_TAG) - TAGS_OBSERVAVEIS), [])

    def test_decreto_12976_so_para_plataforma_ou_app(self):
        plataforma = _acoes({"online": "Sim — plataforma / app"})
        self.assertTrue({"deepfake", "violencia_genero"} <= plataforma)
        for perfil in ({"online": "Sim — site institucional"}, {"online": "Não"},
                       {"setor": "Mídia / Comunicação"}, {"usa_ia": "Sim"}):
            self.assertFalse({"deepfake", "violencia_genero"} & _acoes(perfil), perfil)

    def test_enquadramento_cobre_os_conceitos_exigidos(self):
        t = ENQUADRAMENTO_DECRETO_12976
        for termo in ("questionário não confirma", "intermedeia", "inteligência artificial",
                      "4º", "5º", "8º", "7º", "9º", "10", "art. 6º", "art. 12", "duas horas"):
            self.assertIn(termo, t)

    def test_enquadramento_nao_se_repete_nas_acoes(self):
        for tag in ("deepfake", "violencia_genero"):
            self.assertNotIn("Verifique o enquadramento", ACOES_POR_TAG[tag]["acao"])

    def test_relatorio_mostra_o_enquadramento_uma_vez_e_so_quando_cabe(self):
        perfil = {"online": "Sim — plataforma / app", "setor": "Outro"}
        html = gerar_relatorio_html(gerar_radar(perfil, NORMAS, ARESTAS), perfil)
        self.assertEqual(html.count("Verifique o enquadramento"), 1)
        perfil = {"online": "Sim — site institucional", "setor": "Outro"}
        html = gerar_relatorio_html(gerar_radar(perfil, NORMAS, ARESTAS), perfil)
        self.assertEqual(html.count("Verifique o enquadramento"), 0)

    def test_relatorio_mostra_o_enquadramento_antes_das_acoes(self):
        perfil = {"online": "Sim — plataforma / app", "setor": "Outro"}
        html = gerar_relatorio_html(gerar_radar(perfil, NORMAS, ARESTAS), perfil)
        pos_aviso = html.index("Verifique o enquadramento")
        pos_titulo = html.index("Ações Recomendadas")
        primeira_acao = ACOES_POR_TAG["deepfake"]["acao"][:40]
        self.assertLess(pos_titulo, pos_aviso)
        self.assertLess(pos_aviso, html.index(primeira_acao))

    def test_tela_mostra_o_enquadramento_uma_vez_e_antes_das_acoes(self):
        chamadas = []

        class _Col:
            def metric(self, *a, **k):
                pass

        @contextmanager
        def _expander(*a, **k):
            yield

        st_falso = mock.MagicMock()
        st_falso.markdown.side_effect = lambda t, *a, **k: chamadas.append(("markdown", t))
        st_falso.info.side_effect = lambda t, *a, **k: chamadas.append(("info", t))
        st_falso.caption.side_effect = lambda t, *a, **k: chamadas.append(("caption", t))
        st_falso.columns.side_effect = lambda n: [_Col() for _ in range(n)]
        st_falso.expander.side_effect = _expander
        perfil = {"online": "Sim — plataforma / app", "setor": "Outro"}
        with mock.patch.object(conformidade, "st", st_falso):
            conformidade.render_radar(gerar_radar(perfil, NORMAS, ARESTAS))
        textos = [t for _, t in chamadas]
        avisos = [i for i, t in enumerate(textos) if "Verifique o enquadramento" in t]
        self.assertEqual(len(avisos), 1)
        titulo = textos.index("#### Ações recomendadas")
        primeira = next(i for i, t in enumerate(textos) if ACOES_POR_TAG["deepfake"]["acao"][:40] in t)
        self.assertLess(titulo, avisos[0])
        self.assertLess(avisos[0], primeira)

    def test_ordem_das_acoes_e_deterministica(self):
        perfil = {"setor": "Escritório de Advocacia / Jurídico", "usa_ia": "Sim",
                  "trata_dados": "Sim — ambos", "online": "Sim — plataforma / app"}
        acoes = _gerar_acoes(perfil)
        ordem = {"critica": 0, "alta": 1, "media": 2, "baixa": 3}
        chaves = [(ordem[a["prioridade"]], a["tag_origem"], a["acao"]) for a in acoes]
        self.assertEqual(chaves, sorted(chaves))

    def test_etica_ia_rotulada_na_tela_e_no_relatorio(self):
        a = ACOES_POR_TAG["etica_ia"]
        self.assertTrue(a["acao"].startswith("Boa prática (não é obrigação vigente)"))
        self.assertIn("referência ética", a["base"])
        perfil = {"usa_ia": "Sim"}
        html = gerar_relatorio_html(gerar_radar(perfil, NORMAS, ARESTAS), perfil)
        self.assertIn("Boa prática (não é obrigação vigente)", html)
        self.assertIn("referência ética", html)

    def test_acoes_do_decreto_nao_se_repetem(self):
        d, v = ACOES_POR_TAG["deepfake"]["acao"], ACOES_POR_TAG["violencia_genero"]["acao"]
        self.assertIn("2h", d)
        self.assertNotIn("2h", v)
        self.assertIn("Ligue 180", v)
        self.assertIn("manifestamente ilegal (art. 12, I)", d)

    def test_etica_ia_para_quem_usa_ou_avalia_ia(self):
        self.assertIn("etica_ia", _acoes({"usa_ia": "Sim"}))
        self.assertIn("etica_ia", _acoes({"usa_ia": "Estou avaliando"}))
        self.assertNotIn("etica_ia", _acoes({"usa_ia": "Não"}))
        self.assertIn("não é obrigação vigente", ACOES_POR_TAG["etica_ia"]["acao"])


class TestTagsDoPerfil(unittest.TestCase):
    def test_toda_tag_do_perfil_corresponde_a_norma_ou_acao(self):
        usadas = set(ACOES_POR_TAG) | {t for v in NORMA_TAGS.values() for t in v}
        usadas |= {t for n in NORMAS for t in n.get("temas", [])}
        self.assertEqual(sorted(TAGS_OBSERVAVEIS - usadas), [])

    def test_governanca_e_compliance_nao_sao_mais_emitidas(self):
        self.assertFalse({"governanca", "compliance"} & TAGS_OBSERVAVEIS)


class TestEscopoDaIntersecao(unittest.TestCase):
    def test_tema_fora_do_questionario_nao_altera_o_percentual(self):
        norma = {"id": "x_teste", "status": "vigente", "tipo": "lei", "temas": ["dados_pessoais"]}
        com_extra = dict(norma, temas=["dados_pessoais", "tema_que_o_questionario_nao_avalia"])
        perfil = {"dados_pessoais", "consentimento"}
        self.assertEqual(_score_norma(norma, perfil), _score_norma(com_extra, perfil))

    def test_temas_fora_do_questionario_com_valor_literal(self):
        self.assertIn("deepfake", TAGS_OBSERVAVEIS)
        self.assertIn("dados_pessoais", TAGS_OBSERVAVEIS)
        self.assertNotIn("tema_inexistente_no_questionario", TAGS_OBSERVAVEIS)
        norma = {"id": "x_lit", "status": "vigente", "tipo": "lei", "nome": "X",
                 "temas": ["dados_pessoais", "tema_fora_a", "tema_fora_b"]}
        radar = gerar_radar({"trata_dados": "Sim — clientes"}, [norma], [])
        self.assertEqual(radar["normas"][0]["temas_fora_do_questionario"], 2)

    def test_norma_so_com_temas_fora_do_questionario_nao_entra(self):
        # Comportamento documentado: sem nenhum tema avaliável, a norma não pontua
        # e não aparece no quadro (não há o que comparar com o perfil).
        norma = {"id": "x_fora", "status": "vigente", "tipo": "lei", "nome": "X",
                 "temas": ["tema_fora_a"]}
        self.assertEqual(gerar_radar({"trata_dados": "Sim — clientes"}, [norma], [])["normas"], [])

    def test_tag_so_de_acao_nao_dilui_a_nota(self):
        # etica_ia só aciona ação (a única norma com ela está fora da pontuação):
        # responder "Usa IA: Sim" não pode baixar a nota por causa dela.
        com = {"id": "x_ia", "status": "tramitacao", "tipo": "pl", "nome": "X",
               "temas": ["inteligencia_artificial"]}
        radar = gerar_radar({"usa_ia": "Estou avaliando"}, [com], [])
        self.assertEqual(radar["normas"][0]["pct"], 100)
        self.assertIn("etica_ia", {a["tag_origem"] for a in radar["acoes"]})

    def test_radar_informa_os_temas_fora_do_questionario(self):
        radar = gerar_radar({"setor": "Fintech / Serviços Financeiros", "trata_dados": "Sim — clientes"},
                            NORMAS, ARESTAS)
        lgpd = next(n for n in radar["normas"] if n["id"] == "lgpd")
        esperado = len(_tags_norma("lgpd", next(n for n in NORMAS if n["id"] == "lgpd")) - TAGS_OBSERVAVEIS)
        self.assertEqual(lgpd["temas_fora_do_questionario"], esperado)

    def test_magnifica_humanitas_fora_do_conjunto_pontuado(self):
        self.assertIn("magnifica_humanitas", FORA_DA_PONTUACAO)
        self.assertTrue(any(n["id"] == "magnifica_humanitas" for n in NORMAS))  # continua no corpus
        for usa_ia in ("Sim", "Estou avaliando"):
            radar = gerar_radar({"usa_ia": usa_ia, "setor": "Outro"}, NORMAS, ARESTAS)
            self.assertNotIn("magnifica_humanitas", {n["id"] for n in radar["normas"]})

    def test_percentual_chega_a_100_e_nao_passa(self):
        tags = {"dados_pessoais", "consentimento"}
        # igualdade exata de temas, sem bônus de vigência: exatamente 100%
        nao_vigente = {"id": "x1", "status": "tramitacao", "tipo": "pl", "temas": sorted(tags)}
        self.assertEqual(_score_norma(nao_vigente, tags), 1.0)
        # com o bônus de 1,1 da vigência passaria de 100% sem o limite
        vigente = dict(nao_vigente, id="x2", status="vigente")
        self.assertEqual(_score_norma(vigente, tags), 1.0)

    def test_constituicao_sem_tema_em_comum_e_rotulada_como_base(self):
        perfil = {"setor": "Comércio Exterior / Exportação", "usa_ia": "Não", "trata_dados": "Não",
                  "online": "Não", "porte": "Startup / MEI"}
        radar = gerar_radar(perfil, NORMAS, ARESTAS)
        cf = [n for n in radar["normas"] if n["tipo"] == "constituicao"]
        for n in cf:
            self.assertEqual(n["base_constitucional"], not n["tags_match"])
        self.assertTrue(any(n["base_constitucional"] for n in cf))  # caso real: cf88 sem tema em comum
        self.assertIn("base constitucional, sem tema em comum", gerar_relatorio_html(radar, perfil))

    def test_relatorio_mostra_temas_fora_do_questionario(self):
        perfil = {"setor": "Fintech / Serviços Financeiros", "trata_dados": "Sim — clientes"}
        html = gerar_relatorio_html(gerar_radar(perfil, NORMAS, ARESTAS), perfil)
        self.assertIn("Temas fora do questionário", html)


if __name__ == "__main__":
    unittest.main()
