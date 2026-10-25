"""O sitemap do site estático lista só páginas que existem e batem com o canonical."""
import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BASE = "https://hubstry.dev/lex-io-graph/"
NS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}


class TestSitemap(unittest.TestCase):
    def setUp(self):
        self.urls = [e.text for e in ET.parse(RAIZ / "sitemap.xml").getroot().findall("s:url/s:loc", NS)]

    def test_urls_unicas_e_na_base(self):
        self.assertTrue(self.urls)
        self.assertEqual(len(self.urls), len(set(self.urls)))
        self.assertTrue(all(u.startswith(BASE) for u in self.urls))

    def test_cada_url_existe_e_tem_canonical_igual(self):
        for url in self.urls:
            rel = url[len(BASE):] or "index.html"
            arquivo = RAIZ / rel
            with self.subTest(url=url):
                self.assertTrue(arquivo.is_file(), rel)
                html = arquivo.read_text(encoding="utf-8")
                m = re.search(r'<link rel="canonical" href="([^"]+)"', html)
                self.assertIsNotNone(m, rel)
                self.assertEqual(m.group(1), url)

    def test_artigos_publicados_estao_no_sitemap(self):
        for artigo in sorted((RAIZ / "artigos").glob("*.html")):
            self.assertIn(BASE + "artigos/" + artigo.name, self.urls)


if __name__ == "__main__":
    unittest.main()
