from pathlib import Path

from deciphon_core.filepath import FilePath

__all__ = ["SnapFile"]


class SnapFile:
    def __init__(self, filename: FilePath):
        filename = Path(filename)
        if filename.name == filename.stem:
            raise ValueError("Snap file must have an extension.")
        self._file = filename

    @property
    def path(self):
        return self._file

    @property
    def basedir(self):
        return self._file.parent / f"{self._file.stem}"
