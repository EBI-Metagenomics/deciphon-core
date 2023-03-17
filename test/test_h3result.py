import os
import sys
from pathlib import Path

from blx import BLXApp
from blx.cid import CID

from deciphon_core.h3result import H3Result

cid = CID(sha256hex="8f362179042318deb77fe043e79eef9ce6ef54b852b447b4eee4b5d0ff6bb30d")
h3rfile = Path("PF00742.20.h3r")


def test_h3result(tmp_path: Path):
    os.chdir(tmp_path)
    blx = BLXApp()
    blx.get(cid, h3rfile)
    h3r = H3Result(h3rfile)
    h3r.print_targets(sys.stdout)
    h3r.print_domains(sys.stdout)
    h3r.print_targets_table(sys.stdout)
    h3r.print_domains_table(sys.stdout)
