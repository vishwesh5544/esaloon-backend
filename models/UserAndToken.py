from dataclasses import dataclass, asdict
from typing import List
from models.Token import Token
from models.User import User


@dataclass
class UserAndToken:
    user: User
    tokens_list: List[Token]

    def __init__(self, user: User, tokens_list: List[Token]):
        super().__init__()
        self.user = user
        self.tokens_list = tokens_list

    def as_dict(self):
        return asdict(self)
