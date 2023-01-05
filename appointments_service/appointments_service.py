from database.db import Db
from models.ApiResponseModel import ApiResponseModel
import mysql.connector

from models.Appointment import Appointment
from models.BookedAppointment import BookedAppointment


class AppointmentsService:
    db = mysql.connector
    connection = mysql.connector.connection

    def __init__(self):
        self.db = Db()

    def create_appointment(self, appointment: Appointment):
        cursor = self.db.cursor
        query = "INSERT INTO appointments(time_from, email, service, date) VALUES(%s,%s, %s, %s)"
        values = [appointment.time_from, appointment.email, appointment.service, appointment.date]
        cursor.execute(query, values)
        self.db.connection.commit()
        last_row_id = cursor.lastrowid
        booked_appointment = BookedAppointment(
            appointment_id=last_row_id,
            appointment=appointment
        )
        return booked_appointment

    def get_appointments_by_email(self, email: str):
        cursor = self.db.cursor
        query = "SELECT * FROM appointments WHERE email=%s"
        values = [email]
        cursor.execute(query, values)
        if cursor.rowcount == 0:
            return None
        else:
            return cursor.fetchall()

    def delete_appointment_by_id(self, appointment_id: str, email: str):
        cursor = self.db.cursor
        query = "DELETE FROM appointments WHERE id = %s AND email = %s"
        values = [appointment_id, email]
        cursor.execute(query, values)
        self.db.connection.commit()
        if cursor.rowcount == 0:
            return None
        else:
            return cursor.lastrowid
