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
        for rid in ("tse_agr_0600528_sp", "tse_ed_0600528_sp"):
            self.assertIn("Divergência", JURIS[rid]["proveniencia"]["observacao"], rid)
        self.assertIn("5 salários mínimos", JURIS["tse_agr_0600528_sp"]["resumo"])
        self.assertIn("R$ 5.000,00", JURIS["tse_ed_0600528_sp"]["resumo"])

    def test_divergencia_tse_tst_sobre_o_advogado(self):
        self.assertIn("só as partes respondem", JURIS["tse_respel_0600359_pr"]["resumo"])
        self.assertIn("ao advogado subscritor", JURIS["tst_rr_0000284_pe"]["resumo"])

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
