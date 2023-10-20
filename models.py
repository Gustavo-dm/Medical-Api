from sqlalchemy import Column, String, Date, Table, ForeignKey, Integer
from sqlalchemy.orm import relationship
from db import Base


class Doctor(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(255), index=True)
    crm = Column(String(32), index=True)
    crmUf = Column(String(2))
    patients = relationship(
        "Patient", secondary="doctors_patients", back_populates="doctors"
    )

    def __init__(self, name, crm, crmUf):
        self.name = name
        self.crm = crm
        self.crmUf = crmUf


class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(32), index=True)
    birthDate = Column(Date)
    cpf = Column(String(11), index=True)

    doctors = relationship(
        "Doctor", secondary="doctors_patients", back_populates="patients"
    )


# Relacionamento muitos-para-muitos entre Doctor e Patient
association_table = Table(
    "doctors_patients",  # Changed the table name to doctors_patients to match the relationship
    Base.metadata,
    Column(
        "doctor_id", Integer, ForeignKey("doctors.id")
    ),  # Changed the data type to Integer
    Column(
        "patient_id", Integer, ForeignKey("patients.id")
    ),  # Changed the data type to Integer
)

Doctor.patients = relationship(
    "Patient", secondary=association_table, back_populates="doctors"
)
Patient.doctors = relationship(
    "Doctor", secondary=association_table, back_populates="patients"
)
