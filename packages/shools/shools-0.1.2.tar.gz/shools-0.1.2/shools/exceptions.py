class SedException(Exception):
    def __init__(self, error: bytes) -> None:
        self.message = str(error, encoding="utf-8").replace("sed: -e ", "")
        super().__init__(self.message)
