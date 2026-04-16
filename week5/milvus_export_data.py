from pymilvus import MilvusClient
import json
import os

# ===================== 源 Milvus 配置（你当前的机器）=====================
SOURCE_URI = "http://192.168.175.142:19530"
SOURCE_DB = "default"
# 要导出的集合列表
COLLECTIONS = ["vector_db_pro_max"]
# 分页大小（避免单次查询数据太多）
BATCH_SIZE = 1000

# ===================== 执行导出 =====================
# 连接源 Milvus
client = MilvusClient(uri=SOURCE_URI, db_name=SOURCE_DB)
print("✅ 已连接源 Milvus")

for coll_name in COLLECTIONS:
    print(f"\n🔄 开始导出集合: {coll_name}")

    # 1. 加载集合到内存（查询必须加载）
    client.load_collection(collection_name=coll_name)
    print(f"✅ 集合 {coll_name} 已加载")

    # 2. 获取集合总条数
    total_count = client.get_collection_stats(coll_name)["row_count"]
    print(f"📊 集合总条数: {total_count}")

    # 3. 分页查询所有数据（输出所有字段）
    all_data = []
    for offset in range(0, total_count, BATCH_SIZE):
        res = client.query(
            collection_name=coll_name,
            filter="",  # 空 filter 表示查询所有数据
            offset=offset,
            limit=BATCH_SIZE,
            output_fields=["*"]  # 输出所有字段（含 vector、text、source、doc_type 等）
        )
        all_data.extend(res)
        print(f"📥 已查询 {len(all_data)}/{total_count} 条")

    # 4. 释放集合内存
    client.release_collection(collection_name=coll_name)
    print(f"✅ 集合 {coll_name} 已释放内存")

    # 5. 导出为 JSON 文件
    output_file = f"{coll_name}_export.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

    print(f"🎉 集合 {coll_name} 导出完成！文件: {output_file}，总条数: {len(all_data)}")

print("\n✅ 所有集合导出完成！")