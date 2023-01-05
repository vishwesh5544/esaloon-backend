from dataclasses import dataclass, asdict


@dataclass
class Token:
    tokenid: str
    token: str
    email: str

    def __init__(self, tokenid: str, token: str, email: str):
        super().__init__()
        self.tokenid = tokenid
        self.token = token
        self.email = email

    def as_dict(self):
        return asdict(self)
