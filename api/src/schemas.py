from sqlalchemy import Column, Integer, String, Boolean, JSON, DateTime, Text
from datetime import datetime as dt

from .database import get_database_interface

db_interface = get_database_interface()

Base = db_interface.get_declarative_base()

# Candidate table

class Candidate(Base):
    __tablename__ = 'candidate'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    phone = Column(String(15), nullable=False)
    cpf = Column(String(11), nullable=False, unique=True)
    full_name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    address = Column(String(255), nullable=True)
    education = Column(String(50), nullable=True)
    experience = Column(JSON, nullable=True) # List of past experiences in JSON format
    #Text ou JSON?
    interview_status = Column(String(20), nullable=False)  # Interview status (flow moment)
    skills = Column(JSON, nullable=True) #List of skills in JSON format
    #Text ou JSON?
    feedback = Column(String(255), nullable=True)  
    score = Column(Integer, nullable=True)  
    
    created_at = Column(DateTime, default=dt.now)
    updated_at = Column(DateTime, default=dt.now, onupdate=dt.now)

# Interview table

# JobOpening table