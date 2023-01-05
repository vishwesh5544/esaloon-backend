from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class ApiResponseModel:
    status_code: int
    message: Optional[str]
    response_type: Optional[str]
    response: Optional[dict]

    def __init__(self, code: int, message: Optional[str] = None, response_type: Optional[str] = None, response: Optional[dict] = None):
        super().__init__()
        self.status_code = code
        self.message = message
        self.response_type = response_type
        self.response = response

    def as_dict(self):
        return asdict(self)
