"""Alertas com prazo da home (lib/alertas.py)."""
import unittest
from datetime import date, timedelta

from lib.alertas import ALERTAS_PRAZO, situacao_prazo


class TestAlertas(unittest.TestCase):
    def test_vencimento_bate_com_publicacao_e_prazo(self):
        for al in ALERTAS_PRAZO:
            with self.subTest(alerta=al["id"]):
                self.assertEqual(al["publicacao"] + timedelta(days=al["prazo_dias"]), al["vencimento_nominal"])
                self.assertTrue(al["ressalva_prazo"])
                self.assertTrue(al["fontes"])
                for _, url in al["fontes"]:
                    self.assertTrue(url.startswith("https://www.gov.br/"), "fonte oficial")

    def test_nao_afirma_obrigacao_generalizada(self):
        for al in ALERTAS_PRAZO:
            texto = " ".join(str(v) for v in al.values())
            self.assertIn("verificar o enquadramento", texto)
            self.assertNotIn("todas as empresas devem", texto.lower())

    def test_situacao_muda_com_a_data(self):
        al = ALERTAS_PRAZO[0]
        v = al["vencimento_nominal"]
        self.assertIn("Faltam 56 dias", situacao_prazo(al, date(2026, 10, 24)))
        self.assertIn("Falta 1 dia", situacao_prazo(al, v - timedelta(days=1)))
        self.assertIn("Hoje é a data nominal", situacao_prazo(al, v))
        self.assertIn("chegou ao fim", situacao_prazo(al, v + timedelta(days=1)))
        self.assertNotIn("último dia", " ".join(situacao_prazo(al, v + timedelta(days=d)) for d in (-1, 0, 1)))

    def test_home_exibe_o_alerta(self):
        from pathlib import Path
        from streamlit.testing.v1 import AppTest
        app = Path(__file__).resolve().parent.parent / "app.py"
        at = AppTest.from_file(str(app), default_timeout=60).run()
        self.assertEqual(len(at.exception), 0)
        self.assertTrue(any("Sistema NIDUS" in w.value for w in at.warning))


if __name__ == "__main__":
    unittest.main()
