from __future__ import annotations

import os
from pathlib import Path

from blx import BLXApp
from blx.cid import CID
from h3daemon.hmmfile import HMMFile as H3File
from h3daemon.sched import SchedContext

from deciphon_core.hmmfile import HMMFile
from deciphon_core.press import Press
from deciphon_core.scan import Scan
from deciphon_core.snapfile import NewSnapFile

cid = CID(sha256hex="fe305d9c09e123f987f49b9056e34c374e085d8831f815cc73d8ea4cdec84960")
hmm = Path("minifam.hmm")


def test_scan(tmp_path: Path, seq_iter):
    os.chdir(tmp_path)
    blx = BLXApp()
    blx.get(cid, hmm)

    with Press(HMMFile(path=hmm)) as press:
        for x in press:
            x.press()

    hmmfile = H3File(hmm)
    hmmfile.ensure_pressed()

    with SchedContext(hmmfile) as sched:
        sched.is_ready(True)
        scan = Scan(HMMFile(path=hmm), seq_iter, NewSnapFile(path=Path("snap.dcs")))
        scan.port = sched.get_cport()
        with scan:
            scan.run()
