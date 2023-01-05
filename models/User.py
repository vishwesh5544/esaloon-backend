from dataclasses import dataclass, asdict


@dataclass
class User:
    userid: str
    fullname: str
    email: str
    password: str
    phone_numer: int
    creation_date: str

    def __init__(self, userid: str, fullname: str, email: str, password: str, creation_time: str, phone_number: int):
        super().__init__()
        self.userid = userid
        self.fullname = fullname
        self.email = email
        self.password = password
        self.creation_date = creation_time
        self.phone_numer = phone_number
        # self.creation_date = creation_date

    def as_dict(self):
        return asdict(self)
