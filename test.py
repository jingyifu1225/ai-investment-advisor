from pymongo import MongoClient
import os
import certifi
from dotenv import load_dotenv
import json

# 加载环境变量
load_dotenv()
mongo_uri = os.getenv("MONGO_URI")

print(f"尝试连接到MongoDB: {mongo_uri}")

try:
    # 设置超时时间并指定证书路径
    client = MongoClient(mongo_uri,
                      serverSelectionTimeoutMS=5000,
                      tlsCAFile=certifi.where())
    # 测试连接
    client.admin.command('ping')
    print("MongoDB连接成功!")

    # 检查数据库和集合
    db_name = "ai_investment_db"
    collection_name = "vector_search_collection_new"

    print(f"\n检查数据库 {db_name} 中的集合:")
    db = client[db_name]
    collections = db.list_collection_names()
    print(collections)

    if collection_name in collections:
        collection = db[collection_name]
        print(f"\n集合 {collection_name} 存在")

        # 列出常规索引
        print(f"\n集合 {collection_name} 的常规索引:")
        for index in collection.list_indexes():
            print(index)

        # 尝试获取Atlas Search索引
        print(f"\n尝试获取Atlas Search索引:")
        try:
            search_indexes = db.command({"listSearchIndexes": collection_name})
            print(json.dumps(search_indexes, indent=2))
        except Exception as e:
            print(f"获取Search索引失败: {e}")
    else:
        print(f"\n集合 {collection_name} 不存在")

except Exception as e:
    print(f"MongoDB操作失败: {e}")