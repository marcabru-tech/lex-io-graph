"""Travas de regressão da revisão factual de 20/10/2026.

Mesmo padrão de tests/test_edicao_editorial.py, mas a varredura inclui os
dados (data/*.json) e a Teoria dos Conjuntos (docs/), onde estava a maior
parte das frases corrigidas. Leitura de texto puro, sem rede.
"""
import json
import unittest
from pathlib import Path

from lib.constants import STATUS_LABELS
from lib.hermeneutica import FONTES_DIREITO

RAIZ = Path(__file__).resolve().parent.parent

ARQUIVOS = (
    list((RAIZ / "lib").glob("*.py"))
    + list((RAIZ / "pages").glob("*.py"))
    + [RAIZ / "app.py"]
    + list((RAIZ / "data").glob("*.json"))
    + list((RAIZ / "docs").glob("*.html"))
)

# Frases que não podem voltar em nenhum arquivo.
PROIBIDAS = (
    "cidadãos europeus",
    "usuários europeus",
    "proibições absolutas",
    "Proibições absolutas",
    "sancionada em 21/05/2026",
    "LGPD compliant",
    "Em tramitação no Senado Federal desde 2023",
    "primeiro marco regulatório de IA do mundo",
    "Primeiro marco regulatório de IA do mundo",
    "autarquia federal independente",
    "Inclui IA e algoritmos como fatores de risco",
    "incluir explicitamente IA",
    "riscos psicossociais de IA",
    "revogando parcialmente o Decreto 8.771",
    "regulamentou o tema pelos",
    "Deveres regulamentados pelos",
    "súmulas vinculantes do STF têm força de lei",
    "dano in re ipsa por vazamento",
)


def _normas() -> dict:
    nos = json.loads((RAIZ / "data" / "normas.json").read_text(encoding="utf-8"))["nodes"]
    return {n["id"]: n for n in nos}


def _texto_do_no(no: dict) -> str:
    return json.dumps(no, ensure_ascii=False)


class TestFrasesCorrigidas(unittest.TestCase):
    def test_frases_corrigidas_nao_retornam(self):
        for arquivo in ARQUIVOS:
            texto = arquivo.read_text(encoding="utf-8")
            for frase in PROIBIDAS:
                self.assertNotIn(frase, texto, f"{arquivo.name}: {frase}")

    def test_forca_de_lei_fora_da_jurisprudencia(self):
        # "Força de lei" é termo correto para medida provisória (CF, art. 62);
        # a trava vale para a descrição da jurisprudência, onde estava o erro.
        jur = next((f for f in FONTES_DIREITO["fontes"] if f["nome"].startswith("Jurisprudência")), None)
        self.assertIsNotNone(jur, "fonte 'Jurisprudência' ausente de FONTES_DIREITO")
        self.assertNotIn("força de lei", jur["descricao"])
        self.assertIn("CF, art. 103-A", jur["descricao"])
        self.assertIn("CPC, art. 927", jur["descricao"])

    def test_cadastro_da_lei_15409_sem_tempo_real(self):
        no = _normas().get("lei_15409_2026")
        self.assertIsNotNone(no, "nó lei_15409_2026 ausente")
        texto = _texto_do_no(no)
        self.assertNotIn("tempo real", texto)
        self.assertIn("Lei 15.409, de 20/05/2026, publicada no DOU de 21/05/2026", texto)
        self.assertIn("60 dias após a publicação", texto)
        self.assertIn("regulamento", texto)


class TestPl2338(unittest.TestCase):
    def test_aprovado_no_senado_e_em_tramitacao(self):
        no = _normas().get("pl_ia")
        self.assertIsNotNone(no, "nó pl_ia ausente")
        self.assertEqual(no["status"], "tramitacao")
        self.assertIn("Aprovado pelo Senado Federal em 10/12/2024", no["historia"])
        self.assertIn("remetido à Câmara dos Deputados", no["historia"])


class TestDecisoesNaoVerificadas(unittest.TestCase):
    """Registro não verificado em jurisprudencia.json não é precedente vigente."""

    def test_status_em_conferencia_para_registro_nao_verificado(self):
        self.assertIn("em_conferencia", STATUS_LABELS)
        juris = json.loads((RAIZ / "data" / "jurisprudencia.json").read_text(encoding="utf-8"))
        estados = {r["id"]: r.get("estado_verificacao") for r in juris["jurisprudencia"]}
        nos = _normas()
        conferidos = 0
        for rid, estado in estados.items():
            if rid not in nos or estado == "verificado":
                continue
            conferidos += 1
            self.assertEqual(nos[rid]["status"], "em_conferencia", f"{rid} ({estado})")
        self.assertGreaterEqual(conferidos, 3)

    def test_tres_registros_seguem_nao_verificados(self):
        juris = json.loads((RAIZ / "data" / "jurisprudencia.json").read_text(encoding="utf-8"))
        estados = {r["id"]: r.get("estado_verificacao") for r in juris["jurisprudencia"]}
        for rid in ("stf_adimc", "stj_resp", "stj_resp_plat"):
            self.assertIn(estados.get(rid), ("pendente", "contestado"), rid)


if __name__ == "__main__":
    unittest.main()
