from pymilvus import MilvusClient

db_name = "default"
collection_name = "vector_db"

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
