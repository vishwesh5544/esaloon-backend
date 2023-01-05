from dataclasses import dataclass, asdict


@dataclass
class Appointment:
    time_from: str
    email: str
    service: str
    date: str

    def __init__(self, email: str, time_from: str, service: str, date: str):
        self.email = email
        self.time_from = time_from
        self.service = service
        self.date = date

    def as_dict(self):
        return asdict(self)
