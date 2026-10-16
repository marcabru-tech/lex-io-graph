"""Travas de regressão do conteúdo jurídico prescritivo (PR 1).

Fontes primárias conferidas em 16/10/2026:
- LGPD (Lei 13.709/2018, texto compilado no Planalto): arts. 6º, 7º, 11, 14, 18, 20, 41, 42, 52.
- Marco Civil (Lei 12.965/2014): arts. 13 e 15.
- ECA Digital (Lei 15.211/2025): arts. 1º, 9º, 12, 18, 24, 29.
- Decreto 12.976/2026 (DOU de 21/05/2026): arts. 3º, 7º, 9º, 10 e 12.
- STJ, AREsp 2.130.619/SP (2ª Turma, 07/03/2023; Informativo 766).

As estruturas são lidas por análise estática (ast), sem importar Streamlit.
"""
import ast
import json
import re
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
REGISTROS_STJ = ("stj_resp", "stj_resp_plat", "stj_menor_online")


def _literal(caminho, nome):
    arvore = ast.parse(caminho.read_text(encoding="utf-8"))
    for no in arvore.body:
        if isinstance(no, ast.Assign) and any(
            isinstance(alvo, ast.Name) and alvo.id == nome for alvo in no.targets
        ):
            return ast.literal_eval(no.value)
    raise AssertionError(f"{nome} não encontrado em {caminho}")


ACOES = _literal(RAIZ / "lib" / "conformidade.py", "ACOES_POR_TAG")
RISCOS = _literal(next((RAIZ / "pages").glob("4_*.py")), "riscos")


def _textos_exibidos():
    """Todo texto de lib/, pages/ e data/ (exceto snapshots gerados)."""
    arquivos = list((RAIZ / "lib").rglob("*.py")) + list((RAIZ / "pages").glob("*.py"))
    arquivos += [
        RAIZ / "data" / "normas.json",
        RAIZ / "data" / "jurisprudencia.json",
        RAIZ / "data" / "arestas.json",
    ]
    return {a: a.read_text(encoding="utf-8") for a in arquivos}


def _json(nome):
    with open(RAIZ / "data" / nome, encoding="utf-8") as f:
        return json.load(f)


def _arestas():
    dados = _json("arestas.json")
    return dados if isinstance(dados, list) else next(
        v for v in dados.values() if isinstance(v, list)
    )


class TestCitacoesInexistentes(unittest.TestCase):
    def test_sem_clt_227a(self):
        for arquivo, texto in _textos_exibidos().items():
            self.assertNotIn("227-A", texto, arquivo.name)

    def test_sem_lgpd_art_14_inciso_I(self):
        for arquivo, texto in _textos_exibidos().items():
            self.assertNotIn("art. 14, I ", texto, arquivo.name)
            self.assertNotIn("art. 14, I +", texto, arquivo.name)

    def test_radar_sem_trf4_nem_adi_5527(self):
        texto = json.dumps(RISCOS, ensure_ascii=False)
        self.assertNotIn("TRF-4", texto)
        self.assertNotIn("ADI 5527", texto)


class TestMatrizConformidade(unittest.TestCase):
    def test_revisao_humana_nao_atribuida_ao_art_20(self):
        for chave, item in ACOES.items():
            if "art. 20" in item["base"]:
                self.assertNotRegex(
                    item["acao"].lower(), r"(garantir|implementar)[^.]*revisão humana", chave
                )
        for risco in RISCOS:
            self.assertNotIn("revisão humana conforme LGPD art. 20", risco["acao"])

    def test_dados_sensiveis_com_hipoteses_do_art_11_II(self):
        self.assertIn("art. 11, II", ACOES["dados_sensiveis"]["acao"])

    def test_guarda_de_logs_distingue_arts_13_e_15(self):
        acao = ACOES["guarda_logs"]["acao"]
        self.assertIn("art. 15", acao)
        self.assertIn("art. 13", acao)
        self.assertIn("6 meses", acao)

    def test_deepfake_com_os_tres_prazos_e_a_alternativa(self):
        acao = ACOES["deepfake"]["acao"]
        for prazo in ("2h", "6h", "24h"):
            self.assertIn(prazo, acao)
        self.assertIn("fundamento da manutenção", acao)
        self.assertIn("Até regulamentação", acao)
        self.assertNotIn("Detector", acao)

    def test_consentimento_parental_condicionado(self):
        acao = ACOES["consentimento_pais"]["acao"]
        self.assertIn("melhor interesse", acao)
        self.assertIn("Quando a base for o consentimento", acao)

    def test_referencias_nao_vigentes_rotuladas(self):
        for chave, item in ACOES.items():
            base = item["base"]
            if re.search(r"\bPL \d|NIST|Magnifica", base):
                self.assertTrue(
                    "Referência" in base or "referência" in base or "em tramitação" in base,
                    f"{chave}: {base}",
                )

    def test_acao_sem_base_vigente_comeca_com_boa_pratica(self):
        for chave, item in ACOES.items():
            if item["base"].startswith("Referência, não obrigação vigente"):
                self.assertTrue(item["acao"].startswith("Boa prática"), chave)


class TestTeseDeDanoPresumido(unittest.TestCase):
    """Reprova a afirmação de que vazamento gera dano moral presumido,
    sem proibir o termo "in re ipsa" em uso correto e contextualizado."""

    PADRAO = re.compile(
        r"vazamento[^.]{0,80}?gera dano moral (in re ipsa|presumido)", re.IGNORECASE
    )

    def test_nenhum_texto_afirma_dano_presumido_por_vazamento(self):
        for arquivo, texto in _textos_exibidos().items():
            for m in self.PADRAO.finditer(texto):
                trecho = texto[max(0, m.start() - 40): m.end()]
                self.assertRegex(trecho.lower(), r"não gera|nao gera", f"{arquivo.name}: {trecho}")

    def test_registros_pendentes_sem_tese_nem_aresp(self):
        nos = {n["id"]: n for n in _json("normas.json")["nodes"]}
        juris = {j["id"]: j for j in _json("jurisprudencia.json")["jurisprudencia"]}
        for rid in REGISTROS_STJ:
            textos = [juris[rid]["resumo"], juris[rid]["impacto_dev_junior"]]
            if rid in nos:
                textos += [nos[rid]["ementa"], nos[rid]["historia"]]
            for texto in textos:
                self.assertNotIn("in re ipsa", texto.lower(), rid)
                self.assertNotIn("2.130.619", texto, rid)
                self.assertNotIn("Relator", texto, rid)
                self.assertNotIn("Estabeleceu", texto, rid)


class TestRegistrosStjPendentes(unittest.TestCase):
    def test_estado_permanece_pendente(self):
        juris = {j["id"]: j for j in _json("jurisprudencia.json")["jurisprudencia"]}
        for rid in REGISTROS_STJ:
            self.assertEqual(juris[rid]["estado_verificacao"], "pendente", rid)

    def test_ano_nao_inferido(self):
        juris = {j["id"]: j for j in _json("jurisprudencia.json")["jurisprudencia"]}
        nos = {n["id"]: n for n in _json("normas.json")["nodes"]}
        for rid in REGISTROS_STJ:
            self.assertIsNone(juris[rid]["ano"], rid)
            if rid in nos:
                self.assertIsNone(nos[rid]["ano"], rid)


class TestArestasEcaDigital(unittest.TestCase):
    def test_remocao_nao_cita_art_18(self):
        for aresta in _arestas():
            if "eca_digital" in (aresta["source"], aresta["target"]):
                texto = (aresta.get("descricao", "") + " " + aresta.get("artigos", "")).lower()
                if "remoção" in texto or "remocao" in texto:
                    self.assertNotIn("art. 18", aresta.get("artigos", ""), aresta)

    def test_lgpd_eca_digital_sem_art_12(self):
        aresta = next(
            a for a in _arestas() if a["source"] == "lgpd" and a["target"] == "eca_digital"
        )
        self.assertNotIn("art. 12", aresta["artigos"])


if __name__ == "__main__":
    unittest.main()
