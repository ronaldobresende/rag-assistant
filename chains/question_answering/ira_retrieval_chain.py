"""
Módulo para a cadeia de recuperação IRA.
"""

from typing import Optional
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.runnables import Runnable
from langchain_core.runnables.utils import Input, Output
from langchain_core.language_models import BaseLanguageModel
from langchain_core.retrievers import BaseRetriever
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables.config import RunnableConfig
from data.preprocessors.guardrails import detect_and_preserve_pii, check_bank_name
from prompts.document_prompt import document_prompt
from prompts.prompt_garantias import prompt_garantias


class IraRetrievalChain(Runnable[Input, Output]):
    """
    Classe para a cadeia de recuperação IRA.
    """

    def __init__(
        self,
        llm: BaseLanguageModel,
        retriever: BaseRetriever,
        memory: InMemoryChatMessageHistory
    ) -> None:
        """
        Inicializa a cadeia de recuperação IRA.

        Args:
            llm (BaseLanguageModel): O modelo de linguagem.
            retriever (BaseRetriever): O recuperador de documentos.
            memory (InMemoryChatMessageHistory): O histórico de mensagens do chat.
        """
        self.__llm = llm
        self.__retriever = retriever
        self.__memory = memory

    def check_bank(self, user_input: Input) -> Optional[str]:
        """
        Verifica o nome do banco no input.

        Args:
            user_input (Input): A entrada do usuário.

        Returns:
            Optional[str]: O resultado da verificação do banco, se houver.
        """
        bank_check_result = check_bank_name(user_input)
        if bank_check_result != user_input:
            return bank_check_result
        return None

    def detect_pii(self, user_input: Input) -> str:
        """
        Detecta e preserva informações pessoais identificáveis (PII) no user_input.

        Args:
            user_input (Input): A entrada do usuário.

        Returns:
            str: A entrada com PII detectada e preservada.
        """
        return detect_and_preserve_pii(user_input)

    def format_chat_history(self) -> str:
        """
        Formata o histórico de chat para ser usado no prompt.

        Returns:
            str: O histórico de chat formatado.
        """
        return "\n".join([
            f"Usuário: {msg.content}" if isinstance(msg, HumanMessage)
            else f"IA: {msg.content}"
            for msg in self.__memory.messages
        ])

    def create_chains(self) -> Runnable:
        """
        Cria as cadeias de documentos e recuperação.

        Returns:
            Runnable: A cadeia de recuperação criada.
        """

        prompt=prompt_garantias

        chat_history = self.format_chat_history()

        partial_prompt = prompt.partial(chat_history=chat_history)

        combine_docs_chain = create_stuff_documents_chain(
            llm=self.__llm,
            prompt=partial_prompt,
            document_prompt=document_prompt,
            document_variable_name="context"
        )
        return create_retrieval_chain(
            retriever=self.__retriever,
            combine_docs_chain=combine_docs_chain
        )

    def update_chat_history(self, question: str, answer: str) -> None:
        """
        Atualiza o histórico de chat com a nova pergunta e resposta.

        Args:
            question (str): A pergunta do usuário.
            answer (str): A resposta da IA.
        """
        self.__memory.add_messages([
            HumanMessage(content=question),
            AIMessage(content=answer)
        ])

    def invoke(
        self,
        input: Input,
        config: Optional[RunnableConfig] = None
    ) -> Output:
        """
        Invoca a cadeia de recuperação com a entrada do usuário.

        Args:
            input (Input): A entrada do usuário.
            config (Optional[RunnableConfig]): A configuração opcional.

        Returns:
            Output: A resposta da cadeia de recuperação.
        """
        bank_check_result = self.check_bank(input)
        if bank_check_result:
            return {"answer": bank_check_result}

        question = self.detect_pii(input)
        
        chain = self.create_chains()
        response = chain.invoke({"input": question}, config)

        self.update_chat_history(question, response.get("answer"))
        return response
