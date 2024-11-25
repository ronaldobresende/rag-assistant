from langchain.prompts.chat import (
    ChatPromptTemplate, 
    SystemMessagePromptTemplate, 
    HumanMessagePromptTemplate
)

# Configurar o prompt para a cadeia de conversação
system_template = """
Você é um assistente do banco. Responda às perguntas com base nos documentos fornecidos.
Nunca inclua informações pessoais sensíveis (PII) nas respostas.
Responda apenas a perguntas relacionadas ao banco Itaú. Se a pergunta mencionar outro banco, informe que você só pode responder sobre o banco Itaú.
"""
human_template = """
Contexto:
{context}

Pergunta:
{question}
"""
chat_prompt_garantias = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template(human_template),
])