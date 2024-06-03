from core.requests.request import Request
from core.responses.response import Response

class AIInterface:
    def __init__(self):
        pass

    def invoke(self, req: Request) -> Response:
        pass

    def reset_history(self):
        pass
