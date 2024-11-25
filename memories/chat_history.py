from langchain.chains.conversation.memory import ConversationBufferMemory, ConversationBufferWindowMemory

def get_chat_conversation_history_memory():
    return ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )


def get_conversation_history_memory():
    return ConversationBufferMemory(
        memory_key="history", 
        return_messages=True
    )

def get_chat_conversation_window_history_memory():
    return ConversationBufferWindowMemory(
        memory_key="chat_history",
        return_messages=True
    )

