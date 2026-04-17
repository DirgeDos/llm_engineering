import os
from pathlib import Path

from langchain_community.embeddings import DashScopeEmbeddings
from langchain_milvus import Milvus
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.messages import SystemMessage, HumanMessage, convert_to_messages
from langchain_core.documents import Document

from dotenv import load_dotenv

from week5.embedding import text_embedding
from week5.gen_sparse_vector import text_to_sparse_vector_english
from week5.milvus_op import select_by_vector, hybrid_search

load_dotenv(override=True)

MODEL = "gpt-4.1-nano"
DB_NAME = str(Path(__file__).parent.parent / "vector_db_pro_max")
api_key = os.getenv("EMBEDDING_API_KEY")
self_MODEL = "qwen3.5-plus-2026-02-15"

# embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

RETRIEVAL_K = 10

SYSTEM_PROMPT = """
You are a knowledgeable, friendly assistant representing the company Insurellm.
You are chatting with a user about Insurellm.
If relevant, use the given context to answer any question.
If you don't know the answer, say so.
Context:
{context}
"""

# vectorstore = Chroma(persist_directory=DB_NAME, embedding_function=embedding)
# retriever = milvus_vector_store.as_retriever()

llm = ChatOpenAI(
    temperature=0,
    model_name=self_MODEL,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=api_key,

)


def fetch_context(question: str) -> list[Document]:
    """
    Retrieve relevant context documents for a question.
    """
    dense_vector = text_embedding(question)
    sparse_vector = text_to_sparse_vector_english(question)

    return hybrid_search(dense_vector, sparse_vector, 10)


def combined_question(question: str, history: list[dict] = []) -> str:
    """
    Combine all the user's messages into a single string.
    """
    prior = "\n".join(m["content"] for m in history if m["role"] == "user")
    return prior + "\n" + question


def answer_question(question: str, history: list[dict] = []) -> tuple[str, list[Document]]:
    """
    Answer the given question with RAG; return the answer and the context documents.
    """
    combined = combined_question(question, history)
    docs = fetch_context(combined)
    context = "\n\n".join(doc["text"] for doc in docs)
    system_prompt = SYSTEM_PROMPT.format(context=context)
    messages = [SystemMessage(content=system_prompt)]
    messages.extend(convert_to_messages(history))
    messages.append(HumanMessage(content=question))
    response = llm.invoke(messages)
    return response.content, docs
