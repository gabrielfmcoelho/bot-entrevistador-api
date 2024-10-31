from .models import WebhookData, FlowState
from fastapi import Request

class WhatsappChatFlowController:
    def __init__(self):
        self.flow_state: FlowState = FlowState.WELCOME
        self.webhook_data = None

    async def process_webhook(self, request: Request):
        print("Webhook request received")
        data = await request.json()
        print(f"JSON data: {data}")
        self.webhook_data = WebhookData(data)
        print(f"Webhook data: {self.webhook_data}")

    def _is_first_time(self):
        #candidate = get_candidate_by_phone(self.webhook_data.metadata.phone)
        #if not candidate:
        #    self.flow_state = FlowState.WELCOME
        pass

    def handle_flow(self):
        print("Handling flow")
        # ...
        return {
            "message": "Success"
        }

def get_wpp_chat_flow_controller():
    return WhatsappChatFlowController()