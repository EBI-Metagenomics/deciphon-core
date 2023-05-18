import os
from pathlib import Path

from blx import BLXApp
from blx.cid import CID

from deciphon_core.hmmfile import HMMFile
from deciphon_core.press import Press

cid = CID(sha256hex="fe305d9c09e123f987f49b9056e34c374e085d8831f815cc73d8ea4cdec84960")
hmm = Path("minifam.hmm")


def test_press(tmp_path: Path):
    os.chdir(tmp_path)
    blx = BLXApp()
    blx.get(cid, hmm)

    hmmfile = HMMFile(path=hmm)
    with Press(hmmfile) as press:
        for x in press:
            x.press()

    assert hmmfile.dbfile.path.stat().st_size == 9933912
