from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
import os
from data.ingestors.weaviate_setup import get_context

load_dotenv()

open_api_key = os.getenv('OPENAI_API_KEY')

memory = ConversationBufferMemory(memory_key="history", return_messages=True)

context = get_context()

modelo = "gpt-4o" 
template = f"""
Você é um gerente de um grande banco no Brasil, de especialista em renegociações de dívidas de pessoas jurídicas.
Sua maior especialidade é garantias.
Você deve gerar respostas utilizando o contexto abaixo.
# Contexto
{context}
Você Deve responder apenas perguntas relacionadas a renegociações de dívidas, garantias, tanto de negócio quanto jurídicas.
Em caso de alguma pergunta fora do contexto deve responder: Só falo sobre garantias, você que lute!.
"""

prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", template),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}"),
        ]
    )

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.5,
    api_key=open_api_key)

llm_chain = LLMChain(
    llm=llm,
    prompt=prompt_template,
    verbose=False,
    memory=memory,
)
    
def chat_assistant(question):
    combined_input = f"{context}\n{question}"
    resposta = llm_chain.run(question=combined_input)
    return resposta


