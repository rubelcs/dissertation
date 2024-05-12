from sqlalchemy import create_engine, Column, Integer, String, Date
from database import Base, engine

class PatientRecord(Base):
    __tablename__ = 'patient_records'
    patientid = Column(Integer, primary_key=True, index=True)
    social_security_number = Column(String(255), nullable=False)
    patient_name = Column(String(255), nullable=False)
    date_of_admission = Column(Date, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(10), nullable=False)
    contact_number = Column(String(255), nullable=True)
    insurer_name = Column(String(255), nullable=True)

Base.metadata.create_all(bind=engine)