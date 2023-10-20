# Medical API

The Medical API is a RESTful web service built with Flask and SQLAlchemy that allows you to manage doctors and patients in a medical system.

## Installation

To run the Medical API on your local machine, follow these steps:
I highly suggest you create an virtual enviroment in your machine before starting
- Clone the repository:

```bash
git clone https://github.com/Gustavo-dm/Kogui-DevTest.git
cd Kogui-DevTest
```
- Install the dependecies
```bash
pip install -r requirements.txt
```
- Populate the database with sample data:

```bash
python populate_db.py
```
- Run the server
```bash
python app.py
```

The API will be accessible at http://localhost:5000.

# Endpoints
The Medical API provides the following endpoints:

## Doctors
### GET /doctors
- Returns a list of all doctors in the system. Each doctor object contains id, name, crm, and crmUf.
### GET /doctors/{id}
Returns a single doctor with the specified id.
If the doctor is not found, a 404 status is returned.
The doctor object contains id, name, crm, and crmUf.
### POST /doctors
Creates a new doctor in the system.
Requires a JSON payload with name, crm, and crmUf fields.
The crm field must be unique for each doctor.
Returns a 201 status code upon successful creation.
```json
Request Body Example:
{
  "name": "Dr. John Doe",
  "crm": "12345",
  "crmUf": "SP"
}
```

### GET /doctors/{doctor_id}/patients
Returns a list of all patients linked to the doctor

## Patients
### GET /patients
Returns a list of all patients in the system.
Each patient object contains id, name, birthDate, cpf, and doctors.
The doctors field is a list of linked doctor IDs.
### GET /patients/{id}
Returns a single patient with the specified id.
If the patient is not found, a 404 status is returned.
The patient object contains id, name, birthDate, cpf, and doctors.
The doctors field is a list of linked doctor IDs.
### POST /patients
Creates a new patient in the system.
Requires a JSON payload with name, birthDate, cpf, and doctors fields.
The cpf field must be unique for each patient.
The doctors field should contain a list of doctor IDs to link the patient to.
Returns a 201 status code upon successful creation.
```json
Request Body Example:
{
  "name": "John Smith",
  "birthDate": "1985-05-15",
  "cpf": "11122233344",
  "doctors": [1, 3, 5]
}
```
### GET /patients/<age_group>
Returns a list of patients filtered by age group.
- The age_group parameter is optional and can be one of the following: "jovem", "adulto", or "idoso".
"jovem" filters patients with ages 0-19, "adulto" filters ages 20-59, and "idoso" filters ages 60+.
- If no age_group is provided, all patients will be returned.