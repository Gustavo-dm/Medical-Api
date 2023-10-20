from flask import request
from flask_restx import Namespace, Resource, fields
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker, joinedload
from models import Doctor, Patient
from db import engine
from datetime import datetime

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

patient_ns = Namespace("patients", description="Patient related operations")

doctor_model = patient_ns.model(
    "Doctor",
    {
        "id": fields.Integer(description="Doctor Id"),
    },
)

patient_model = patient_ns.model(
    "Patient",
    {
        "id": fields.Integer(description="Patient Id"),
        "name": fields.String(required=True, description="Patient name"),
        "birthDate": fields.String(required=True, description="Patient birth date"),
        "cpf": fields.String(required=True, description="Patient CPF"),
        "doctors": fields.List(
            fields.Nested(doctor_model),
            required=True,
            description="List of linked doctors",
        ),
    },
)


@patient_ns.route("/")
class PatientListResource(Resource):
    @patient_ns.marshal_with(patient_model, as_list=True)
    def get(self):
        session = SessionLocal()

        patients = session.query(Patient).options(joinedload(Patient.doctors)).all()

        session.close()
        return patients

    @patient_ns.expect(patient_model)
    def post(self):
        data = request.json

        try:
            session = sessionmaker(bind=engine)()
            cpf = data.get("cpf")
            existing_patient = session.query(Patient).filter_by(cpf=cpf).first()
            if existing_patient:
                return {"message": "CPF already exists"}, 400

            doctor_ids = data.get("doctors", [])
            if not doctor_ids:
                return {"message": "Patient must have at least one doctor"}, 400

            doctors = session.query(Doctor).filter(Doctor.id.in_(doctor_ids)).all()

            patient = Patient(
                name=data["name"],
                birthDate=data["birthDate"],
                cpf=data["cpf"],
                doctors=doctors,
            )

            session.add(patient)
            session.commit()
            session.close()

            return {"message": "Patient created ", "Name": patient.name}, 201
        except IntegrityError as e:
            return {"message": "Integrity Error: "}, 400
        except Exception as e:
            return {"message": "An error occurred", "error": str(e)}, 500


@patient_ns.route("/<int:id>")
class PatientResource(Resource):
    @patient_ns.marshal_with(patient_model)
    def getbyId(self, id):
        session = SessionLocal()
        patient = (
            session.query(Patient)
            .filter_by(id=id)
            .options(joinedload(Patient.doctors))
            .all()
        )
        session.close()

        if not patient:
            return {"message": "Patient not found"}, 404

        return patient

    def delete(self, id):
        session = SessionLocal()
        patient = session.query(Patient).filter_by(id=id).first()

        if patient:
            session.delete(patient)
            session.commit()
            session.close()
            return {"message": "Patient deleted successfully"}
        else:
            session.close()
            return {"message": "Patient not found"}, 404


@patient_ns.route("/<string:age_group>")
class PatientFilteredListResource(Resource):
    @patient_ns.marshal_with(patient_model, as_list=True)
    def get(self, age_group):
        session = SessionLocal()

        current_date = datetime.today()

        if age_group:
            if age_group == "jovem":
                birth_date_limit = current_date.replace(year=current_date.year - 19)
            elif age_group == "adulto":
                birth_date_limit = current_date.replace(year=current_date.year - 20)
            elif age_group == "idoso":
                birth_date_limit = current_date.replace(year=current_date.year - 60)
            else:
                return {"message": "Invalid age group filter"}, 400

            patients = (
                session.query(Patient)
                .options(joinedload(Patient.doctors))
                .filter(Patient.birthDate <= birth_date_limit)
                .all()
            )

        else:
            patients = session.query(Patient).all()

        session.close()
        return patients
