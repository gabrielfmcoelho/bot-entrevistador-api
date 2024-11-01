from pydantic import BaseModel
from enum import Enum

class CandidateForm(BaseModel):
    pass

class JobOpeningForm(BaseModel):
    pass

class InterviewForm(BaseModel):
    pass

class WebhookMessage(BaseModel):
    audio: str | None = None
    document: str | None = None
    image: str | None = None
    video: str | None = None
    message_text: str | None = None

    @classmethod
    def from_payload(cls, payload_data: dict):
        return cls(
            audio=payload_data.get('audio', None),
            document=payload_data.get('document', None),
            image=payload_data.get('image', None),
            video=payload_data.get('video', None),
            message_text=payload_data.get('message', {}).get('text', None)
        )

class WebhookMetadata(BaseModel):
    quoted_message: str | None = None
    pushname: str | None = None
    from_contact: str | None = None
    contact: str | None = None
    phone: str | None = None

    @classmethod
    def from_payload(cls, payload_data: dict):
        instance = cls(
            quoted_message=payload_data.get('quoted_message', None),
            pushname=payload_data.get('pushname', None),
            from_contact=payload_data.get('from', None),
            contact=payload_data.get('contact', None)
        )
        instance.parse_phone()
        return instance

    def parse_phone(self):
        if self.from_contact:
            self.phone = self.from_contact.split('@s.')[0]

class WebhookData(BaseModel):
    content: WebhookMessage
    metadata: WebhookMetadata

    @classmethod
    def from_payload(cls, payload_data: dict):
        content = WebhookMessage.from_payload(payload_data)
        metadata = WebhookMetadata.from_payload(payload_data)
        return cls(content=content, metadata=metadata)
    
class FlowContent(BaseModel):
    name: str
    initial_prompt: str
    evaluation_prompt: str
    ok_response_prompt: str
    error_response_prompt: str
    quit_response_prompt: str|None = None

MAIN_CTX_PROMPT = "Você é uma assistente virtual que ajuda a realizar entrevistas de emprego, avaliando candidatos, extraindo informações e dando feedbacks. Seu dialogo deve ser casual, informal e amigável para deixar o candidato confortavel. Você irá guiar o candidato por um fluxo de perguntas e respostas, e ao final, irá avaliar as respostas e dar um feedback."

class FlowState(Enum):
    WELCOME: FlowContent = FlowContent(
        name='welcome',
        # 1
        initial_prompt=f"Crie uma mensagem de boas-vindas para o usuário que está iniciando a entrevista.",
        # 2
        evaluation_prompt="Verifique se na mensagem enviada pelo usuário, se ele gostaria de iniciar a entrevista e retorne apenas um JSON com a chave 'start_interview' e o valor 'true' ou 'false'",
        ok_response_prompt=f"Você ja questionou se o usuario gostaria de iniciar a entrevista e ele disse sim. Crie uma mensagem apenas informando que a entrevista será iniciada já que ele concordou e o usuário será guiado por um fluxo de perguntas e respostas.",
        error_response_prompt="Desculpe, não entendi. Você gostaria de continuar a entrevista?",
        quit_response_prompt="Ok, se precisar de mais alguma coisa, estou por aqui."
    )
    BASIC_INFO: FlowContent = FlowContent(
        name='basic_info',
        # 1
        initial_prompt=f"Vamos começar com algumas informações básicas. Pergunte ao usuário qual é o seu nome completo, idade e cpf.",
        # 2
        evaluation_prompt="Extraia da mensagem do usuario: nome completo, idade e cpf e me retorne apenas um JSON com as chaves 'full_name', 'age' e 'cpf'.",
        ok_response_prompt=f"Crie uma mensagem de agradecimento, chamando o usuário pelo nome e informando que seguiremos para a próxima etapa.",
        error_response_prompt="Desculpe, não entendi. Você gostaria de continuar a entrevista?",
        quit_response_prompt="Ok, se precisar de mais alguma coisa, estou por aqui."
    )