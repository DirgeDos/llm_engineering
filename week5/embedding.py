import json
import os

import dashscope
from langchain_community.embeddings import DashScopeEmbeddings
from openai import OpenAI

embedding_api_key = os.getenv("EMBEDDING_API_KEY")

input_text = "操作用户:admin"

embedding_client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=embedding_api_key,
    # 以下是北京地域base-url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

dash_scope_embedding = DashScopeEmbeddings(
    model="text-embedding-v3",
    dashscope_api_key=embedding_api_key,

)


def text_embedding(text):
    resp = dashscope.TextEmbedding.call(
        model="text-embedding-v3",
        input=text,
        api_key=embedding_api_key,
    )
    if resp.status_code != 200:
        raise Exception(f"向量生成失败：{resp.message}")

    embedding_vector = resp.output["embeddings"][0]["embedding"]
    return embedding_vector


# completion = embedding_client.embeddings.create(
#     model="text-embedding-v3",
#     input=input_text
# )
# print(completion.model_dump_json())
