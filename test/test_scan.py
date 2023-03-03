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
from deciphon_core.seq import SeqIter, Seq


def test_scan(tmp_path: Path, minifam: File):
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
        scan = Scan(minifam.name, MySeqIter(), "prods", port)
        scan.run()
        scan.close()
    pass


@dataclass
class File:
    cid: CID
    name: str


@pytest.fixture
def minifam():
    cid = CID("fe305d9c09e123f987f49b9056e34c374e085d8831f815cc73d8ea4cdec84960")
    name = "minifam.hmm"
    return File(cid, name)


class MySeqIter(SeqIter):
    seqs = [
        Seq(
            1,
            b"Homoserine_dh-consensus",
            b"CCTATCATTTCGACGCTCAAGGAGTCGCTGACAGGTGACCGTATTACTCGAATCGAAGGGATATTAAACG"
            b"GCACCCTGAATTACATTCTCACTGAGATGGAGGAAGAGGGGGCTTCATTCTCTGAGGCGCTGAAGGAGGC"
            b"ACAGGAATTGGGCTACGCGGAAGCGGATCCTACGGACGATGTGGAAGGGCTAGATGCTGCTAGAAAGCTG"
            b"GCAATTCTAGCCAGATTGGCATTTGGGTTAGAGGTCGAGTTGGAGGACGTAGAGGTGGAAGGAATTGAAA"
            b"AGCTGACTGCCGAAGATATTGAAGAAGCGAAGGAAGAGGGTAAAGTTTTAAAACTAGTGGCAAGCGCCGT"
            b"CGAAGCCAGGGTCAAGCCTGAGCTGGTACCTAAGTCACATCCATTAGCCTCGGTAAAAGGCTCTGACAAC"
            b"GCCGTGGCTGTAGAAACGGAACGGGTAGGCGAACTCGTAGTGCAGGGACCAGGGGCTGGCGCAGAGCCAA"
            b"CCGCATCCGCTGTACTCGCTGACCTTCTC",
        ),
        Seq(
            2,
            b"AA_kinase-consensus",
            b"AAACGTGTAGTTGTAAAGCTTGGGGGTAGTTCTCTGACAGATAAGGAAGAGGCATCACTCAGGCGTTTAG"
            b"CTGAGCAGATTGCAGCATTAAAAGAGAGTGGCAATAAACTAGTGGTCGTGCATGGAGGCGGCAGCTTCAC"
            b"TGATGGTCTGCTGGCATTGAAAAGTGGCCTGAGCTCGGGCGAATTAGCTGCGGGGTTGAGGAGCACGTTA"
            b"GAAGAGGCCGGAGAAGTAGCGACGAGGGACGCCCTAGCTAGCTTAGGGGAACGGCTTGTTGCAGCGCTGC"
            b"TGGCGGCGGGTCTCCCTGCTGTAGGACTCAGCGCCGCTGCGTTAGATGCGACGGAGGCGGGCCGGGATGA"
            b"AGGCAGCGACGGGAACGTCGAGTCCGTGGACGCAGAAGCAATTGAGGAGTTGCTTGAGGCCGGGGTGGTC"
            b"CCCGTCCTAACAGGATTTATCGGCTTAGACGAAGAAGGGGAACTGGGAAGGGGATCTTCTGACACCATCG"
            b"CTGCGTTACTCGCTGAAGCTTTAGGCGCGGACAAACTCATAATACTGACCGACGTAGACGGCGTTTACGA"
            b"TGCCGACCCTAAAAAGGTCCCAGACGCGAGGCTCTTGCCAGAGATAAGTGTGGACGAGGCCGAGGAAAGC"
            b"GCCTCCGAATTAGCGACCGGTGGGATGAAGGTCAAACATCCAGCGGCTCTTGCTGCAGCTAGACGGGGGG"
            b"GTATTCCGGTCGTGATAACGAAT",
        ),
        Seq(
            3,
            b"23ISL-consensus",
            b"CAGGGTCTGGATAACGCTAATCGTTCGCTAGTTCGCGCTACAAAAGCAGAAAGTTCAGATATACGGAAAG"
            b"AGGTGACTAACGGCATCGCTAAAGGGCTGAAGCTAGACAGTCTGGAAACAGCTGCAGAGTCGAAGAACTG"
            b"CTCAAGCGCACAGAAAGGCGGATCGCTAGCTTGGGCAACCAACTCCCAACCACAGCCTCTCCGTGAAAGT"
            b"AAGCTTGAGCCATTGGAAGACTCCCCACGTAAGGCTTTAAAAACACCTGTGTTGCAAAAGACATCCAGTA"
            b"CCATAACTTTACAAGCAGTCAAGGTTCAACCTGAACCCCGCGCTCCCGTCTCCGGGGCGCTGTCCCCGAG"
            b"CGGGGAGGAACGCAAGCGCCCAGCTGCGTCTGCTCCCGCTACCTTACCGACACGACAGAGTGGTCTAGGT"
            b"TCTCAGGAAGTCGTTTCGAAGGTGGCGACTCGCAAAATTCCAATGGAGTCACAACGCGAGTCGACT",
        ),
    ]

    def __init__(self):
        self._idx = -1
        super().__init__()

    def __iter__(self):
        return self

    def __next__(self):
        self._idx += 1
        if self._idx < len(self.seqs):
            return self.seqs[self._idx]
        raise StopIteration()
