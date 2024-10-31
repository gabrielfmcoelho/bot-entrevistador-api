from fastapi import APIRouter, HTTPException, Depends, Request
from .models import CandidateForm, InterviewForm
from .controllers import get_chat_flow_controller

router = APIRouter(
    prefix="/api",
    tags=["api"],
    responses={404: {"description": "Not found"}},
)

# PRINCIPAL ROTA, O RESTANTE PODE IMPLEMENTAR DEPOIS OU NEM IMPLEMENTAR
@router.post("/webhook")
async def webhook(request: Request, controller=Depends(get_chat_flow_controller)):
    controller.process_webhook(request)
    return controller.handle_flow()

# ROTAS PARA CRIAR SISTEMA DE ENTREVISTAS COM POSTAGEM VAGAS, CANDIDATOS E ACOMPANHAMENTO DE ENTREVISTAS
@router.post("/candidates")
async def create_candidate(request: CandidateForm):
    pass

@router.get("/candidates")
async def get_candidates(id: int=None, cpf: str=None, phone: str=None):
    pass

@router.get("/candidates/{id}/interviews")
async def get_candidate_interviews(id: int, interview_id: int=None, interview_status: str=None):
    pass

@router.post("/job_openings")
async def create_job_opening(request: InterviewForm):
    pass

@router.get("/job_openings")
async def get_job_openings(id: int):
    pass

@router.get("/job_openings/{id}/candidates")
async def get_job_opening_candidates(id: int):
    pass

@router.post("/job_openings/{id}/candidates/{candidate_id}")
async def add_candidate_to_job_opening(id: int, candidate_id: int):
    pass

@router.get("/job_openings/{id}/candidates/{candidate_id}/interview")
async def create_interview(id: int, candidate_id: int):
    pass
