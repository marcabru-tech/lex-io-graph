"""A6-g: limpeza final da auditoria (regex, legenda da CF, verificação do Google, equivalências)."""
import json
import unittest
from contextlib import contextmanager
from pathlib import Path
from unittest import mock

import lib.conformidade as conformidade
import lib.radar as radar
from lib.conformidade import TAGS_OBSERVAVEIS, _tags_norma, _tags_pontuaveis, gerar_radar
from lib.taxonomia import chave_proposicao

RAIZ = Path(__file__).resolve().parent.parent
NORMAS = json.loads((RAIZ / "data" / "normas.json").read_text(encoding="utf-8"))["nodes"]
ARESTAS = json.loads((RAIZ / "data" / "arestas.json").read_text(encoding="utf-8"))["edges"]


class TestRegexPontos(unittest.TestCase):
    def test_pontos_so_entre_digitos(self):
        self.assertEqual(chave_proposicao("PL 2..338/2023", pivo=26), [])
        self.assertEqual(chave_proposicao("PL 2.338./2023", pivo=26), [])
        self.assertEqual(chave_proposicao("PL 2.338/2023", pivo=26), ["PL 2338/2023"])
        self.assertEqual(chave_proposicao("PL 1.234.567/2023", pivo=26), ["PL 1234567/2023"])


class TestLegendaDaConstituicao(unittest.TestCase):
    PERFIL = {"setor": "Comércio Exterior / Exportação", "usa_ia": "Não", "trata_dados": "Não",
              "online": "Não", "porte": "Startup / MEI"}

    def test_base_constitucional_nao_cita_percentual(self):
        r = gerar_radar(self.PERFIL, NORMAS, ARESTAS)
        cf = next(n for n in r["normas"] if n["base_constitucional"])
        self.assertTrue(cf["temas_fora_do_questionario"])
        legendas = []

        class _Col:
            def metric(self, *a, **k):
                pass

        @contextmanager
        def _expander(titulo, *a, **k):
            legendas.append(("expander", titulo))
            yield

        st_falso = mock.MagicMock()
        st_falso.caption.side_effect = lambda t, *a, **k: legendas.append(("caption", t))
        st_falso.columns.side_effect = lambda n: [_Col() for _ in range(n)]
        st_falso.expander.side_effect = _expander
        with mock.patch.object(conformidade, "st", st_falso):
            conformidade.render_radar(r)
        i = next(k for k, (tipo, t) in enumerate(legendas) if tipo == "expander" and cf["nome"] in t)
        legenda = next(t for tipo, t in legendas[i + 1:] if tipo == "caption" and "tema(s) desta norma" in t)
        self.assertNotIn("percentual", legenda)
        # Norma com percentual continua citando o percentual.
        outra = [t for tipo, t in legendas if tipo == "caption" and "ficaram fora do percentual" in t]
        self.assertTrue(outra or all(n["base_constitucional"] or not n["temas_fora_do_questionario"]
                                     for n in r["normas"]))


class TestTagsMatchEquivalente(unittest.TestCase):
    def test_tags_match_ja_esta_dentro_das_pontuaveis(self):
        # Gemini B2: usar tags_perfil ou tags_perfil & pontuáveis dá o mesmo resultado
        # para normas pontuadas, porque os temas do perfil são TAGS_OBSERVAVEIS.
        pontuaveis = _tags_pontuaveis(NORMAS)
        por_id = {n["id"]: n for n in NORMAS}
        r = gerar_radar({"usa_ia": "Sim", "trata_dados": "Sim — ambos", "online": "Sim — plataforma / app",
                         "setor": "Outro"}, NORMAS, ARESTAS)
        for n in r["normas"]:
            comuns = set(n["tags_match"])
            self.assertLessEqual(comuns, TAGS_OBSERVAVEIS)
            self.assertEqual(comuns, comuns & pontuaveis & _tags_norma(n["id"], por_id[n["id"]]), n["id"])


class TestAgregacaoDeTermos(unittest.TestCase):
    def test_primeiro_termo_nao_casa_segundo_casa(self):
        # Caminho False -> True da agregação (GLM L2 2.10); o True -> False já tinha teste.
        primeiro, segundo = radar.TEMAS_RADAR["plataformas"][:2]
        ementa = f"Regula {segundo}"
        self.assertFalse(radar._casa_termo(primeiro, ementa))
        self.assertTrue(radar._casa_termo(segundo, ementa))

        def busca(termo, n):
            return [{"fonte": "Câmara dos Deputados", "id": "1", "sigla": "PL 1/2026", "ementa": ementa,
                     "termo_busca": termo, "termo_na_ementa": radar._casa_termo(termo, ementa)}]
        with mock.patch.object(radar, "buscar_senado", return_value=[]), \
             mock.patch.object(radar, "buscar_lexml", return_value=[]), \
             mock.patch.object(radar, "buscar_camara", side_effect=busca):
            r = radar.coletar_radar(temas=["plataformas"])
        itens = r["temas"]["plataformas"]["camara"]
        self.assertEqual(len(itens), 1)
        self.assertEqual(radar.termos_do_item(itens[0]), [primeiro, segundo])
        self.assertTrue(itens[0]["termo_na_ementa"])


class TestVerificacaoGoogle(unittest.TestCase):
    def test_arquivo_do_search_console_continua_publicado(self):
        # Verifica a propriedade https://hubstry.dev/lex-io-graph/ no Google Search Console.
        # Não apagar: a verificação cai sem ele.
        arq = RAIZ / "googlec3e890cd899f5c06.html"
        self.assertTrue(arq.is_file())
        self.assertEqual(arq.read_text(encoding="utf-8").strip(),
                         "google-site-verification: googlec3e890cd899f5c06.html")


if __name__ == "__main__":
    unittest.main()
