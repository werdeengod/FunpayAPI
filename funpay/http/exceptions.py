class HttpRequestError(Exception):
    def __init__(self, status: int, url: str, text: str):
        self.status = status
        self.url = url
        self.text = text

    def __str__(self):
        return f"[ERROR {self.status}] - {self.url}"

