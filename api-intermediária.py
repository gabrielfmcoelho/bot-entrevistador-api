from fastapi import FastAPI, WebSocket
import requests
import json

app = FastAPI()

# Base de dados simulada (em produção use uma base de dados real)
conversation_db = {}  # Simula um banco de dados

@app.get("/check_conversation/{cpf}")
async def check_conversation(cpf: str):
    if cpf in conversation_db:
        return {"message": "Usuário já registrado.", "conversation": conversation_db[cpf]}
    else:
        return {"message": "Nenhuma conversa encontrada para este CPF."}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()  # Recebe mensagem via WebSocket
        user_message = process_message(data)  # Processa a mensagem do usuário
        user_number = get_user_number_from_message(data)  # Extrai o número do usuário
        
        # Verifica se o número do usuário já existe no "banco de dados"
        if user_number not in conversation_db:
            conversation_db[user_number] = {"nome": "Novo Usuário", "tipo_entrevista": "não definido", "flow": "inicio", "history": []}

            # Chama a API externa ao iniciar a entrevista
            api_data = call_external_api(user_number)

            welcome_message = f"Olá! Parece que é sua primeira vez aqui. {api_data['message']} Vamos começar sua entrevista para uma vaga?"
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

def process_message(data):
    """
    Lógica para processar a mensagem recebida da API A.
    Converte os dados recebidos de JSON para dicionário e retorna a mensagem do usuário.
    """
    try:
        message_data = json.loads(data)  # Converte a string JSON em dicionário
        return message_data.get("message", "")  # Retorna a mensagem do campo "message"
    except json.JSONDecodeError:
        return ""  # Caso a conversão falhe, retorna uma string vazia

def get_user_number_from_message(data):
    """
    Extrai o número do usuário da mensagem recebida da API A.
    Converte os dados recebidos de JSON para dicionário e retorna o número do usuário.
    """
    try:
        message_data = json.loads(data)  # Converte a string JSON em dicionário
        return message_data.get("user_number", "")  # Retorna o número do campo "user_number"
    except json.JSONDecodeError:
        return ""  # Caso a conversão falhe, retorna uma string vazia

# Função para fazer a chamada à API externa
def call_external_api(user_number):
    """
    Faz uma requisição GET para a API externa e retorna os dados.
    """
    api_url = f"http://195.200.0.244:3001/api/user/{user_number}"  # Substitua o endpoint conforme necessário
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()  # Retorna os dados da API externa como JSON
        else:
            return {"message": "Não conseguimos obter dados no momento."}
    except Exception as e:
        return {"message": f"Erro ao acessar a API externa: {str(e)}"}

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

# Perguntas para Engenheiro de Dados
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

# Perguntas para Desenvolvedora Full-stack
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

# Perguntas para Estagiário Coder
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

# Função para enviar dados para a API C (ChatGPT)
def get_chatgpt_response(user_message):
    api_url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer YOUR_CHATGPT_API_KEY",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": user_message}]
    }
    response = requests.post(api_url, json=data, headers=headers)
    return response.json().get("choices")[0]["message"]["content"]

def update_flow(current_flow, user_message, user_number):
    history = conversation_db[user_number]["history"]
    if len(history) >= 12:
        return "finalizado"
    return current_flow

def send_message_to_api_a(user_number, message):
    api_a_url = f"http://api-a-url/send_message/{user_number}"
    payload = {"message": message}
    response = requests.post(api_a_url, json=payload)
    return response.json()
