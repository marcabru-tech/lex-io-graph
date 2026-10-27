"""Invariantes do workflow do Radar (ADR 006 e emenda de 27/10/2026)."""
import unittest
from pathlib import Path

WF = (Path(__file__).resolve().parent.parent / ".github" / "workflows" / "update-radar.yml").read_text(encoding="utf-8")
PASSOS = WF.split("# GOVERNANÇA")[0]


class TestWorkflowRadar(unittest.TestCase):
    def test_nao_faz_push_direto_em_main(self):
        self.assertNotIn("git push origin main", PASSOS)
        self.assertNotIn("git pull --rebase origin main", PASSOS)

    def test_snapshot_entra_por_pr_mesclada_no_job(self):
        self.assertIn('git push origin "$RAMO"', PASSOS)
        self.assertIn("gh pr create --base main", PASSOS)
        self.assertIn('gh pr merge "$RAMO" --squash --delete-branch', PASSOS)
        self.assertIn("pull-requests: write", PASSOS)

    def test_travas_continuam_antes_do_commit(self):
        i_validar = PASSOS.index("name: Validar snapshot")
        i_escopo = PASSOS.index("name: Trava de escopo")
        i_commit = PASSOS.index("name: Commitar snapshot")
        self.assertLess(i_validar, i_commit)
        self.assertLess(i_escopo, i_commit)
        self.assertIn('PERMITIDO="data/radar_legislativo.json"', PASSOS)
        self.assertIn("git add data/radar_legislativo.json", PASSOS)


if __name__ == "__main__":
    unittest.main()
