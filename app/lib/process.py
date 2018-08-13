from typing import Callable, Optional

class Process:
    def __init__(self, f: Callable):
        self._f = f

    def run(self) -> None:
        pass

    def join(self) -> Optional[str]:
        pass
