import logging
import time
import os
from dotenv import load_dotenv

load_dotenv()

import psycopg2

LOG = logging.getLogger(__name__)

con = None
while not con:
    try:
        con = psycopg2.connect(
            os.environ["DATABASE_URL"],
        )
    except Exception as e:
        LOG.error(e, exc_info=e)
        LOG.warning("Could not connect to database, retrying in 5 seconds...")
        time.sleep(5)
