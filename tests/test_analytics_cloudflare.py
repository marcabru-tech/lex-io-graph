import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BEACON = "static.cloudflareinsights.com/beacon.min.js"
TOKEN = "feb0887f254e45ac9769d963002114a7"
PUBLICAS = ["index.html", "artigo-04-anpd-judiciario.html",
            "artigos/artigo-01-regulacao-digital.html",
            "artigos/artigo-02-graciliano-prefeito.html",
            "artigos/artigo-03-paradigma-preventivo.html",
            "artigos/artigo-04-anpd-judiciario.html"]


class TestBeaconCloudflare(unittest.TestCase):
    def test_paginas_publicas_tem_um_beacon(self):
        for nome in PUBLICAS:
            texto = (RAIZ / nome).read_text(encoding="utf-8")
            self.assertEqual(texto.count(BEACON), 1, nome)
            self.assertIn(TOKEN, texto, nome)

    def test_app_nao_tem_beacon(self):
        arquivos = [RAIZ / "app.py"] + list((RAIZ / "pages").glob("*.py")) + list((RAIZ / "lib").glob("*.py"))
        for p in arquivos:
            self.assertNotIn("cloudflareinsights", p.read_text(encoding="utf-8"), p.name)

    def test_aviso_distingue_analytics_e_registros_da_hospedagem(self):
        texto = (RAIZ / "index.html").read_text(encoding="utf-8")
        self.assertIn("Essa ferramenta não é utilizada dentro da aplicação", texto)
        self.assertIn("a URL solicitada, que pode conter parâmetros de consulta", texto)


if __name__ == "__main__":
    unittest.main()


class TestRetencaoContador(unittest.TestCase):
    def test_aviso_informa_prazo_do_contador(self):
        texto = (RAIZ / "index.html").read_text(encoding="utf-8")
        self.assertIn("mantidos no Google Cloud Logging por até 12 meses", texto)
        self.assertIn("não inclui endereço IP nem URL da requisição", texto)
        self.assertIn("retenção configurada de 30 dias", texto)
