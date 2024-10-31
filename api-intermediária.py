import requests

conversation_db = {}  # Armazena o estado das conversas

def process_message(user_number, user_message):
    """
    Processa a mensagem recebida e atualiza o estado da conversa.
    """
    if user_number not in conversation_db:
        # Novo usuário
        conversation_db[user_number] = {
            "nome": "Novo Usuário",
            "tipo_entrevista": "não definido",
            "flow": "inicio",
            "history": []
        }
        welcome_message = "Olá! Parece que é sua primeira vez aqui. Vamos começar sua entrevista para uma vaga?"
        send_message_to_whatsapp(user_number, welcome_message)
    else:
        flow = conversation_db[user_number]["flow"]
        response = manage_chatbot_flow(flow, user_message, user_number)

        # Atualiza o fluxo com base na resposta do usuário
        conversation_db[user_number]["flow"] = update_flow(flow, user_message, user_number)
        send_message_to_whatsapp(user_number, response)

def send_message_to_whatsapp(user_number, message):
    api_url = f"http://api-a-url/send_message/{user_number}"
    payload = {"message": message}
    response = requests.post(api_url, json=payload)
    return response.json()

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
    return "Qual tipo de entrevista você gostaria de fazer? Responda: Engenheiro de Dados, Desenvolvedor Full-stack, ou Estagiário Coder."

def handle_interview_choice(user_message, user_number):
    user_message = user_message.lower()
    if user_message in ["engenheiro de dados", "desenvolvedor full-stack", "estagiário coder"]:
        conversation_db[user_number]["tipo_entrevista"] = user_message
        conversation_db[user_number]["flow"] = f"perguntas_{user_message.replace(' ', '_')}"
        return f"Ótimo! Vamos iniciar sua entrevista para o cargo {user_message}."
    else:
        return "Por favor, escolha entre Engenheiro de Dados, Desenvolvedor Full-stack ou Estagiário Coder."

def ask_interview_question(flow, user_message, user_number):
    interview_type = flow.split("_")[1]
    if interview_type == "dados":
        return engineering_data_questions(user_message, user_number)
    elif interview_type == "desenvolvedor":
        return full_stack_questions(user_message, user_number)
    elif interview_type == "estagiário":
        return coder_intern_questions(user_message, user_number)
    return "Pergunta não definida."

def engineering_data_questions(user_message, user_number):
    history = conversation_db[user_number]["history"]
    questions = [
        "Você tem experiência com Databricks e Apache Spark?",
        # ... mais perguntas
    ]
    
    if len(history) < len(questions):
        return questions[len(history)]
    return "Obrigado! Essa foi a última pergunta da entrevista para Engenheiro de Dados."

def full_stack_questions(user_message, user_number):
    history = conversation_db[user_number]["history"]
    questions = [
        "Conte-nos sobre um projeto em que você trabalhou em ambas as partes: frontend e backend.",
        # ... mais perguntas
    ]
    
    if len(history) < len(questions):
        return questions[len(history)]
    return "Obrigado! Essa foi a última pergunta da entrevista para Desenvolvedor"
