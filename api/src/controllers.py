from .models import WebhookData
from fastapi import Request
import requests

class WhatsappChatFlowController:
    def __init__(self):
        self.conversation_db = {}  # Armazena o estado das conversas

    async def process_webhook(self, request: Request):
        print("Webhook request received")
        data = await request.json()
        print(f"JSON data: {data}")
        self.webhook_data = WebhookData(data)
        
        user_number = self.webhook_data.metadata.phone
        user_message = self.webhook_data.message.content  # Ajuste conforme sua estrutura de dados

        self.process_message(user_number, user_message)

    def process_message(self, user_number, user_message):
        """
        Processa a mensagem recebida e atualiza o estado da conversa.
        """
        if user_number not in self.conversation_db:
            # Novo usuário
            self.conversation_db[user_number] = {
                "nome": "Novo Usuário",
                "tipo_entrevista": "não definido",
                "flow": "inicio",
                "history": []
            }
            welcome_message = "Olá! Parece que é sua primeira vez aqui. Vamos começar sua entrevista para uma vaga?"
            self.send_message_to_whatsapp(user_number, welcome_message)
        else:
            flow = self.conversation_db[user_number]["flow"]
            response = self.manage_chatbot_flow(flow, user_message, user_number)

            # Atualiza o fluxo com base na resposta do usuário
            self.conversation_db[user_number]["flow"] = self.update_flow(flow, user_message, user_number)
            self.send_message_to_whatsapp(user_number, response)

    def send_message_to_whatsapp(self, user_number, message):
        api_url = f"http://api-a-url/send_message/{user_number}"
        payload = {"message": message}
        response = requests.post(api_url, json=payload)
        return response.json()

    def manage_chatbot_flow(self, flow, user_message, user_number):
        if flow == "inicio":
            return self.ask_for_interview_type(user_number)
        elif flow == "escolher_tipo":
            return self.handle_interview_choice(user_message, user_number)
        elif flow.startswith("perguntas_"):
            return self.ask_interview_question(flow, user_message, user_number)
        return "Desculpe, não entendi."

    def ask_for_interview_type(self, user_number):
        self.conversation_db[user_number]["flow"] = "escolher_tipo"
        return "Qual tipo de entrevista você gostaria de fazer? Responda: Engenheiro de Dados, Desenvolvedor Full-stack, ou Estagiário Coder."

    def handle_interview_choice(self, user_message, user_number):
        user_message = user_message.lower()
        if user_message in ["engenheiro de dados", "desenvolvedor full-stack", "estagiário coder"]:
            self.conversation_db[user_number]["tipo_entrevista"] = user_message
            self.conversation_db[user_number]["flow"] = f"perguntas_{user_message.replace(' ', '_')}"
            return f"Ótimo! Vamos iniciar sua entrevista para o cargo {user_message}."
        else:
            return "Por favor, escolha entre Engenheiro de Dados, Desenvolvedor Full-stack ou Estagiário Coder."

    def ask_interview_question(self, flow, user_message, user_number):
        interview_type = flow.split("_")[1]
        if interview_type == "dados":
            return self.engineering_data_questions(user_message, user_number)
        elif interview_type == "desenvolvedor":
            return self.full_stack_questions(user_message, user_number)
        elif interview_type == "estagiário":
            return self.coder_intern_questions(user_message, user_number)
        return "Pergunta não definida."

    def engineering_data_questions(self, user_message, user_number):
        history = self.conversation_db[user_number]["history"]
        questions = [
            "Você tem experiência com Databricks e Apache Spark? Pode descrever um projeto recente onde utilizou essas ferramentas?",
            "Como você garantiria que um pipeline de dados é escalável e fácil de manter? Que estratégias ou práticas você costuma usar?",
            "Fale sobre sua experiência com processos ETL (Extração, Transformação e Carga) e como você lidou com grandes volumes de dados.",
            "Quais são os principais desafios que você enfrentou ao trabalhar com bancos de dados relacionais (SQL Server) e NoSQL (MongoDB)?",
            "Como você desenharia um sistema de Big Data para processar petabytes de dados de forma eficiente?",
            "Você já otimizou um banco de dados para desempenho? Pode descrever como?",
            "Qual é a sua abordagem para gerenciar e monitorar pipelines de dados em produção?",
            "Como você lida com falhas em pipelines de dados? Pode dar um exemplo prático?",
            "Você já implementou uma arquitetura de dados em nuvem (AWS, Azure, GCP)? Pode descrever sua experiência?",
            "Qual é a importância de versionamento de dados em um pipeline de dados?",
            "Fale sobre sua experiência com ferramentas de orquestração de dados, como Apache Airflow.",
            "Como você garante a segurança dos dados em grandes sistemas de Big Data?"
        ]
        
        if len(history) < len(questions):
            return questions[len(history)]
        return "Obrigado! Essa foi a última pergunta da entrevista para Engenheiro de Dados."

    def full_stack_questions(self, user_message, user_number):
        history = self.conversation_db[user_number]["history"]
        questions = [
             "Conte-nos sobre um projeto em que você trabalhou em ambas as partes: frontend e backend. Quais foram os maiores desafios?",
            "Como você aborda o design de interfaces voltadas para o usuário final? Que boas práticas você segue para garantir uma boa usabilidade?",
            "Como você integra bancos de dados relacionais ao backend de uma aplicação? Pode descrever um caso em que fez essa integração utilizando uma API REST?",
            "Como você lida com autenticação e autorização em suas aplicações full-stack?",
            "Fale sobre um desafio que enfrentou ao criar uma API robusta e segura.",
            "Qual é a sua abordagem para testar aplicações full-stack (frontend e backend)?",
            "Você já implementou Continuous Integration e Continuous Deployment (CI/CD)? Como você configura esse processo?",
            "Como você otimiza o desempenho de uma aplicação web no frontend?",
            "Que ferramentas você utiliza para monitorar o desempenho do backend em produção?",
            "Você já trabalhou com contêineres (Docker) em aplicações full-stack? Pode descrever sua experiência?",
            "Como você lida com o gerenciamento de estado no frontend de uma aplicação complexa?",
            "Quais são as principais considerações de segurança ao desenvolver aplicações full-stack?"
        ]
        
        if len(history) < len(questions):
            return questions[len(history)]
        return "Obrigado! Essa foi a última pergunta da entrevista para Desenvolvedor Full-stack."

    def coder_intern_questions(self, user_message, user_number):
        history = self.conversation_db[user_number]["history"]
        questions = [
            "Você já trabalhou com PostgreSQL?",
            "Você tem alguma experiência com Django ou Vue.js? Pode descrever algum projeto em que utilizou essas tecnologias?",
            "Você estará lidando com diversas tecnologias. Como você lida com o aprendizado de novas ferramentas?",
            "Você já trabalhou em projetos utilizando metodologias ágeis (Scrum/Kanban)?",
            "Como você lida com feedbacks e revisões de código?",
            "Fale sobre um projeto onde você trabalhou no ciclo de vida completo do código (desenvolvimento, testes e deploy).",
            "Você tem alguma experiência com APIs REST? Pode descrever como você construiu ou integrou uma API em um projeto?",
            "Fale sobre como você abordaria a resolução de um bug crítico que afeta os usuários.",
            "Você já utilizou controle de versão (Git) em seus projetos? Qual sua abordagem para lidar com conflitos de merge?",
            "Como você lida com a documentação de um projeto em que está trabalhando?",
            "Quais práticas você segue para garantir que o código que escreve seja legível e sustentável?",
            "Quais são suas expectativas ao trabalhar em equipe com desenvolvedores mais experientes?"
        ]
        
        if len(history) < len(questions):
            return questions[len(history)]
        return "Obrigado! Essa foi a última pergunta da entrevista para Estagiário Coder."

    def update_flow(self, current_flow, user_message, user_number):
        history = self.conversation_db[user_number]["history"]
        if len(history) >= 12:
            return "finalizado"
        return current_flow

def get_wpp_chat_flow_controller():
    return WhatsappChatFlowController()
