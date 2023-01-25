import logging
import time

import psycopg2

LOG = logging.getLogger(__name__)

con = None
while not con:
    try:
        con = psycopg2.connect(
            "dbname=postgres user=postgres password=postgres host=postgres"
        )
    except:
        LOG.warning("Could not connect to database, retrying in 5 seconds...")
        time.sleep(5)
