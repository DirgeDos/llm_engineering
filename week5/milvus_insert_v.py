import os
import glob
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_milvus import Milvus
from langchain_text_splitters import RecursiveCharacterTextSplitter

from week5.embedding import dash_scope_embedding

if __name__ == '__main__':
    # MODEL = "gpt-4.1-nano"
    db_name = "vector_db"
    # openai_api_key = os.getenv('OPENAI_API_KEY')
    # api_key = os.getenv('EMBEDDING_API_KEY')
    #
    folders = glob.glob("knowledge-base/company")

    documents = []
    for folder in folders:
        doc_type = os.path.basename(folder)
        loader = DirectoryLoader(folder, glob="**/*.md", loader_cls=TextLoader, loader_kwargs={'encoding': 'utf-8'})
        folder_docs = loader.load()
        for doc in folder_docs:
            doc.metadata["doc_type"] = doc_type
            documents.append(doc)

    # print(f"Loaded {len(documents)} documents")
    #
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    #
    # print(f"Divided into {len(chunks)} chunks")
    # print(f"First chunk:\n\n{chunks[0]}")
    #
    #
    chunk = chunks[2:4]

    from langchain_core.documents import Document

    MILVUS_HOST = "192.168.175.142"
    MILVUS_PORT = 19530

    print("开始")

    db = Milvus.from_documents(
        # 测试数据
        documents=chunk,
        embedding=dash_scope_embedding,
        collection_name=db_name,
        connection_args={"uri": "http://192.168.175.142:19530"},
        auto_id=True
    )


    # vector_store_saved = Milvus.from_documents(
    #     chunk,
    #     embeddings,
    #     collection_name=db_name,
    #     connection_args={
    #         "host": "192.168.175.142",
    #         "port": "19530"
    #     },
    # )
