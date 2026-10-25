"""Quadro de conformidade: ações alcançáveis e escopo explícito da interseção temática."""
import json
import unittest
from pathlib import Path

from lib.conformidade import (ACOES_POR_TAG, FORA_DA_PONTUACAO, NORMA_TAGS, PERFIL_TEMA_MAP, TAGS_OBSERVAVEIS,
                              _gerar_acoes, _score_norma, _tags_norma, gerar_radar)

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

    def test_acoes_do_decreto_explicitam_a_condicao_de_aplicacao(self):
        for tag in ("deepfake", "violencia_genero"):
            self.assertIn("intermedeia conteúdo gerado por terceiros", ACOES_POR_TAG[tag]["acao"])
            self.assertIn("o questionário não confirma", ACOES_POR_TAG[tag]["acao"])
            self.assertIn("arts. 4º, 5º e 8º pressupõem intermediação", ACOES_POR_TAG[tag]["acao"])
            self.assertIn("os arts. 7º, 9º e 10 tratam de hipóteses específicas", ACOES_POR_TAG[tag]["acao"])

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

    def test_percentual_nunca_passa_de_100(self):
        perfil = {k: list(v)[0] for k, v in PERFIL_TEMA_MAP.items()}
        for n in gerar_radar(perfil, NORMAS, ARESTAS)["normas"]:
            self.assertLessEqual(n["pct"], 100)


if __name__ == "__main__":
    unittest.main()
