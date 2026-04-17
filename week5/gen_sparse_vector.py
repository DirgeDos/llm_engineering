import pickle

import jieba
from pymilvus.model.sparse.bm25.tokenizers import build_default_analyzer
from pymilvus.model.sparse import BM25EmbeddingFunction

with open("bm25_encoder_new.pkl", "rb") as f:
    bm25_ef = pickle.load(f)

def text_to_sparse_vector_chinese(text: str):
    """
    中文文本 → Milvus 稀疏向量
    作用：做关键词检索（替代BM25，数据库原生支持）
    """
    # 中文分词
    words = list(jieba.cut(text))
    # 词频统计
    word_count = {}
    for w in words:
        if len(w.strip()) > 0:
            word_count[w] = word_count.get(w, 0) + 1

    # 转成稀疏向量格式（Milvus要求：{索引: 权重}）
    sparse_dict = {}
    for idx, (word, cnt) in enumerate(word_count.items()):
        sparse_dict[idx] = float(cnt)

    return sparse_dict


def text_to_sparse_vector_english(text: str):


    one_encode_data_list = bm25_ef.encode_documents([text])
    one_sp_v = one_encode_data_list[0]  # 这是一个 coo_array

    return {int(i): float(v) for i, v in zip(one_sp_v.col, one_sp_v.data)}
