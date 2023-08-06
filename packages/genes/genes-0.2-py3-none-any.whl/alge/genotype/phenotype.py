
from collections.abc import Sized
from typing import List


class Phenotype(Sized):

    _data: List[bool]

    def __init__(self, phenotype: List[bool]):
        self._data = phenotype

    def __len__(self) -> int:
        return len(self._data)

    def __getitem__(self, item) -> bool:
        return self._data[item]

    def data(self) -> List[bool]:
        return self._data
