import os

from db_utils.config.config import Config
from db_utils.connect import connect
from db_utils.util.logger import logger


def table_exists(conn, table_name, schema="public"):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_schema = %s AND table_name = %s
            );
        """,
            (schema, table_name),
        )
        return cur.fetchone()[0]


def script_already_applied(conn, filename):
    with conn.cursor() as cur:
        cur.execute("SELECT 1 FROM applied_scripts WHERE filename = %s", (filename,))
        return cur.fetchone() is not None


def mark_script_applied(conn, filename):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO applied_scripts (filename) VALUES (%s)", (filename,))
        conn.commit()


def apply_sql_scripts(conn, config):
    try:
        if not table_exists(conn, "applied_scripts"):
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS applied_scripts (
                        id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                        filename TEXT UNIQUE NOT NULL,
                        applied_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                    );
                """
                )
                conn.commit()
                logger.info("Table 'applied_scripts' was verified or created.")

        files = sorted(f for f in os.listdir("./db_scripts/") if f.endswith(".sql"))

        for file in files:
            if script_already_applied(conn, file):
                logger.info(f"Script was applied: {file}")
                continue

            logger.info(f"Applied: {file}")
            with open(os.path.join("./db_scripts/", file), "r") as f:
                sql = f.read()

            with conn.cursor() as cur:
                cur.execute(sql)
                conn.commit()

            mark_script_applied(conn, file)
    except Exception as e:
        logger.error(e)
    finally:
        logger.info("Close db connection..")
        conn.close()


if __name__ == "__main__":
    logger.info("Open connection to db...")

    config = Config()
    conn = connect(config)

    apply_sql_scripts(conn, config)
