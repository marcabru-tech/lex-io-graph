"""Status referencia_etica (PR 7): fora do percentual, visível, sem hierarquia."""
import json
import unittest
from contextlib import contextmanager
from pathlib import Path
from unittest import mock

import lib.validacao as validacao
import lib.conformidade as conformidade
from lib.conformidade import (GRUPO_POR_STATUS, NORMA_TAGS, STATUS_FORA_DA_PONTUACAO, TAGS_OBSERVAVEIS,
                              _grupo, _score_norma, gerar_radar, gerar_relatorio_html)
from lib.constants import STATUS_COLORS, STATUS_LABELS, cor_borda_status, rotulo_status

RAIZ = Path(__file__).resolve().parent.parent
NORMAS = json.loads((RAIZ / "data" / "normas.json").read_text(encoding="utf-8"))["nodes"]
ARESTAS = json.loads((RAIZ / "data" / "arestas.json").read_text(encoding="utf-8"))["edges"]
MH = next(n for n in NORMAS if n["id"] == "magnifica_humanitas")


def _norma(id_, status, temas=("ia",), tipo="documento_internacional"):
    return {"id": id_, "nome": id_, "sigla": id_, "tipo": tipo, "ementa": "x", "status": status,
            "temas": list(temas), "orgao": "x", "ano": 2026}


class TestStatusReferenciaEtica(unittest.TestCase):
    def test_status_tem_rotulo_e_cor(self):
        self.assertEqual(STATUS_LABELS["referencia_etica"], "Referência ética (não vinculante)")
        self.assertIn("referencia_etica", STATUS_COLORS)
        self.assertEqual(rotulo_status("referencia_etica"), "Referência ética (não vinculante)")
        self.assertEqual(rotulo_status("valor_desconhecido"), "valor_desconhecido")

    def test_exclusao_do_percentual_e_pelo_status_nao_por_lista_de_ids(self):
        self.assertIn("referencia_etica", STATUS_FORA_DA_PONTUACAO)
        qualquer = _norma("documento_qualquer", "referencia_etica", temas=("dados_pessoais",))
        self.assertEqual(_score_norma(qualquer, {"dados_pessoais"}), 0.0)
        self.assertEqual(_grupo("referencia_etica"), "referencia")

    def test_instrumento_externo_mantem_a_pontuacao_e_ganha_grupo_proprio(self):
        acordo = _norma("acordo_x", "instrumento_externo", temas=("dados_pessoais",))
        self.assertGreater(_score_norma(acordo, {"dados_pessoais"}), 0.0)
        self.assertEqual(_grupo("instrumento_externo"), "nao_incorporado")
        self.assertNotEqual(_grupo("instrumento_externo"), "vigente")

    def test_instrumento_externo_aparece_na_secao_propria(self):
        acordo = _norma("acordo_x", "instrumento_externo", temas=("dados_pessoais",))
        acordo["nome"] = "Acordo X"
        perfil = {"trata_dados": "Sim — clientes"}
        radar = gerar_radar(perfil, [acordo], [])
        self.assertEqual(radar["normas"][0]["grupo"], "nao_incorporado")
        html = gerar_relatorio_html(radar, perfil)
        titulo = "Instrumentos externos — não incorporados ao direito brasileiro"
        self.assertIn(titulo, html)
        self.assertNotIn("Normas vigentes com interseção temática", html)
        self.assertLess(html.index(titulo), html.index("Acordo X"))


class TestGrupoExplicito(unittest.TestCase):
    def test_todo_status_conhecido_tem_grupo_declarado(self):
        self.assertEqual(sorted(set(STATUS_LABELS) - set(GRUPO_POR_STATUS)), [])

    def test_status_desconhecido_nao_vira_vigente(self):
        self.assertEqual(_grupo("valor_desconhecido"), "desconhecido")
        self.assertEqual(_grupo(""), "desconhecido")

    def test_status_desconhecido_aparece_a_parte_no_quadro(self):
        norma = _norma("x_desc", "status_inventado", temas=("dados_pessoais",), tipo="lei")
        radar = gerar_radar({"trata_dados": "Sim — clientes"}, [norma], [])
        self.assertEqual(radar["normas"][0]["grupo"], "desconhecido")
        html = gerar_relatorio_html(radar, {"trata_dados": "Sim — clientes"})
        self.assertIn("Status não reconhecido", html)


class TestCorDoStatus(unittest.TestCase):
    def test_borda_na_cor_do_status_para_referencia_e_instrumento_externo(self):
        self.assertEqual(cor_borda_status("referencia_etica", "#123456"), (STATUS_COLORS["referencia_etica"], 4))
        self.assertEqual(cor_borda_status("instrumento_externo", "#123456"), (STATUS_COLORS["instrumento_externo"], 4))
        self.assertEqual(cor_borda_status("vigente", "#123456"), ("#123456", 1))

    def test_grafo_usa_a_borda_do_status(self):
        pagina = (RAIZ / "pages" / "1_📊_Grafo_Normativo.py").read_text(encoding="utf-8")
        self.assertIn("cor_borda_status(", pagina)
        self.assertIn('"border": borda', pagina)


class TestVisibilidade(unittest.TestCase):
    PERFIL = {"usa_ia": "Sim", "setor": "Outro"}

    def test_referencia_aparece_a_parte_sem_percentual(self):
        radar = gerar_radar(self.PERFIL, NORMAS, ARESTAS)
        ids = {r["id"] for r in radar["referencias"]}
        self.assertIn("magnifica_humanitas", ids)
        self.assertNotIn("magnifica_humanitas", {n["id"] for n in radar["normas"]})
        ref = next(r for r in radar["referencias"] if r["id"] == "magnifica_humanitas")
        self.assertNotIn("pct", ref)
        self.assertEqual(ref["rotulo"], "Referência ética (não vinculante)")

    def test_correspondencia_vem_das_tags_curadas_do_quadro(self):
        # O tema "ia" do corpus não é emitido pelo questionário (que emite
        # "inteligencia_artificial"); a correspondência vem do NORMA_TAGS curado.
        self.assertNotIn("ia", TAGS_OBSERVAVEIS)
        self.assertIn("etica_ia", NORMA_TAGS["magnifica_humanitas"])
        ref = next(r for r in gerar_radar(self.PERFIL, NORMAS, ARESTAS)["referencias"]
                   if r["id"] == "magnifica_humanitas")
        self.assertIn("etica_ia", ref["tags_match"])

    def test_tela_mostra_a_secao_de_referencias(self):
        chamadas = []

        class _Col:
            def metric(self, *a, **k):
                pass

        @contextmanager
        def _expander(*a, **k):
            yield

        st_falso = mock.MagicMock()
        for nome in ("markdown", "caption", "info", "warning"):
            getattr(st_falso, nome).side_effect = (lambda n: lambda t, *a, **k: chamadas.append((n, t)))(nome)
        st_falso.columns.side_effect = lambda n: [_Col() for _ in range(n)]
        st_falso.expander.side_effect = _expander
        with mock.patch.object(conformidade, "st", st_falso):
            conformidade.render_radar(gerar_radar(self.PERFIL, NORMAS, ARESTAS))
        textos = [t for _, t in chamadas]
        self.assertIn("#### Referências não vinculantes relacionadas", textos)
        linha = next(t for t in textos if "Magnifica Humanitas" in t and "Referência ética" in t)
        self.assertNotIn("%", linha)

    def test_relatorio_mostra_a_referencia_com_o_rotulo(self):
        html = gerar_relatorio_html(gerar_radar(self.PERFIL, NORMAS, ARESTAS), self.PERFIL)
        self.assertIn("Referências não vinculantes relacionadas", html)
        self.assertIn("Referência ética (não vinculante)", html)

    def test_sem_tema_em_comum_nao_aparece(self):
        radar = gerar_radar({"setor": "Comércio Exterior / Exportação"}, NORMAS, ARESTAS)
        self.assertNotIn("magnifica_humanitas", {r["id"] for r in radar["referencias"]})


class TestHierarquiaBloqueada(unittest.TestCase):
    def _erros(self, arestas):
        normas = [_norma("ref", "referencia_etica"), _norma("lei_x", "vigente", tipo="lei"),
                  _norma("ext", "instrumento_externo")]
        dados = {"normas.json": {"nodes": normas}, "arestas.json": {"edges": arestas}}
        real = validacao._ler
        with mock.patch.object(validacao, "_ler", side_effect=lambda nome: dados.get(nome) or real(nome)):
            return [e for e in validacao.validar_corpus() if "hierarquia" in e]

    def _aresta(self, s, t, tipo="hierarquia"):
        return {"source": s, "target": t, "tipo": tipo, "descricao": "x", "artigos": "x"}

    def test_hierarquia_com_referencia_etica_e_bloqueada_nos_dois_sentidos(self):
        self.assertTrue(self._erros([self._aresta("ref", "lei_x")]))
        self.assertTrue(self._erros([self._aresta("lei_x", "ref")]))

    def test_relacao_tematica_continua_permitida(self):
        self.assertFalse(self._erros([self._aresta("ref", "lei_x", "complementaridade")]))

    def test_instrumento_externo_continua_bloqueado(self):
        self.assertTrue(self._erros([self._aresta("ext", "lei_x")]))

    def test_corpus_real_valido(self):
        self.assertEqual(validacao.validar_corpus(), [])


class TestConteudoDoNo(unittest.TestCase):
    def test_campos_congelados_pelo_adr_008(self):
        self.assertEqual(MH["sigla"], "Magnifica Humanitas (Leão XIV, 15/05/2026; apresentada em 25/05/2026)")
        self.assertEqual(MH["orgao"], "Santa Sé / Vaticano")
        self.assertEqual(MH["ano"], 2026)
        self.assertEqual(MH["tipo"], "documento_internacional")

    def test_sem_causalidade_nem_citacao_sem_fonte(self):
        texto = json.dumps(MH, ensure_ascii=False)
        self.assertNotIn("impacto direto", texto)
        self.assertNotIn("argumento central da encíclica", texto)
        self.assertNotIn("base filosófica da encíclica", texto)
        self.assertNotIn("Chris Olah", texto)  # volta só com fonte primária conferida
        self.assertIn("convergência temática", texto)

    def test_interpretacoes_identificadas(self):
        finnis = next(a for a in MH["autores"] if a["nome"] == "John Finnis")
        self.assertTrue(finnis["contribuicao"].startswith("Leitura do Lexiograph"))
        lex = next(l for l in MH["latim"] if l["original"] == "Lex iniusta non est lex")
        self.assertIn("Leitura do Lexiograph", lex["traducao_juridica"])

    def test_capitulos_tratados_como_temas(self):
        for item in MH["artigos_chave"]:
            self.assertTrue(item.startswith("Tema (síntese):"), item)


if __name__ == "__main__":
    unittest.main()
