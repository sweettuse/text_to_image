from __future__ import annotations
from itertools import islice
from typing import Iterable

def flatten(iterable):
    def _helper(it_or_value):
        if isinstance(it_or_value, (str, bytes)):
            yield it_or_value
            return

        try:
            it = iter(it_or_value)
        except TypeError:
            yield it_or_value
            return

        for v in it:
            yield from _helper(v)
    return _helper(iterable)

def chunks(iterable: Iterable, size: int, chunk_type=list):
    yield from iter(lambda it=iter(iterable): chunk_type(islice(it, size)), chunk_type())