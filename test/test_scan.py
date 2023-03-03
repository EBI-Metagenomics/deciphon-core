from __future__ import annotations

import os
from pathlib import Path

from blx.cid import CID
from blx.download import download
from h3daemon.hmmfile import HMMFile
from h3daemon.sched import SchedContext

from deciphon_core.press import Press
from deciphon_core.scan import Scan

cid = CID("fe305d9c09e123f987f49b9056e34c374e085d8831f815cc73d8ea4cdec84960")
hmm = Path("minifam.hmm")


def test_scan(tmp_path: Path, seq_iter):
    os.chdir(tmp_path)
    download(cid, hmm, False)

    db = hmm.parent / f"{hmm.stem}.dcp"
    with Press(hmm, db) as press:
        for x in press:
            x.press()

    hmmfile = HMMFile(hmm)
    hmmfile.ensure_pressed()

    prod = Path("prod")

    with SchedContext(hmmfile) as sched:
        sched.is_ready(True)
        scan = Scan(hmm, db, seq_iter, prod)
        scan.port = sched.master.get_port()
        with scan:
            scan.run()
