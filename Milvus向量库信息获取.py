# -*- coding: utf-8 -*-
# -------------------------------
# @项目：dify
# @文件：test.py
# @时间：2024/12/2 19:22
# @作者：xming
# -------------------------------
import traceback

from pymilvus import (
  connections,
  Collection,
  CollectionSchema,
  FieldSchema,
  DataType,
  MilvusException
)


def test_milvus_connection():
  try:
    # 连接到 Milvus
    connections.connect(
        host='10.110.1.13',  # 替换为你的 Milvus 主机
        port='19530',  # 替换为你的 Milvus 端口
        user='root',  # 替换为你的用户名
        password='Milvus'  # 替换为你的密码
    )
    print("Milvus 连接成功!")

    # 列出所有集合
    from pymilvus import utility
    collections = utility.list_collections()
    print("现有集合:", collections)

    # 测试特定集合
    # collection_name = 'Vector_index_da0c79af_1580_4f41_af5d_7b923c4e8195_Node'
    collection_name = 'Vector_index_08790e29_a40b_46e2_be1b_24cb80bde58f_Node'

    try:
      # 尝试获取集合
      collection = Collection(collection_name)

      # 检查集合是否存在
      print(f"集合 {collection_name} 是否存在: {collection.name}")

      # 检查集合是否已加载
      print(f"集合 {collection_name} 是否已加载: {collection.name}")

      # 如果未加载，尝试加载
      if not collection.is_empty:
        collection.load()
        print(f"集合 {collection_name} 已加载")

      # 获取集合信息
      print("集合详细信息:")
      print(collection.schema)

    except MilvusException as collection_error:
      print(f"处理集合时出错: {collection_error}")
      traceback.print_exc()

  except Exception as e:
    print(f"发生错误: {e}")
    traceback.print_exc()
  finally:
    # 关闭连接
    connections.disconnect("default")


def create_test_collection():
  try:
    connections.connect(
        host='10.120.0.7',
        port='19530',
        user='root',
        password='Milvus'
    )

    # 定义字段
    fields = [
      FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
      FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=128)
    ]

    # 创建模式
    schema = CollectionSchema(fields, "Test collection")

    # 创建集合
    collection_name = "test_collection"
    collection = Collection(collection_name, schema)

    print(f"测试集合 {collection_name} 创建成功!")

  except Exception as e:
    print(f"创建测试集合时出错: {e}")
    traceback.print_exc()
  finally:
    connections.disconnect("default")


# 运行测试
if __name__ == "__main__":
  # 测试连接和现有集合
  test_milvus_connection()

  # 可选：创建测试集合
  # create_test_collection()