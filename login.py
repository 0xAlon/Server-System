import logging
import db_config
import pymysql
import sys
import secrets
from passlib.hash import pbkdf2_sha256

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


def handler(user, secret):
    with conn.cursor() as cur:
        cur.execute("select * from Users WHERE user = %s", user)
        conn.commit()
        if cur.rowcount == 1:
            for row in cur:
                if pbkdf2_sha256.verify(secret, row[3]):
                    token = secrets.token_hex(16)
                    try:
                        cur.execute('UPDATE Users set token = %s where id = %s', (token, row[0]))
                        conn.commit()
                    except Exception as exception:
                        logging.warning("ERROR: Unexpected error: Could not Update MySql instance. %s ", exception)
                    finally:
                        cur.close()
                        return token
                else:
                    return None
        else:
            return None


if __name__ == '__main__':
    print(handler("alon", "123456"))
