from .database import get_database_interface

db_interface = get_database_interface()

Base = db_interface.get_declarative_base()

# Candidate table

# Interview table

# JobOpening table