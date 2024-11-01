from .models import WebhookData, FlowState, MAIN_CTX_PROMPT
from .repository import candidate_repository
from fastapi import Request
from .chatgpt import get_chatgpt_response
from .whatsapp import send_whatsapp_message
import json

class WhatsappChatFlowController:
    def __init__(self):
        self.flow_state: FlowState = None
        self.status_phase = None
        self.webhook_data = None
        self.candidate = None

    async def process_webhook(self, request: Request):
        data = await request.json()
        self.webhook_data = WebhookData.from_payload(data)
        return self.webhook_data

    def _is_valid_start(self):
        if self.webhook_data.content.message_text == "/iniciar-entrevista" or candidate_repository.get_candidate_by_phone(self.webhook_data.metadata.phone):
            return True
        print("Not a valid start, quitting and awaiting ...")
        return False

    def _get_candidate(self):
        candidate = candidate_repository.get_candidate_by_phone(self.webhook_data.metadata.phone)
        if not candidate:
            candidate = candidate_repository.create_candidate(self.webhook_data.metadata.phone)
            print(f"New candidate created: {candidate}, {candidate.id}")
        else:
            print(f"Existing candidate: {candidate}, {candidate.id}")
        self.candidate = candidate
    
    def _set_flow_state(self):
        candidate_status = candidate_repository.get_interview_status(self.candidate.id)
        candidate_status, self.status_phase = candidate_status.split("_")
        if candidate_status == FlowState.WELCOME.name:
            self.flow_state = FlowState.WELCOME
        elif candidate_status == FlowState.BASIC_INFO.name:
            self.flow_state = FlowState.BASIC_INFO
        print(f"Flow state: {self.flow_state.name}, {self.status_phase}")

    def _execute_flow(self):
        # first generate initial prompt
        if self.status_phase == "1":
            print("handling phase 1")
            prompt = self.flow_state.value.initial_prompt
            chatgpt_response = get_chatgpt_response(MAIN_CTX_PROMPT, prompt)
            print(f"gpt_response: {chatgpt_response}")
            send_whatsapp_message(self.webhook_data.metadata.phone, chatgpt_response)
            print("message sent")
            candidate_repository.update_interview_status(self.candidate.id, f"{self.flow_state.name}_2")
        elif self.status_phase == "2":
            print("handling phase 2")
            prompt = self.flow_state.value.evaluation_prompt
            chatgpt_response = get_chatgpt_response(MAIN_CTX_PROMPT, f"{prompt} [mensagem do usuario]: {self.webhook_data.content.message_text}")
            print(f"gpt_response: {chatgpt_response}")
            if type(chatgpt_response) == str:
                chatgpt_response_json = self._parse_chatgpt_response(chatgpt_response)
            if self.flow_state == FlowState.WELCOME:
                self._handle_welcome(chatgpt_response_json)
            elif self.flow_state == FlowState.BASIC_INFO:
                self._handle_basic_info(chatgpt_response_json)

    def _parse_chatgpt_response(self, chatgpt_response):
        #```json
        #    {
        #    "start_interview": true
        #    }
        #    ```
        extracted_data = chatgpt_response.split("```json")[1].split("```")[0]
        return json.loads(extracted_data)

    def _handle_welcome(self, chatgpt_response):
        print("Handling welcome")
        print(f"ChatGPT response: {chatgpt_response}")
        print(f"{type(chatgpt_response)}")
        print(f"{chatgpt_response.get('start_interview')}")
        print(f"{type(chatgpt_response.get('start_interview'))}")
        if chatgpt_response.get("start_interview"):
            print("Starting interview")
            chatgpt_response = get_chatgpt_response(MAIN_CTX_PROMPT, self.flow_state.value.ok_response_prompt)
            send_whatsapp_message(self.webhook_data.metadata.phone, chatgpt_response)
            self.flow_state = FlowState.BASIC_INFO
            candidate_repository.update_interview_status(self.candidate.id, f"{self.flow_state.name}_2")
            send_whatsapp_message(self.webhook_data.metadata.phone, self.flow_state.value.initial_prompt)
        else:
            send_whatsapp_message(self.webhook_data.metadata.phone, self.flow_state.value.quit_response_prompt)

    def _handle_basic_info(self, chatgpt_response):
        print("Handling basic info")
        print(f"ChatGPT response: {chatgpt_response}")
        if chatgpt_response.get("full_name") and chatgpt_response.get("age") and chatgpt_response.get("cpf"):
            candidate_repository.update_basic_info(self.candidate.id, chatgpt_response.get("full_name"), chatgpt_response.get("age"), chatgpt_response.get("cpf"))
            send_whatsapp_message(self.webhook_data.metadata.phone, f"{self.flow_state.value.ok_response_prompt} [nome do usuario]: {chatgpt_response.get('full_name')}")
        else:
            raise Exception("Missing data")

    def handle_flow(self):
        print("Handling flow")
        if self._is_valid_start():
            self._get_candidate()
            self._set_flow_state()
            self._execute_flow()
        return {
            "message": "Success"
        }

def get_chat_flow_controller():
    return WhatsappChatFlowController()