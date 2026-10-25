"""A2: marcar (não descartar) resultados da Câmara e consolidar a mesma proposição entre as Casas."""
import copy
import json
import unittest
from pathlib import Path
from unittest import mock

import lib.radar as radar
import updater
from lib.radar import consolidar_tema, resumo_consolidacao, termo_na_ementa, termos_do_item
from lib.radar_cartao import html_cartao

RAIZ = Path(__file__).resolve().parent.parent
# Casos medidos da A2: recorte congelado da coleta de 23/10/2026 (anterior à A2).
# Não lê data/radar_legislativo.json, que muda a cada coleta semanal.
SNAPSHOT = json.loads((RAIZ / "tests" / "fixtures" / "radar_snapshot_pre_a2.json").read_text(encoding="utf-8"))


def _cartao(tema: str, sigla: str):
    c = consolidar_tema(SNAPSHOT["temas"][tema], tema)
    for grupo in ("principal", "conferir"):
        for x in c[grupo]:
            if x["sigla"] == sigla:
                return grupo, x
    return None, None


class TestCasosMedidos(unittest.TestCase):
    def test_ruido_sinalizado_e_sem_novidade(self):
        for tema, sigla in (("ia", "PL 5580/2026"), ("dados", "PL 5594/2026"), ("ia", "PL 5338/2026")):
            grupo, _ = _cartao(tema, sigla)
            self.assertEqual(grupo, "conferir", sigla)
        siglas_novas = {n["sigla"] for n in updater.detectar_novidades(SNAPSHOT, {})}
        for sigla in ("PL 5580/2026", "PL 5594/2026", "PL 5338/2026"):
            self.assertNotIn(sigla, siglas_novas)

    def test_relevantes_nao_sao_descartados(self):
        for tema, sigla in (("infraestrutura_digital", "PLP 74/2026"), ("minerais_criticos", "PL 2988/2026"),
                            ("minerais_criticos", "PL 1984/2026"), ("ia", "PL 5349/2026"),
                            ("dados", "PL 5498/2026")):
            grupo, _ = _cartao(tema, sigla)
            self.assertIsNotNone(grupo, sigla)  # continua acessível (principal ou conferir)

    def test_proposicao_nas_duas_casas_vira_um_cartao_com_as_duas_fontes(self):
        # PL 278/2026: mesma ementa no Senado e na Câmara -> um cartão, duas fontes.
        c = consolidar_tema(SNAPSHOT["temas"]["infraestrutura_digital"], "infraestrutura_digital")
        cartoes = [x for x in c["principal"] + c["conferir"] if x["sigla"] == "PL 278/2026"]
        self.assertEqual(len(cartoes), 1)
        fontes = {f["fonte"] for f in cartoes[0]["fontes"]}
        self.assertEqual(fontes, {"Senado Federal", "Câmara dos Deputados"})
        self.assertTrue(all(f["url"] and f["id"] for f in cartoes[0]["fontes"]))
        html = html_cartao(cartoes[0])
        self.assertIn("↗ Senado Federal", html)
        self.assertIn("↗ Câmara dos Deputados", html)

    def test_mesma_designacao_com_ementas_diferentes_nao_funde(self):
        # PLP 74/2026: o do Senado altera a LC 229; o da Câmara trata de
        # benefícios tributários. São proposições distintas (A6-e).
        c = consolidar_tema(SNAPSHOT["temas"]["infraestrutura_digital"], "infraestrutura_digital")
        cartoes = [x for x in c["principal"] + c["conferir"] if x["sigla"] == "PLP 74/2026"]
        self.assertEqual(len(cartoes), 2)
        self.assertEqual(sorted(x["chave"] for x in cartoes), ["PLP 74/2026", "PLP 74/2026@camara"])
        self.assertEqual(sorted(f["casa"] for x in cartoes for f in x["fontes"]), ["camara", "senado"])
        self.assertNotEqual(cartoes[0]["ementa"], cartoes[1]["ementa"])

    def test_tema_curado_nao_passa_pela_marca(self):
        tema = "Sustação dos Decretos 12.975 e 12.976/2026"
        c = consolidar_tema(SNAPSHOT["temas"][tema], tema)
        self.assertEqual(c["conferir"], [])
        self.assertEqual(len(c["principal"]), len(SNAPSHOT["temas"][tema]["camara"]))

    def test_mesma_proposicao_em_dois_temas_continua_nos_dois(self):
        for tema in ("plataformas", "trabalho_digital"):
            grupo, _ = _cartao(tema, "PL 5253/2026")
            self.assertIsNotNone(grupo, tema)

    def test_snapshot_antigo_sem_o_campo_e_classificado_localmente(self):
        temas = SNAPSHOT["temas"]
        for tema_data in temas.values():
            for fonte in ("senado", "camara", "lexml"):
                for item in tema_data.get(fonte, []):
                    self.assertNotIn("termo_na_ementa", item)  # recorte congelado, anterior à A2
        total_antes = sum(len(t.get(f, [])) for t in temas.values() for f in ("senado", "camara", "lexml"))
        r = resumo_consolidacao(SNAPSHOT)
        self.assertEqual(r["itens_coletados"], total_antes)  # nada apagado
        self.assertGreater(r["cartoes_principais"], 0)
        self.assertGreater(r["cartoes_a_conferir"], 0)


class TestRegras(unittest.TestCase):
    def test_campo_gravado_prevalece_e_ausencia_recalcula(self):
        self.assertFalse(termo_na_ementa({"termo_na_ementa": False, "termo_busca": "x", "ementa": "x"}))
        self.assertTrue(termo_na_ementa({"termo_busca": "dados pessoais",
                                         "ementa": "Trata de dados pessoais de usuários"}))
        self.assertFalse(termo_na_ementa({"termo_busca": "dados pessoais", "ementa": "Trata de impostos"}))
        self.assertTrue(termo_na_ementa({"ementa": "sem termo registrado"}))

    def test_dois_termos_agregados_e_elegivel_se_algum_casar(self):
        def busca_falsa(termo, n):
            return [{"fonte": "Câmara dos Deputados", "id": "1", "sigla": "PL 1/2026",
                     "ementa": "Regula plataformas digitais", "termo_busca": termo,
                     "termo_na_ementa": radar._casa_termo(termo, "Regula plataformas digitais")}]
        with mock.patch.object(radar, "buscar_senado", return_value=[]), \
             mock.patch.object(radar, "buscar_lexml", return_value=[]), \
             mock.patch.object(radar, "buscar_camara", side_effect=busca_falsa):
            r = radar.coletar_radar(temas=["plataformas"])
        itens = r["temas"]["plataformas"]["camara"]
        self.assertEqual(len(itens), 1)
        self.assertEqual(termos_do_item(itens[0]), radar.TEMAS_RADAR["plataformas"][:2])
        self.assertTrue(itens[0]["termo_na_ementa"])  # "plataformas digitais" casa

    def test_limite_de_dois_termos_preservado(self):
        chamadas = []
        with mock.patch.object(radar, "buscar_senado", return_value=[]), \
             mock.patch.object(radar, "buscar_lexml", return_value=[]), \
             mock.patch.object(radar, "buscar_camara", side_effect=lambda t, n: chamadas.append(t) or []):
            radar.coletar_radar(temas=["ia"])
        self.assertEqual(chamadas, radar.TEMAS_RADAR["ia"][:2])

    NOVO = {"temas": {"t": {
        "senado": [{"id": "s1", "sigla": "PL 278/2026", "ementa": "datacenter", "termo_busca": "datacenter"}],
        "camara": [{"id": "c9", "sigla": "PL 278/2026", "ementa": "datacenter", "termo_busca": "datacenter",
                    "termo_na_ementa": True}],
    }}}

    def test_mesma_proposicao_mesmo_tema_duas_casas_um_alerta(self):
        nov = updater.detectar_novidades(self.NOVO, {})
        self.assertEqual(len(nov), 1)
        self.assertEqual((nov[0]["tema"], nov[0]["chave"]), ("t", "PL 278/2026"))
        # já vista no MESMO tema por outra Casa, com outro id: não é novidade
        anterior = {"temas": {"t": {"camara": [{"id": "outro", "sigla": "PL 278/2026"}]}}}
        self.assertEqual(updater.detectar_novidades(self.NOVO, anterior), [])

    def test_mesma_proposicao_em_tema_novo_continua_elegivel(self):
        anterior = {"temas": {"x": {"camara": [{"id": "outro", "sigla": "PL 278/2026"}]}}}
        nov = updater.detectar_novidades(self.NOVO, anterior)
        self.assertEqual([(n["tema"], n["chave"]) for n in nov], [("t", "PL 278/2026")])

    def test_so_a_camara_vai_para_conferir(self):
        tema = {
            "senado": [{"id": "s", "sigla": "PL 1/2026", "ementa": "outro assunto", "termo_busca": "dados pessoais"}],
            "lexml": [{"id": "l", "sigla": "PL 2/2026", "ementa": "outro assunto", "termo_busca": "dados pessoais"}],
            "camara": [{"id": "c", "sigla": "PL 3/2026", "ementa": "outro assunto", "termo_busca": "dados pessoais"}],
        }
        c = consolidar_tema(tema, "dados")
        self.assertEqual({x["sigla"] for x in c["principal"]}, {"PL 1/2026", "PL 2/2026"})
        self.assertEqual([x["sigla"] for x in c["conferir"]], ["PL 3/2026"])
        self.assertTrue(all(f["fonte"] == "Câmara dos Deputados" for x in c["conferir"] for f in x["fontes"]))

    def test_consolidacao_nao_altera_o_snapshot(self):
        tema = copy.deepcopy(SNAPSHOT["temas"]["infraestrutura_digital"])
        consolidar_tema(tema)
        self.assertEqual(tema, SNAPSHOT["temas"]["infraestrutura_digital"])


class TestRetratoVivo(unittest.TestCase):
    """Só invariantes: valem antes e depois de qualquer coleta semanal."""

    def test_consolidacao_preserva_todos_os_itens(self):
        vivo = json.loads((RAIZ / "data" / "radar_legislativo.json").read_text(encoding="utf-8"))
        total = sum(len(t.get(f, [])) for t in vivo.get("temas", {}).values()
                    for f in ("senado", "camara", "lexml"))
        self.assertEqual(resumo_consolidacao(vivo)["itens_coletados"], total)

    def test_retrato_gravado_depois_da_a2_continua_legivel(self):
        # Simula a coleta de segunda-feira: o campo termo_na_ementa passa a vir gravado.
        depois = copy.deepcopy(SNAPSHOT)
        for tema, dados in depois["temas"].items():
            for item in dados.get("camara", []):
                item["termo_na_ementa"] = termo_na_ementa(item)
        for tema in SNAPSHOT["temas"]:
            antes = consolidar_tema(SNAPSHOT["temas"][tema], tema)
            gravado = consolidar_tema(depois["temas"][tema], tema)
            for grupo in ("principal", "conferir"):
                self.assertEqual([c["chave"] for c in antes[grupo]],
                                 [c["chave"] for c in gravado[grupo]], (tema, grupo))


if __name__ == "__main__":
    unittest.main()
