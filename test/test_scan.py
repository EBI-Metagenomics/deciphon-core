from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import pytest
from blx.cid import CID
from blx.download import download
from h3daemon.hmmfile import HMMFile
from h3daemon.sched import SchedContext

from deciphon_core.press import Press
from deciphon_core.scan import Scan


def test_scan(tmp_path: Path, minifam: File, seq_iter):
    os.chdir(tmp_path)
    download(minifam.cid, minifam.name, False)
    dcp = Path("minifam.dcp")
    with Press(minifam.name, dcp) as press:
        for _ in press:
            pass
    hmmfile = HMMFile(Path(minifam.name))
    hmmfile.ensure_pressed()
    with SchedContext(hmmfile) as sched:
        sched.is_ready(True)
        port = sched.master.get_port()
        with Scan(minifam.name, seq_iter, "prods", port) as scan:
            scan.run()


@dataclass
class File:
    cid: CID
    name: str


@pytest.fixture
def minifam():
    cid = CID("fe305d9c09e123f987f49b9056e34c374e085d8831f815cc73d8ea4cdec84960")
    name = "minifam.hmm"
    return File(cid, name)
