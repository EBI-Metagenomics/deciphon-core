from __future__ import annotations

from os import PathLike
from pathlib import Path

from deciphon_core.cffi import ffi, lib
from deciphon_core.error import DeciphonError

__all__ = ["Scan"]


class Scan:
    def __init__(self, hmm: str | PathLike[str], seq: str | PathLike[str]):
        self._cscan = lib.dcp_scan_new(0)
        if self._cscan == ffi.NULL:
            raise MemoryError()

        self._hmm = Path(hmm)
        self._db = Path(self._hmm.stem + ".dcp")
        self._seq = Path(seq)

        rc = lib.dcp_scan_set_nthreads(self._cscan, 1)
        if rc:
            raise DeciphonError(rc)

        lib.dcp_scan_set_lrt_threshold(self._cscan, 10.0)
        lib.dcp_scan_set_multi_hits(self._cscan, True)
        lib.dcp_scan_set_hmmer3_compat(self._cscan, False)

        rc = lib.dcp_scan_set_db_file(self._cscan, bytes(self._db))
        if rc:
            raise DeciphonError(rc)

        rc = lib.dcp_scan_set_seq_file(self._cscan, bytes(self._seq))
        if rc:
            raise DeciphonError(rc)

    def run(self, prod: str | PathLike[str]):
        rc = lib.dcp_scan_run(self._cscan, bytes(Path(prod)))
        if rc:
            raise DeciphonError(rc)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()
        return True

    def close(self):
        lib.dcp_scan_del(self._cscan)
