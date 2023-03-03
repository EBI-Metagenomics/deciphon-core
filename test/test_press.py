import os
from pathlib import Path

from blx.cid import CID
from blx.download import download

from deciphon_core.press import Press

cid = CID("fe305d9c09e123f987f49b9056e34c374e085d8831f815cc73d8ea4cdec84960")
hmm = Path("minifam.hmm")


def test_press(tmp_path: Path):
    os.chdir(tmp_path)
    download(cid, hmm, False)

    db = hmm.parent / f"{hmm.stem}.dcp"
    with Press(hmm, db) as press:
        for x in press:
            x.press()

    assert db.stat().st_size == 6711984
