import asyncpg
from loguru import logger


class AppHistory:
    def __init__(
        self,
        dbname,
        user,
        pw,
        host,
        port=5601,
        pool_config={},
    ):
        self.DB_NAME = dbname
        self.TABLE_NAME_PREFIX = "brick_history"
        self.conn_str = f"postgres://{user}:{pw}@{host}:{port}/{dbname}"

    async def init(self, **pool_config):
        self.pool = await asyncpg.create_pool(dsn=self.conn_str, **pool_config)
        # await self._init_table()
        logger.info("App history Initialized")

    def get_table_name(self, domain_name):
        return f"{self.TABLE_NAME_PREFIX}_{domain_name}"

    async def init_table(self, domain_name):
        table_name = self.get_table_name(domain_name)
        qstrs = [
            """
            CREATE TABLE IF NOT EXISTS {table_name} (
                uuid TEXT NOT NULL,
                user_id TEXT NOT NULL,
                app_name TEXT NOT NULL,
                time TIMESTAMP NOT NULL,
                PRIMARY KEY (uuid, time)
            );
            """.format(
                table_name=table_name
            ),
            """
                CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;
            """,
            """
            SELECT create_hypertable('{table_name}', 'time');
            """.format(
                table_name=table_name
            ),
            """
            CREATE INDEX IF NOT EXISTS brick_history_time_index ON {table_name} (time DESC);
            """.format(
                table_name=table_name
            ),
            """
            CREATE INDEX IF NOT EXISTS brick_data_uuid_index ON {table_name} (uuid);
            """.format(
                table_name=table_name
            ),
        ]
        async with self.pool.acquire() as conn:
            for qstr in qstrs:
                try:
                    res = await conn.execute(qstr)
                except Exception as e:
                    if "already a hypertable" in str(e):
                        pass
                    else:
                        raise e
        logger.info("Init table {}", table_name)
