from __future__ import annotations

import shutil
from pathlib import Path

from deciphon_core.cffi import ffi, lib
from deciphon_core.error import DeciphonError
from deciphon_core.filepath import FilePath
from deciphon_core.seq import SeqIter
from deciphon_core.cseq import CSeqIter

__all__ = ["Scan"]


class Scan:
    def __init__(
        self, hmm: FilePath, db: FilePath, seqit: SeqIter, prodname: str, port: int
    ):
        self._cscan = lib.dcp_scan_new(port)
        if self._cscan == ffi.NULL:
            raise MemoryError()

        self._hmm = Path(hmm)
        self._db = Path(db)

        if rc := lib.dcp_scan_set_nthreads(self._cscan, 1):
            raise DeciphonError(rc)

        lib.dcp_scan_set_lrt_threshold(self._cscan, 10.0)
        lib.dcp_scan_set_multi_hits(self._cscan, True)
        lib.dcp_scan_set_hmmer3_compat(self._cscan, False)

        if rc := lib.dcp_scan_set_db_file(self._cscan, bytes(self._db)):
            raise DeciphonError(rc)

        x = self._seqit = CSeqIter(seqit)
        lib.dcp_scan_set_seq_iter(self._cscan, x.c_callback, x.c_self)

        self._prodname = prodname

    @property
    def product_filename(self):
        return f"{self._prodname}.dcs"

    def run(self):
        prodname = self._prodname
        if rc := lib.dcp_scan_run(self._cscan, prodname.encode()):
            raise DeciphonError(rc)

        archive = shutil.make_archive(prodname, "zip", base_dir=prodname)
        shutil.move(archive, self.product_filename)
        shutil.rmtree(prodname)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    def close(self):
        lib.dcp_scan_del(self._cscan)
