from __future__ import annotations

import shutil
from os import PathLike
from pathlib import Path
from typing import Union

from deciphon_core.cffi import ffi, lib
from deciphon_core.error import DeciphonError

__all__ = ["Scan"]


class Scan:
    def __init__(
        self, hmm: Union[str, PathLike[str]], seq: Union[str, PathLike[str]], port: int
    ):
        self._cscan = lib.dcp_scan_new(port)
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

        self._base_name = f"{self._seq.stem}"

    @property
    def base_name(self):
        return self._base_name

    @base_name.setter
    def base_name(self, x: str):
        self._base_name = x

    @property
    def product_name(self):
        return self.base_name + ".dcs"

    def run(self):
        base_name = self.base_name

        rc = lib.dcp_scan_run(self._cscan, base_name.encode())
        if rc:
            raise DeciphonError(rc)

        archive = shutil.make_archive(base_name, "zip", base_dir=base_name)
        shutil.move(archive, self.product_name)
        shutil.rmtree(base_name)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    def close(self):
        lib.dcp_scan_del(self._cscan)
