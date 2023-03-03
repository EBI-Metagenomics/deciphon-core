from collections.abc import Iterator
from dataclasses import dataclass
from typing import Optional
from deciphon_core.cffi import ffi, lib
from abc import ABCMeta, abstractmethod

__all__ = ["Seq", "SeqIter"]


@dataclass
class Seq:
    id: int
    name: bytes
    data: bytes


class SeqIter(Iterator, metaclass=ABCMeta):
    def __init__(self) -> None:
        self._cself = ffi.new_handle(self)
        if self._cself == ffi.NULL:
            raise MemoryError()
        self.save_seq: Optional[Seq] = None

    @property
    def cnext_seq_callb(self):
        return lib.next_seq_callb

    @property
    def cself(self):
        return self._cself

    @abstractmethod
    def __next__(self) -> Seq:
        ...


@ffi.def_extern()
def next_seq_callb(cseq, cself):
    seqit: SeqIter = ffi.from_handle(cself)
    try:
        seq = next(seqit)
        print(seq)
        seqit.save_seq = seq
        lib.dcp_seq_setup(cseq, seq.id, seq.name, seq.data)
    except Exception:
        return False
    return True
