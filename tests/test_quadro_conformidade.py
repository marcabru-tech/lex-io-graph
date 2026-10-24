"""Quadro e relatório de conformidade (PR de conteúdo 1a, 24/10/2026).

Travas: registros em conferência e propostas em tramitação nunca aparecem como
"normas aplicáveis"; o relatório escapa todo valor, traz o aviso de triagem e
conta o corpus em vez de um número fixo; o cálculo não altera os dados do corpus.
"""
import copy
import unittest

from lib.conformidade import PERGUNTAS, gerar_radar, gerar_relatorio_html
from lib.graph_builder import load_json


def _perfil_amplo():
    perfil = {}
    for chave, pergunta in PERGUNTAS.items():
        opcoes = pergunta.get("opcoes") or pergunta.get("options") or []
        perfil[chave] = opcoes[1] if len(opcoes) > 1 else (opcoes[0] if opcoes else "")
    return perfil


class TestQuadro(unittest.TestCase):
    def setUp(self):
        self.normas = load_json("normas.json")["nodes"]
        self.arestas = load_json("arestas.json")["edges"]
        self.perfil = _perfil_amplo()

    def test_grupos_separam_vigente_proposta_e_em_conferencia(self):
        radar = gerar_radar(self.perfil, self.normas, self.arestas)
        for n in radar["normas"]:
            if n["status"] == "em_conferencia":
                self.assertEqual(n["grupo"], "em_conferencia", n["id"])
            elif n["status"] == "tramitacao":
                self.assertEqual(n["grupo"], "proposta", n["id"])
            else:
                self.assertEqual(n["grupo"], "vigente", n["id"])

    def test_arestas_com_proposta_ou_conferencia_nao_viram_risco_alto(self):
        radar = gerar_radar(self.perfil, self.normas, self.arestas)
        grupo = {n["id"]: n["grupo"] for n in radar["normas"]}
        for a in radar["arestas"]:
            g = {grupo.get(a["source"]), grupo.get(a["target"])}
            if "em_conferencia" in g:
                self.assertEqual(a["risco"], "em_conferencia")
            elif "proposta" in g:
                self.assertEqual(a["risco"], "prospectivo")

    def test_nao_altera_o_corpus(self):
        antes = copy.deepcopy(self.arestas)
        gerar_radar(self.perfil, self.normas, self.arestas)
        self.assertEqual(self.arestas, antes)

    def test_relatorio(self):
        radar = gerar_radar(self.perfil, self.normas, self.arestas)
        html = gerar_relatorio_html(radar, self.perfil)
        self.assertNotIn("18 normas", html)
        self.assertIn(f"Corpus curado: {len(self.normas)} normas", html)
        self.assertNotIn("Engine IPII", html, "o quadro é triagem temática, não usa o IPII")
        self.assertIn("não é certificação de conformidade", html)
        self.assertNotIn("Normas Aplicáveis", html)

    def test_relatorio_escapa_valores(self):
        radar = gerar_radar(self.perfil, self.normas, self.arestas)
        radar = copy.deepcopy(radar)
        radar["normas"][0]["nome"] = "<script>alert(1)</script>"
        html = gerar_relatorio_html(radar, self.perfil)
        self.assertNotIn("<script>alert(1)</script>", html)
        self.assertIn("&lt;script&gt;", html)


class TestTextosDaFerramenta(unittest.TestCase):
    def test_sem_tags_com_erro_de_digitacao(self):
        from pathlib import Path
        src = (Path(__file__).resolve().parent.parent / "lib" / "conformidade.py").read_text(encoding="utf-8")
        self.assertNotIn("neutridade", src)
        self.assertNotIn("viies", src)

    def test_radar_de_riscos_sem_dispositivo_inexistente(self):
        from pathlib import Path
        src = next((Path(__file__).resolve().parent.parent / "pages").glob("4_*Radar_Riscos.py")).read_text(encoding="utf-8")
        self.assertNotIn("Marco Civil art. 7º, 15", src)


if __name__ == "__main__":
    unittest.main()
