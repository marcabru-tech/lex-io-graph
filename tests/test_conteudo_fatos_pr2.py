"""Travas da PR de conteúdo 2 (24/10/2026): fatos corrigidos com fonte oficial
ou conferência da Luna. Nada aqui altera estado de verificação (ADR 007) nem
campos regidos pelo ADR 008 (orgao, ano, sigla).
"""
import json
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def _nos():
    return {n["id"]: n for n in json.loads((RAIZ / "data" / "normas.json").read_text(encoding="utf-8"))["nodes"]}


class TestFatosPR2(unittest.TestCase):
    def setUp(self):
        self.n = _nos()
        self.corpus = (RAIZ / "data" / "normas.json").read_text(encoding="utf-8")

    def test_vetos(self):
        self.assertIn("§ 7º do art. 35, o art. 36 e o art. 41 foram vetados", self.n["eca_digital"]["historia"])
        self.assertIn("O art. 5º foi vetado", self.n["lei_15409_2026"]["historia"])

    def test_pl_misoginia_autoria(self):
        self.assertIn("Ana Paula Lobato", self.n["pl_misoginia"]["historia"])

    def test_lei_15504_altera_eca_digital(self):
        self.assertIn("art. 36-A", self.n["lei_15504_2026"]["historia"])

    def test_adi_5527_objeto(self):
        h = self.n["stf_adimc"]["historia"]
        self.assertIn("art. 10, § 2º", h)
        self.assertNotIn("obrigação de guarda de registros", h)
        juris = {j["id"]: j for j in json.loads((RAIZ / "data" / "jurisprudencia.json").read_text(encoding="utf-8"))["jurisprudencia"]}
        self.assertEqual(juris["stf_adimc"]["estado_verificacao"], "contestado", "ADR 007: estado não muda")

    def test_viena_vigencia(self):
        self.assertIn("25/10/2009", self.n["convencao_viena_1969"]["historia"])

    def test_autores(self):
        autores = {a["nome"]: a for n in self.n.values() for a in (n.get("autores") or [])}
        self.assertEqual(autores["José Afonso da Silva"]["datas"], "1925–2025")
        self.assertIn("1976", autores["José Afonso da Silva"]["obra"])
        self.assertEqual(autores["Luciano Mendes de Almeida"]["datas"], "1930–2006")

    def test_cf88_artigos(self):
        art = self.n["cf88"]["artigos_chave"]
        self.assertIn("Art. 5º, X", art)
        self.assertIn("Art. 5º, LXXIX", art)

    def test_mecanicos(self):
        for frase in ("concluÃ", "Camara ", "mais abrangente da América Latina", "em conferência)\""):
            self.assertNotIn(frase, self.corpus)

    def test_camada_ensaistica(self):
        textos = "".join((RAIZ / p).read_text(encoding="utf-8") for p in (
            "lib/inteligencia.py", "lib/repositorio.py", "lib/hermeneutica.py", "lib/multisemiose.py"))
        for frase in ("58 volumes", "pelo parte", "séculos XVIII", "Ne bis in idem / Proportionalitas",
                      "arco de 170 anos", "é o primeiro pós-digital", "Resgatado na reforma do CC"):
            self.assertNotIn(frase, textos)
        p7 = next((RAIZ / "pages").glob("7_*Hermeneutica.py")).read_text(encoding="utf-8")
        self.assertNotIn("Influência da Declaração Universal", p7)


if __name__ == "__main__":
    unittest.main()
