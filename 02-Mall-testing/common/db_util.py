# common/db_util.py
import pymysql

class DBUtil:
    def __init__(self, host, port, user, password, database):
        self.conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

    def query_one(self, sql, params=None):
        """查询单条数据"""
        with self.conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()

    def close(self):
        """关闭连接"""
        if self.conn:
            self.conn.close()
