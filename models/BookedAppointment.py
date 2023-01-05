from dataclasses import dataclass, asdict

from models.Appointment import Appointment


@dataclass
class BookedAppointment:
    id: int
    appointment: Appointment

    def __init__(self, appointment_id: int, appointment: Appointment):
        self.id = appointment_id
        self.appointment = appointment

    def as_dict(self):
        return asdict(self)
