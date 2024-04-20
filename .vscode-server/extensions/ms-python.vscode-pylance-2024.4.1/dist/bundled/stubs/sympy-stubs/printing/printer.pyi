import inspect
from typing import Any, Callable, Generator, Type
from contextlib import contextmanager

@contextmanager
def printer_context(printer, **kwargs) -> Generator[None, Any, None]:
    ...

class Printer:
    _global_settings: dict[str, Any] = ...
    _default_settings: dict[str, Any] = ...
    printmethod: str = ...
    def __init__(self, settings=...) -> None:
        ...
    
    @classmethod
    def set_global_settings(cls, **settings) -> None:
        ...
    
    @property
    def order(self) -> Any:
        ...
    
    def doprint(self, expr) -> str:
        ...
    
    def emptyPrinter(self, expr) -> str:
        ...
    


class _PrintFunction:
    def __init__(self, f, print_cls: Type[Printer]) -> None:
        ...
    
    def __reduce__(self):
        ...
    
    def __call__(self, *args, **kwargs):
        ...
    
    @property
    def __signature__(self) -> inspect.Signature:
        ...
    


def print_function(print_cls) -> Callable[..., _PrintFunction]:
    ...

