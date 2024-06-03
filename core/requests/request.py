class Request():
    username: str
    text: str

    def __init__(self, username, text) -> None:
        self.username = username
        self.text = text