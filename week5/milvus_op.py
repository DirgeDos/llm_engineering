from pymilvus import MilvusClient, AnnSearchRequest, WeightedRanker

db_name = "default"
collection_name = "vector_db_pro_max_new_2048_cos_mix"

client = MilvusClient(
    uri="http://192.168.175.142:19530",
    db_name=db_name,
)


def get_all(fields=None):
    if fields is not None and not isinstance(fields, list):
        raise ValueError("参数错误！请传入字段列表，例如：['a']、['a', 'b']")

    all_results = []

    batch_size = 16384
    query_param = {
        "collection_name": collection_name,
        "filter": "",
        "batch_size": batch_size,
        "output_fields": fields if fields else ["*"]
    }

    iterator = client.query_iterator(**query_param)
    while True:
        res = iterator.next()

        if not res:
            iterator.close()
            break

        all_results.extend(res)

    return all_results


def insert(data: list[dict]):
    if not isinstance(data, list):
        raise TypeError("插入失败！data 必须是列表，格式：[{}, {}]")

    # 强制校验：列表里的每个元素必须是字典
    for item in data:
        if not isinstance(item, dict):
            raise TypeError("插入失败！列表内必须是字典，格式：[{...}, {...}]")
    client.insert(
        collection_name=collection_name,
        data=data
    )


def get_collection_fields():
    """
    获取当前集合的所有字段名（a、b、c、text、image等）
    :return: 字段名列表 → ['pk', 'vector', 'text', 'image']
    """
    collection_info = client.describe_collection(collection_name=collection_name)
    field_names = [field["name"] for field in collection_info["fields"]]
    return field_names


def select_by_vector(vector: list, limit: int = 3):
    if not isinstance(vector, list) or len(vector) == 0:
        raise TypeError("参数错误！必须传入非空向量列表")

    res = client.search(
        collection_name=collection_name,
        anns_field="vector",  # 【固定】你集合里存储向量的字段名
        data=[vector],  # 【必须二维列表】格式：[待检索向量]
        limit=limit,  # 返回几条最相似的数据
        search_params={"metric_type": "COSINE"},  # 相似度计算方式：IP内积
        output_fields=["text", "doc_type", "source"]  # 【关键】返回所有字段（text/doc_type/vector）
    )

    final_result = []
    for hit in res[0]:  # res[0] 是当前查询的结果集
        final_result.append({
            # "pk": hit["id"],  # 主键ID
            # "similarity": hit["distance"],  # 相似度分数（越高越相似）
            "text": hit["entity"]["text"],  # 文本内容
            "doc_type": hit["entity"]["doc_type"],  # 文档类型
            "source": hit["entity"]["source"]
        })

    return final_result


def hybrid_search(dense_vector: list, sparse_vector: dict, limit: int = 3):
    # 1. 构建稠密向量检索请求
    dense_req = AnnSearchRequest(
        data=[dense_vector],  # 查询向量（二维列表）
        anns_field="vector",  # 稠密向量字段名
        param={"metric_type": "COSINE"},  # 与集合定义一致
        limit=limit * 2  # 召回更多候选再融合
    )

    # 2. 构建稀疏向量检索请求
    sparse_req = AnnSearchRequest(
        data=[sparse_vector],  # 查询稀疏向量（字典格式）
        anns_field="sparse_vector",  # 稀疏向量字段名
        param={"metric_type": "IP"},  # 稀疏向量必须用 IP
        limit=limit * 2
    )

    # 3. 执行混合检索（使用 hybrid_search 方法）
    res = client.hybrid_search(
        collection_name=collection_name,  # 你的集合名称，可以定义为全局变量或参数传入
        reqs=[dense_req, sparse_req],  # 两个请求
        ranker=WeightedRanker(0.6, 0.4),  # 加权融合：稠密权重0.6，稀疏0.4
        limit=limit,  # 最终返回数量
        output_fields=["text", "doc_type", "source"]
    )

    # 4. 格式化结果（与你原来的纯ANN检索格式一致）
    final_result = []
    for hit in res[0]:  # res[0] 是第一个查询的结果集
        final_result.append({
            "text": hit["entity"]["text"],
            "doc_type": hit["entity"]["doc_type"],
            "source": hit["entity"]["source"]
        })
    return final_result