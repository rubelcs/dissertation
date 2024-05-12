from typing import Union
from fastapi import FastAPI,Form, staticfiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.exceptions import HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import PatientRecord
from database import engine
from scripts import add_record, record_exists, get_record_by_patient_id
import time
from cryptography.fernet import Fernet
def load_key():
    with open("encryption_key.txt", "rb") as key_file:
        return key_file.read()

# Load the key
key = load_key()
cipher = Fernet(key)

#create a fastapi app
app = FastAPI()
# Mount a static directory to serve the HTML file
app.mount("/static", StaticFiles(directory="static", html=True), name="static")
class Records(BaseModel):
    patient_id:str
    social_security_number:str
    patient_name: str
    date_of_admission: str
    date_of_birth: str
    gender: str
    contact_number: Union[int, str]
    insurer_name: str


@app.post("/submit_record/")
def submit_patient_record(
    patient_id: str = Form(...),
    social_security_number: str = Form(...),
    patient_name: str = Form(...),
    date_of_admission: str = Form(...),
    date_of_birth: str = Form(...),
    gender: str = Form(...),
    contact_number: str = Form(...),
    insurer_name: str = Form(...),
):
    start_time = time.time()
    encrypted_ssn = cipher.encrypt(social_security_number.encode())
    encrypted_ssn_str = encrypted_ssn.decode('utf-8')  # Convert bytes to string
    db_record = PatientRecord(
        patientid=patient_id,
        social_security_number=encrypted_ssn,
        patient_name=patient_name,
        date_of_admission=date_of_admission,
        date_of_birth=date_of_birth,
        gender=gender,
        contact_number=str(contact_number),
        insurer_name=insurer_name,
    )
    print(db_record)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    db.close()
    add_record(patient_id, str(encrypted_ssn_str), patient_name, date_of_admission, date_of_birth, gender, str(contact_number), insurer_name)
    end_time = time.time()
    print(f"Time taken to add record to db and blockchain: {end_time - start_time} seconds")
    return {"message": "Patient record created successfully and deployed to the blockchain."}


@app.get("/record_exists/{patient_id}")
def check_record_exists(patient_id: str):
    start_time = time.time()
    result = {"record_exists": get_record_by_patient_id(patient_id)}
    end_time = time.time()
    print(f"Time taken to check record existence: {end_time - start_time} seconds")
    return result

# Define a route for serving your results.html page
@app.get("/results", response_class=HTMLResponse)
def get_results():
    start_time = time.time()
    try:
        # Open the results.html file located in the 'static' directory
        with open('static/results.html', 'r') as f:
            html_content = f.read()
            return HTMLResponse(content=html_content, status_code=200)
    except FileNotFoundError:
        # If the file is not found, raise an HTTP 404 error
        raise HTTPException(status_code=404, detail="Results page not found.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)