import pymysql
from dbutils.pooled_db import PooledDB
from pymysql import Error

# ===================== 【1】MySQL 基础配置 =====================
MYSQL_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "123456",
    "database": "prices-dev",
    "charset": "utf8mb4",
    # 连接池固定参数（不用改）
    "cursorclass": pymysql.cursors.DictCursor  # 可选：返回字典格式数据
}

# ===================== 【2】创建全局连接池 =====================
# 整个程序只创建一次连接池（核心！）
POOL = PooledDB(
    creator=pymysql,        # 使用pymysql作为连接驱动
    maxconnections=10,      # 连接池最大连接数
    mincached=2,            # 初始化时最少空闲连接
    maxcached=5,            # 池中最大空闲连接
    maxshared=3,            # 最大共享连接数
    blocking=True,          # 无连接时等待，不报错
    **MYSQL_CONFIG          # 加载数据库配置
)

# ===================== 【3】使用连接池操作数据库 =====================
def init_table():
    """初始化数据表（使用连接池）"""
    try:
        # 从连接池获取连接（with 自动归还连接，不用手动关闭！）
        with POOL.connection() as conn:
            # 游标：执行SQL的工具（和你之前用法完全一样）
            with conn.cursor() as cursor:
                # 创建表
                sql = """
                    CREATE TABLE IF NOT EXISTS prices (
                        city VARCHAR(100) PRIMARY KEY, 
                        price DOUBLE
                    )
                """
                cursor.execute(sql)
                conn.commit()
                print("✅ 表创建成功（连接池版）")

    except Error as e:
        print(f"❌ 数据库错误：{e}")

# 执行初始化
if __name__ == '__main__':
    init_table()