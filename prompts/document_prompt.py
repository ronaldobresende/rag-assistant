from langchain_core.prompts import PromptTemplate

document_prompt = PromptTemplate(
    input_variables=["page_content", "history", "question"],
    template="""\
`Context:`
"{question}"
content: {page_content}
history: {history}
""",
)