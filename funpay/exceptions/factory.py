class APIErrorFactory(Exception):
    def __init__(self, code: int = None, name: str = None):
        super().__init__(code)

        self.code = int(code) if code else None
        self.name = name

    def __str__(self):
        return f"[{self.code}] {self.name}\n"
