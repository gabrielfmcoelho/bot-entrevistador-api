from pydantic import BaseModel
from enum import Enum

class CandidateForm(BaseModel):
    pass

class JobOpeningForm(BaseModel):
    pass

class InterviewForm(BaseModel):
    pass

class WebhookMessage(BaseModel):
    audio: str|None = None
    document: str|None = None
    image: str|None = None
    video: str|None = None
    message_text: str|None = None
    reaction_message: str|None = None
    sticker: str|None = None

    # when initializing the class, parse the JSON data into the class attributes, every attribute has the same name as the JSON key except for the message_text and reaction_message that are message['text'] and reaction['message']
    def __init__(self, payload_data: dict):
        self.audio = payload_data.get('audio', None)
        self.document = payload_data.get('document', None)
        self.image = payload_data.get('image', None)
        self.video = payload_data.get('video', None)
        self.message_text = payload_data.get('message', None).get('text', None)
        self.reaction_message = payload_data.get('reaction', None).get('message', None)
        self.sticker = payload_data.get('sticker', None)

class WebhookMetadata(BaseModel):
    quoted_message: str|None = None
    pushname: str|None = None
    from_contact: str|None = None
    contact: str|None = None
    phone: str|None = None

    def __init__(self, payload_data: dict):
        self.quoted_message = payload_data.get('quoted_message', None)
        self.pushname = payload_data.get('pushname', None)
        self.from_contact = payload_data.get('from', None)
        self.contact = payload_data.get('contact', None)
        self.parse_phone()

    def parse_phone(self):
        if self.from_contact:
            self.phone = self.from_contact.split('@s.')[0]

class WebhookData(BaseModel):
    content: WebhookMessage
    metadata: WebhookMetadata

    def __init__(self, payload_data: dict):
        self.message = WebhookMessage(payload_data)
        self.metadata = WebhookMetadata(payload_data)

class FlowContent(BaseModel):
    initial_prompt: str
    evaluation_prompt: str
    ok_response_prompt: str
    error_response_prompt: str
    quit_response_prompt: str|None = None

class FlowState(Enum):
    WELCOME = FlowContent(
        initial_prompt="Olá! Parece que é sua primeira vez aqui. Vamos começar sua entrevista para uma vaga?",
        evaluation_prompt="Você gostaria de continuar a entrevista?",
        ok_response_prompt="Ótimo! Vamos continuar.",
        error_response_prompt="Desculpe, não entendi. Você gostaria de continuar a entrevista?",
        quit_response_prompt="Ok, se precisar de mais alguma coisa, estou por aqui."
    )
    PRESENT_JOB_OFFER = "..."
    BASIC_INFO = "..."
    EXPERIENCE = "..."
    EDUCATION = "..."
    SKILLS = "..."
    FEEDBACK = "..."
    FINISH = "..."