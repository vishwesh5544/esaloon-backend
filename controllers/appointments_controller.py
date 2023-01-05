from flask_restful import Resource
from flask import current_app as app, request
from flask_restful import Resource, reqparse
from models.ApiResponseModel import ApiResponseModel
from appointments_service.appointments_service import AppointmentsService
from models.Appointment import Appointment


class AppointmentsController(Resource):

    def __init__(self):
        with app.app_context():
            self.appoinments_service = AppointmentsService()

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("time_from", type=str, required=True, help='Starting time cannot be empty.')
        parser.add_argument("email", type=str, required=True, help='Email cannot be empty.')
        parser.add_argument("service", type=str, required=True, help='Service cannot be empty.')
        parser.add_argument("date", type=str, required=True, help='Date cannot be empty.')
        args = parser.parse_args()
        appointment = Appointment(
            time_from=args["time_from"],
            email=args["email"],
            service=args["service"],
            date=args["date"]
        )
        print(appointment.as_dict())
        return ApiResponseModel(code=201, message="Appointment booked successfully.", response_type="success",
                                response=self.appoinments_service.create_appointment(appointment)).as_dict(), 201

    def get(self):
        args = request.args
        email = args['email']
        appointments = self.appoinments_service.get_appointments_by_email(email)
        if appointments is None or appointments.__sizeof__() < 0:
            return ApiResponseModel(code=404, message="No records found for email.", response_type="Failure").as_dict()
        else:
            return ApiResponseModel(response=self.appoinments_service.get_appointments_by_email(email), code=200, response_type="success",
                                    message="sucess").as_dict(), 200

    def delete(self):
        args = request.args
        appointment_id = args["id"]
        email = args["email"]
        deleted_appointment = self.appoinments_service.delete_appointment_by_id(appointment_id=appointment_id, email=email)
        if deleted_appointment is None:
            return ApiResponseModel(code=404, message="No records found.", response_type="Failure").as_dict(), 404
        else:
            return ApiResponseModel(code=200, message="Appointment deleted successfully.", response_type="success").as_dict(), 200
