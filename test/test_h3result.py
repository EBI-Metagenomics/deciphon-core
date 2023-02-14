import os
import sys
from dataclasses import dataclass
from pathlib import Path

import pytest
from blx.cid import CID
from blx.download import download

from deciphon_core.h3result import H3Result


@dataclass
class File:
    cid: CID
    name: str


@pytest.fixture
def h3r_file():
    cid = CID("2427439024da42a5cead8d31bdab294b80b1119f00c4743581ed87b62211760c")
    name = "PF00742.20.h3r"
    return File(cid, name)


def test_h3result(tmp_path: Path, h3r_file: File):
    os.chdir(tmp_path)
    download(h3r_file.cid, h3r_file.name, False)
    h3r = H3Result(h3r_file.name)
    h3r.print_targets(sys.stdout)
    h3r.print_domains(sys.stdout)
    h3r.print_targets_table(sys.stdout)
    h3r.print_domains_table(sys.stdout)
