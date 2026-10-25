"""Jurisprudência sobre julgados inventados por IA (decisão da Luna, 25/10/2026): quatro registros pendentes."""
import json
import unittest
from pathlib import Path

from lib.ipii.matcher import calcular_todas_intersecoes, excluida_do_ipii
from lib.ipii.tokenizer import tokenizar_corpus
from lib.validacao import _NUMERO_CNJ, digito_cnj, validar_corpus, validar_jurisprudencia

RAIZ = Path(__file__).resolve().parent.parent
JURIS = {r["id"]: r for r in json.loads((RAIZ / "data" / "jurisprudencia.json").read_text(encoding="utf-8"))["jurisprudencia"]}
NORMAS = json.loads((RAIZ / "data" / "normas.json").read_text(encoding="utf-8"))["nodes"]
NOS = {n["id"]: n for n in NORMAS}
NOVOS = {
    "tse_respel_0600359_pr": ("TSE", "0600359-43.2024.6.16.0150", "2025-02-13"),
    "tse_agr_0600528_sp": ("TSE", "0600528-12.2024.6.26.0163", "2026-05-28"),
    "tse_ed_0600528_sp": ("TSE", "0600528-12.2024.6.26.0163", "2026-08-20"),
    "tst_rr_0000284_pe": ("TST", "0000284-92.2024.5.06.0351", "2026-02-25"),
}


class TestRegistros(unittest.TestCase):
    def test_quatro_registros_pendentes_um_por_acordao(self):
        for rid, (tribunal, numero, data) in NOVOS.items():
            r = JURIS[rid]
            with self.subTest(rid=rid):
                self.assertEqual(r["estado_verificacao"], "pendente")
                self.assertEqual(r["tribunal"], tribunal)
                self.assertIn(numero, r["numero"])
                self.assertEqual(r["data_julgamento"], data)
                self.assertTrue(r["proveniencia"]["origem"])
                self.assertIn("ADR 007", r["proveniencia"]["observacao"])

    def test_digito_cnj_confere(self):
        for rid in NOVOS:
            m = _NUMERO_CNJ.search(JURIS[rid]["numero"])
            seq, dv, ano, seg, tr, org = m.groups()
            self.assertEqual(int(dv), digito_cnj(seq, ano, seg, tr, org), rid)

    def test_normas_relacionadas_so_com_ids_do_corpus(self):
        for rid in NOVOS:
            self.assertLessEqual(set(JURIS[rid]["normas_relacionadas"]), set(NOS), rid)

    def test_divergencia_do_valor_da_multa_registrada(self):
        # A divergência foi resolvida pela leitura dos acórdãos: vale a decisão monocrática (5 SM);
        # os embargos citam R$ 5.000,00 só em obiter dictum.
        self.assertIn("obiter dictum", JURIS["tse_agr_0600528_sp"]["proveniencia"]["observacao"])
        self.assertIn("5 salários mínimos", JURIS["tse_ed_0600528_sp"]["proveniencia"]["observacao"])
        self.assertIn("5 salários mínimos", JURIS["tse_agr_0600528_sp"]["resumo"])
        self.assertIn("R$ 5.000,00", JURIS["tse_ed_0600528_sp"]["resumo"])

    def test_divergencia_tse_tst_sobre_o_advogado(self):
        self.assertIn("só as partes respondem", JURIS["tse_respel_0600359_pr"]["resumo"])
        self.assertIn("ao advogado subscritor", JURIS["tst_rr_0000284_pe"]["resumo"])
        # O contraste é leitura do Lexiograph, não conteúdo do acórdão do TST (revisão independente).
        self.assertNotIn("tse_respel", JURIS["tst_rr_0000284_pe"]["resumo"])
        self.assertIn("Nota editorial do Lexiograph (não consta do acórdão)",
                      JURIS["tst_rr_0000284_pe"]["proveniencia"]["observacao"])

    def test_tst_artigos_por_sancao(self):
        r = JURIS["tst_rr_0000284_pe"]["resumo"]
        parte, advogado = r.split("Aplicou também ao advogado")
        self.assertNotIn("139", parte)  # o art. 139, III fundamenta só a penalidade ao advogado
        self.assertIn("CPC, arts. 77, I e II, e 80, I e II", parte)
        self.assertIn("139, III", advogado)
        self.assertIn("possível infração ao art. 34", r)
        self.assertIn("apenas como hipótese", r)
        self.assertEqual(JURIS["tst_rr_0000284_pe"]["relator"], "Min. Antônio Fabrício de Matos Gonçalves")

    def test_datas_de_publicacao_do_portal(self):
        self.assertEqual(JURIS["tst_rr_0000284_pe"]["data_publicacao"], "2026-03-03")
        self.assertEqual(JURIS["tse_ed_0600528_sp"]["data_publicacao"], "2026-08-28")
        self.assertEqual(JURIS["tse_agr_0600528_sp"]["data_publicacao"], "2026-06-10")
        self.assertEqual(JURIS["tse_respel_0600359_pr"]["data_publicacao"], "2025-05-22")

    def test_situacao_processual_registrada(self):
        self.assertIn("trânsito em julgado em 21/08/2025", JURIS["tse_respel_0600359_pr"]["proveniencia"]["observacao"])
        for rid in ("tse_agr_0600528_sp", "tse_ed_0600528_sp"):
            self.assertIn("recurso extraordinário interposto em 31/08/2026", JURIS[rid]["proveniencia"]["observacao"], rid)

    def test_tese_3_completa(self):
        self.assertIn("e/ou pelo respectivo órgão de classe, a quem a autoridade judicial oficiará",
                      JURIS["tse_respel_0600359_pr"]["resumo"])

    def test_valor_da_multa_que_vale(self):
        self.assertIn("5 salários mínimos, fixado na decisão monocrática e mantido",
                      JURIS["tse_agr_0600528_sp"]["proveniencia"]["observacao"])
        self.assertIn("apenas em obiter dictum", JURIS["tse_agr_0600528_sp"]["proveniencia"]["observacao"])

    def test_nos_sem_atribuir_ia_onde_o_acordao_nao_constatou(self):
        self.assertNotIn("IA", NOS["tst_rr_0000284_pe"]["nome"])
        self.assertNotIn("IA", NOS["tse_agr_0600528_sp"]["nome"])
        for rid in NOVOS:
            self.assertIn(JURIS[rid]["resumo"], NOS[rid]["ementa"], rid)

    def test_precedente_sem_inteiro_teor_nao_vira_registro(self):
        self.assertFalse(any("0600016" in r["numero"] for r in JURIS.values()))
        self.assertFalse(any("1001128-84.2024.5.02.0044" in json.dumps(r) for r in JURIS.values()))


class TestNosEIpii(unittest.TestCase):
    def test_nos_em_conferencia(self):
        for rid in NOVOS:
            n = NOS[rid]
            self.assertEqual((n["tipo"], n["status"]), ("jurisprudencia", "em_conferencia"), rid)

    def test_fora_do_ipii(self):
        tokens = tokenizar_corpus(NORMAS)
        for rid in NOVOS:
            self.assertTrue(excluida_do_ipii(tokens[rid]), rid)
        pares = {p for r in calcular_todas_intersecoes(tokens) for p in (r["source"], r["target"])}
        self.assertFalse(pares & set(NOVOS))

    def test_validacao_sem_erros(self):
        self.assertEqual(validar_corpus(), [])
        erros, _ = validar_jurisprudencia()
        self.assertEqual(erros, [])


if __name__ == "__main__":
    unittest.main()
