from db import engine, SessionLocal, Base
from models import Doctor, Patient


def create_database():
    # Create the database tables
    Base.metadata.create_all(bind=engine)


def populate_database():
    # Add data to the database
    session = SessionLocal()

    # Doctors
    doctor1 = Doctor(Name="Dr. John Doe", Crm="12345", CrmUf="NY")
    doctor2 = Doctor(Name="Dr. Jane Smith", Crm="67890", CrmUf="CA")

    # Patients
    patient1 = Patient(Name="Alice", BirthDate="1990-01-01", Cpf="11111111111")
    patient2 = Patient(Name="Bob", BirthDate="1985-05-15", Cpf="22222222222")
    patient3 = Patient(Name="Eve", BirthDate="1995-12-31", Cpf="33333333333")

    # Linking doctors and patients
    doctor1.patients.extend([patient1, patient2])
    doctor2.patients.append(patient3)

    # Add the objects to the session and commit changes to the database
    session.add_all([doctor1, doctor2, patient1, patient2, patient3])
    session.commit()
    session.close()


if __name__ == "__main__":
    create_database()
    populate_database()
    print("Database created and populated.")
