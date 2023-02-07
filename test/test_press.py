import os
from dataclasses import dataclass
from pathlib import Path

import pytest
from blx.cid import CID
from blx.download import download

from deciphon_core.press import Press


@dataclass
class File:
    cid: CID
    name: str


@pytest.fixture
def minifam():
    cid = CID("fe305d9c09e123f987f49b9056e34c374e085d8831f815cc73d8ea4cdec84960")
    name = "minifam.hmm"
    return File(cid, name)


def test_press(tmp_path: Path, minifam: File):
    os.chdir(tmp_path)
    download(minifam.cid, minifam.name, False)
    dcp = Path("minifam.dcp")
    with Press(minifam.name, dcp) as press:
        for _ in press:
            pass
    assert dcp.stat().st_size == 6711984
