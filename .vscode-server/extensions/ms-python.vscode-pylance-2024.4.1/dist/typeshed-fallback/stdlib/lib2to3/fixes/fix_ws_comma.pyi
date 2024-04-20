from typing import ClassVar, Literal

from .. import fixer_base
from ..pytree import Leaf

class FixWsComma(fixer_base.BaseFix):
    BM_compatible: ClassVar[Literal[False]]
    PATTERN: ClassVar[str]
    COMMA: Leaf
    COLON: Leaf
    SEPS: tuple[Leaf, Leaf]
    def transform(self, node, results): ...
