"""Norma com status em_conferencia não gera sugestão de ligação no IPII.

Decisão de produto: decisão judicial não verificada em fonte oficial não pode
servir de base para propor aresta. Corpus mínimo, sem ler data/.
"""
import unittest

from lib.ipii.matcher import STATUS_EXCLUIDOS_DO_IPII, calcular_todas_intersecoes
from lib.ipii.tokenizer import tokenizar_corpus
from lib.ipii.validator import validar_arestas


def _norma(id_: str, status: str, tipo: str = "lei") -> dict:
    # Mesmo conteúdo para todas: o par só não sai por causa do status.
    return {
        "id": id_, "tipo": tipo, "status": status, "ano": 2024,
        "temas": ["dados_pessoais", "internet"],
        "ementa": "Proteção de dados pessoais de usuários de plataformas digitais",
        "direito_comparado": "GDPR europeu e CCPA da Califórnia",
        "autores": [{"nome": "Dworkin", "obra": "Law's Empire", "contribuicao": "integridade"}],
        "latim": [{"original": "Ubi ius ibi remedium"}],
    }


def _ids(sugeridas: list) -> set:
    return {i for s in sugeridas for i in (s["source"], s["target"])}


class TestExclusaoDoIpii(unittest.TestCase):
    def setUp(self):
        self.assertIn("em_conferencia", STATUS_EXCLUIDOS_DO_IPII)

    def test_norma_em_conferencia_nao_aparece_em_sugestao(self):
        corpus = [
            _norma("lei_a", "vigente"),
            _norma("lei_b", "vigente"),
            _norma("decisao_x", "em_conferencia", tipo="jurisprudencia"),
        ]
        sugeridas = calcular_todas_intersecoes(tokenizar_corpus(corpus), threshold=0.0)
        self.assertNotIn("decisao_x", _ids(sugeridas))
        self.assertEqual([(s["source"], s["target"]) for s in sugeridas], [("lei_a", "lei_b")])

    def test_controle_mesma_norma_vigente_seria_sugerida(self):
        corpus = [
            _norma("lei_a", "vigente"),
            _norma("decisao_x", "vigente", tipo="jurisprudencia"),
        ]
        sugeridas = calcular_todas_intersecoes(tokenizar_corpus(corpus))
        self.assertIn("decisao_x", _ids(sugeridas))

    def test_pontuacao_dos_demais_pares_nao_muda(self):
        base = [_norma("lei_a", "vigente"), _norma("lei_b", "tramitacao", tipo="pl")]
        com_excluida = base + [_norma("decisao_x", "em_conferencia", tipo="jurisprudencia")]
        sem = calcular_todas_intersecoes(tokenizar_corpus(base), threshold=0.0)
        com = calcular_todas_intersecoes(tokenizar_corpus(com_excluida), threshold=0.0)
        self.assertEqual(sem, com)

    def test_aresta_existente_com_norma_excluida_fica_fora_da_cobertura(self):
        corpus = [_norma("lei_a", "vigente"), _norma("lei_b", "vigente"),
                  _norma("decisao_x", "em_conferencia", tipo="jurisprudencia")]
        tokens = tokenizar_corpus(corpus)
        sugeridas = calcular_todas_intersecoes(tokens)
        existentes = [
            {"source": "lei_a", "target": "lei_b", "tipo": "intersecao"},
            {"source": "lei_a", "target": "decisao_x", "tipo": "interpreta", "descricao": "x"},
        ]
        r = validar_arestas(sugeridas, existentes, frozenset({"decisao_x"}))
        self.assertEqual(r["total_existentes"], 1)
        self.assertEqual(r["faltando"], 0)
        self.assertEqual(r["cobertura"], 1.0)
        self.assertEqual([g["par"] for g in r["fora_do_ipii"]], ["lei_a ↔ decisao_x"])
        self.assertNotIn("decisao_x", " ".join(g["par"] for g in r["gap_engine"]))

    def test_validador_sem_excluidas_mantem_comportamento(self):
        existentes = [{"source": "a", "target": "b", "tipo": "intersecao"}]
        r = validar_arestas([], existentes)
        self.assertEqual((r["total_existentes"], r["faltando"], r["fora_do_ipii"]), (1, 1, []))


if __name__ == "__main__":
    unittest.main()
