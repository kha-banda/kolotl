from mysql.connector import pooling
import config

_pool = None

def init_pool():
    global _pool
    if _pool is None:
        _pool = pooling.MySQLConnectionPool(
            pool_name=config.DB_POOL_NAME,
            pool_size=config.DB_POOL_SIZE,
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME
        )
    return _pool

def get_connection():
    if _pool is None:
        init_pool()
    return _pool.get_connection()
