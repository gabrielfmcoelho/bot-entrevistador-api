import requests
import json

def process_message(self, message: WebhookRequest):
    """
    Process the incoming message from the webhook.
    """
    if message.metadata.phone not in conversation_db:
        conversation_db[message.metadata.phone] = {
            "nome": "Novo Usuário",
            "tipo_entrevista": "não definido",
            "flow": "inicio",
            "history": []
            }
        welcome_message = f"Olá! Parece que é sua primeira vez aqui. Vamos começar sua entrevista para uma vaga?"
        await websocket.send_text(welcome_message)
    else:
        flow = conversation_db[user_number]["flow"]
        response = manage_chatbot_flow(flow, user_message, user_number)

        # Envia mensagem para a API C (ChatGPT/Gemini) para gerar uma resposta se necessário
        chatgpt_response = get_chatgpt_response(user_message)
        conversation_db[user_number]["history"].append({"user": user_message, "bot": chatgpt_response})

        # Atualiza o fluxo com base na resposta do usuário
        conversation_db[user_number]["flow"] = update_flow(flow, user_message, user_number)
        send_message_to_api_a(user_number, chatgpt_response)

        await websocket.send_text(f"Resposta enviada para {user_number}: {chatgpt_response}")

def manage_chatbot_flow(flow, user_message, user_number):
    if flow == "inicio":
        return ask_for_interview_type(user_number)
    elif flow == "escolher_tipo":
        return handle_interview_choice(user_message, user_number)
    elif flow.startswith("perguntas_"):
        return ask_interview_question(flow, user_message, user_number)
    return "Desculpe, não entendi."

def ask_for_interview_type(user_number):
    conversation_db[user_number]["flow"] = "escolher_tipo"
    return "Qual tipo de entrevista você gostaria de fazer? Responda: Engenheiro de Dados, Desenvolvedora Full-stack, ou Estagiário Coder."

def handle_interview_choice(user_message, user_number):
    user_message = user_message.lower()
    if user_message in ["engenheiro de dados", "desenvolvedora full-stack", "estagiário coder"]:
        conversation_db[user_number]["tipo_entrevista"] = user_message
        conversation_db[user_number]["flow"] = f"perguntas_{user_message.replace(' ', '_')}"
        return f"Ótimo! Vamos iniciar sua entrevista para o cargo {user_message}."
    else:
        return "Por favor, escolha entre Engenheiro de Dados, Desenvolvedora Full-stack ou Estagiário Coder."

# Fluxo de perguntas específicas para as entrevistas
def ask_interview_question(flow, user_message, user_number):
    interview_type = flow.split("_")[1]
    if interview_type == "engenheiro":
        return engineering_data_questions(user_message, user_number)
    elif interview_type == "desenvolvedora":
        return full_stack_questions(user_message, user_number)
    elif interview_type == "estagiário":
        return coder_intern_questions(user_message, user_number)
    return "Pergunta não definida."

### Engenheiro de Dados - Perguntas (12 no mínimo)
def engineering_data_questions(user_message, user_number):
    history = conversation_db[user_number]["history"]
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

### Desenvolvedora Full-stack - Perguntas (12 no mínimo)
def full_stack_questions(user_message, user_number):
    history = conversation_db[user_number]["history"]
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
    return "Obrigado! Essa foi a última pergunta da entrevista para Desenvolvedora Full-stack."

### Estagiário Coder - Perguntas (12 no mínimo)
def coder_intern_questions(user_message, user_number):
    history = conversation_db[user_number]["history"]
    questions = [
        "Você já trabalhou com PostgreSQL? Como você criaria uma API para manipular dados em um banco de dados relacional?",
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

def update_flow(current_flow, user_message, user_number):
    history = conversation_db[user_number]["history"]
    if len(history) >= 12:
        return "finalizado"
    return current_flow