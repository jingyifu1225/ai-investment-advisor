# test_mongodb.py
import certifi
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


def test_mongodb_connection():
    # 从环境变量获取MongoDB URI
    mongo_uri = os.getenv("MONGO_URI")
    print(f"正在测试连接MongoDB: {mongo_uri}")

    try:
        # 创建MongoDB客户端
        client = MongoClient(
            mongo_uri,
            serverSelectionTimeoutMS=10000,  # 10秒超时
            tlsCAFile=certifi.where()  # 添加SSL证书验证
        )

        # 测试连接
        result = client.admin.command('ping')
        print("MongoDB连接成功!")
        print(f"服务器响应: {result}")

        # 测试获取数据库和集合
        db_name = "ai_investment_db"  # 替换为你的数据库名称
        collection_name = "vector_search_collection_new"  # 替换为你的集合名称

        db = client[db_name]
        collections = db.list_collection_names()
        print(f"可用集合: {collections}")

        if collection_name in collections:
            collection = db[collection_name]
            print(f"集合'{collection_name}'存在")

            # 查看索引
            print("索引:")
            for index in collection.list_indexes():
                print(f"  - {index}")

            # 测试Atlas Search索引
            try:
                search_indexes = db.command({"listSearchIndexes": collection_name})
                print(f"搜索索引: {search_indexes}")
            except Exception as e:
                print(f"获取搜索索引失败: {e}")
        else:
            print(f"集合'{collection_name}'不存在")

        return True
    except Exception as e:
        print(f"MongoDB连接失败: {e}")
        return False


if __name__ == "__main__":
    test_mongodb_connection()