from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_restx import Api
from doctor_routes import doctor_ns
from patient_routes import patient_ns
DATABASE_URI = 'mysql://root:1234@localhost:3306/kogui'

app = Flask(__name__)

engine = create_engine(DATABASE_URI)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

api = Api(app, title="Medical API", description="API for managing doctors and patients")

api.add_namespace(doctor_ns)
api.add_namespace(patient_ns)

if __name__ == "__main__":

    app.run(debug=True)
