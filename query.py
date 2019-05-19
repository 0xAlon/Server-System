import logging
import db_config
import pymysql
import sys

# logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s', datefmt='%d-%m-%y %H:%M:%S')

# db settings
host = db_config.db_host
name = db_config.db_username
password = db_config.db_password
db_name = db_config.db_name

try:
    conn = pymysql.connect(host=host, user=name, passwd=password, db=db_name, connect_timeout=5)
except:
    logging.error("ERROR: Unexpected error: Could not connect to MySql instance.")
    sys.exit()

logging.info("SUCCESS: Connection to MySql instance succeeded")


def handler(token):
    with conn.cursor() as cur:
        cur.execute("select * from Users WHERE token = %s", token)
        conn.commit()
        if cur.rowcount == 0:
            return None
        else:
            for row in cur:
                print(cur)
            return True

if __name__ == '__main__':
    print(handler("bcf7e94367645c74ccfd451b66cb1eed"))
