from .database import get_database_interface
from .schemas import Candidate
from datetime import datetime as dt

# CANDIDATE REPOSITORY

class CandidateRepository:
    def __init__(self):
        self.db_interface = get_database_interface()

    def get_candidate_by_phone(self, phone: str):
        """Retrieve a candidate by phone number."""
        with self.db_interface.get_session() as session:
            return session.query(Candidate).filter(Candidate.phone == phone).first()

    def get_candidate_by_id(self, candidate_id: int):
        """Retrieve a candidate by ID."""
        with self.db_interface.get_session() as session:
            return session.query(Candidate).filter(Candidate.id == candidate_id).first()

    def update_interview_status(self, candidate_id: int, status: str):
        """Update the interview status of a candidate."""
        with self.db_interface.get_session() as session:
            candidate = session.query(Candidate).filter(Candidate.id == candidate_id).first()
            if candidate:
                candidate.interview_status = status
                candidate.updated_at = dt.now()
                session.commit()
                return True
            return False

    def save_feedback(self, candidate_id: int, feedback: str):
        """Save feedback for a candidate."""
        with self.db_interface.get_session() as session:
            candidate = session.query(Candidate).filter(Candidate.id == candidate_id).first()
            if candidate:
                candidate.feedback = feedback
                candidate.updated_at = dt.now()
                session.commit()
                return True
            return False

    def get_feedback(self, candidate_id: int):
        """Retrieve the feedback of a candidate."""
        with self.db_interface.get_session() as session:
            candidate = session.query(Candidate).filter(Candidate.id == candidate_id).first()
            return candidate.feedback if candidate else None

    def get_interview_status(self, candidate_id: int):
        """Retrieve the interview status of a candidate."""
        with self.db_interface.get_session() as session:
            candidate = session.query(Candidate).filter(Candidate.id == candidate_id).first()
            return candidate.interview_status if candidate else None

    def save_answer(self, candidate_id: int, answer: str):
        """Save an answer for a candidate (assuming 'answers' field as JSON)."""
        with self.db_interface.get_session() as session:
            candidate = session.query(Candidate).filter(Candidate.id == candidate_id).first()
            if candidate:
                # Assuming answers is a list, we append the new answer
                if not candidate.answers:
                    candidate.answers = []
                candidate.answers.append(answer)
                candidate.updated_at = dt.now()
                session.commit()
                return True
            return False


# JOB OPENING REPOSITORY

# INTERVIEW REPOSITORY