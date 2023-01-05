from dataclasses import dataclass, asdict


@dataclass
class UserAndTokenSingle:
    email: str
    token: str

    def __init__(self, email: str, token: str):
        super().__init__()
        self.email = email
        self.token = token

    def as_dict(self):
        return asdict(self)
