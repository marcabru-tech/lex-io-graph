"""A6-b: proposição que passa de "conferir" a "principal" gera novidade."""
import json
import unittest
from pathlib import Path

import updater

RAIZ = Path(__file__).resolve().parent.parent
FIXTURE = json.loads((RAIZ / "tests" / "fixtures" / "radar_snapshot_pre_a2.json").read_text(encoding="utf-8"))


def _camara(sigla: str, ementa: str, termo: str = "dados pessoais", **extra) -> dict:
    return {"id": sigla, "sigla": sigla, "ementa": ementa, "termo_busca": termo,
            "url": "https://www.camara.leg.br/", **extra}


def _radar(tema: str, camara=(), senado=()) -> dict:
    return {"temas": {tema: {"senado": list(senado), "camara": list(camara), "lexml": []}}}


class TestPromocao(unittest.TestCase):
    def test_conferir_para_principal_gera_novidade(self):
        # Semana 1: ementa sem o termo -> "conferir", sem alerta.
        semana1 = _radar("dados", camara=[_camara("PL 10/2026", "Altera regras de tributação")])
        self.assertEqual(updater.detectar_novidades(semana1, {}), [])
        # Semana 2: ementa atualizada passa a citar o termo -> "principal".
        semana2 = _radar("dados", camara=[_camara("PL 10/2026", "Protege dados pessoais na tributação")])
        nov = updater.detectar_novidades(semana2, semana1)
        self.assertEqual([(n["tema"], n["chave"]) for n in nov], [("dados", "PL 10/2026")])

    def test_campo_gravado_tambem_conta(self):
        semana1 = _radar("dados", camara=[_camara("PL 11/2026", "x", termo_na_ementa=False)])
        semana2 = _radar("dados", camara=[_camara("PL 11/2026", "x", termo_na_ementa=True)])
        self.assertEqual(len(updater.detectar_novidades(semana2, semana1)), 1)

    def test_principal_nas_duas_semanas_nao_repete(self):
        r = _radar("dados", camara=[_camara("PL 12/2026", "Trata de dados pessoais")])
        self.assertEqual(updater.detectar_novidades(r, r), [])

    def test_conferir_nas_duas_semanas_nao_alerta(self):
        r = _radar("dados", camara=[_camara("PL 13/2026", "Trata de impostos")])
        self.assertEqual(updater.detectar_novidades(r, r), [])

    def test_ja_principal_pelo_senado_nao_alerta_quando_camara_entra(self):
        senado = {"id": "s1", "sigla": "PL 14/2026", "ementa": "Trata de impostos", "termo_busca": "dados pessoais"}
        semana1 = _radar("dados", senado=[senado])
        semana2 = _radar("dados", senado=[senado],
                         camara=[_camara("PL 14/2026", "Trata de impostos")])
        self.assertEqual(updater.detectar_novidades(semana2, semana1), [])

    def test_retrato_anterior_sem_o_campo_e_reclassificado(self):
        # Retrato pré-A2 como anterior: nada do próprio retrato vira novidade.
        self.assertEqual(updater.detectar_novidades(FIXTURE, FIXTURE), [])


if __name__ == "__main__":
    unittest.main()
