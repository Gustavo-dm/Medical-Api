from flask import request
from flask_restx import Namespace, Resource, fields
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from models import Doctor, Patient
from db import engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

doctor_ns = Namespace("doctors", description="Doctor related operations")

doctor_model = doctor_ns.model(
    "Doctor",
    {
        "id": fields.Integer(description="Doctor id"),
        "name": fields.String(required=True, description="Doctor name"),
        "crm": fields.String(required=True, description="Doctor CRM number"),
        "crmUf": fields.String(required=True, description="Doctor CRM state"),
    },
)

patient_model = doctor_ns.model(
    "Patient",
    {
        "id": fields.Integer(description="Patient Id"),
        "name": fields.String(description="Patient name"),
        "birthDate": fields.String(description="Patient birth date"),
        "cpf": fields.String(description="Patient CPF"),
    },
)


@doctor_ns.route("/")
class DoctorListResource(Resource):
    @doctor_ns.marshal_with(doctor_model, as_list=True)
    def get(self):
        session = SessionLocal()
        doctors = session.query(Doctor).all()
        session.close()
        return doctors

    @doctor_ns.expect(doctor_model)
    def post(self):
        data = request.json

        try:
            session = sessionmaker(bind=engine)()
            crm = data.get("crm")
            crm_uf = data.get("crmUf")
            existing_doctor = (
                session.query(Doctor).filter_by(crm=crm, crmUf=crm_uf).first()
            )
            if existing_doctor:
                return {"message": "Doctor with the same CRM already exists"}, 400

            doctor = Doctor(
                    name=data["name"],
                    crm=data["crm"],
                    crmUf=data["crmUf"],
                )
            session.add(doctor)
            session.commit()
            session.close()

            return {"message": "Doctor created ", "Name": doctor.name}, 201
        except IntegrityError as e:
            return {"message": "Integrity Error"}, 400
        except Exception as e:
            return {"message": "An error occurred", "error": str(e)}, 500


@doctor_ns.route("/<int:doctor_id>")
class DoctorResource(Resource):
    @doctor_ns.marshal_with(doctor_model)
    def get(self, doctor_id):
        session = SessionLocal()
        doctor = session.query(Doctor).filter_by(id=doctor_id).first()
        session.close()

        if doctor:
            return doctor
        else:
            return {"message": "Doctor not found"}, 404

    def delete(self, doctor_id):
        session = SessionLocal()
        doctor = session.query(Doctor).filter_by(id=doctor_id).first()

        if doctor:
            if doctor.patients:
                session.close()
                return {"message": "Cannot delete doctor with patients"}, 400

            session.delete(doctor)
            session.commit()
            session.close()
            return {"message": "Doctor deleted successfully"}
        else:
            session.close()
            return {"message": "Doctor not found"}, 404


@doctor_ns.route("/<int:doctor_id>/patients")
class DoctorPatientListResource(Resource):
    @doctor_ns.marshal_with(patient_model, as_list=True)
    def get(self, doctor_id):
        session = SessionLocal()

        doctor = session.query(Doctor).filter_by(id=doctor_id).first()
        if not doctor:
            session.close()
            return {"message": "Doctor not found"}, 404

        patients = (
            session.query(Patient).filter(Patient.doctors.any(id=doctor_id)).all()
        )
        session.close()
        return patients
