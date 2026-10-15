"""
Query the Apel EGI grid MySQL database for updates to the vsupersummaries table.
Write the query result into a log file that can be parsed by filebeat and sent to OpenSearch.
"""

from datetime import datetime, timezone
import json
import os

from dotenv import load_dotenv
import mysql.connector

load_dotenv()

connection = mysql.connector.connect(
    host=os.getenv("dbHost"),
    user=os.getenv("dbUser"),
    password=os.getenv("dbPassword"),
    database=os.getenv("dbDatabase")
)

month = datetime.now(timezone.utc).month

query = """
    SELECT *
    FROM vsupersummaries
    WHERE GlobalUserName like "%rowan moss%"
    AND Month = %s
"""

cursor = connection.cursor()

cursor.execute(query, (month,))

for row in cursor.fetchall():
    # Each query result row is a tuple, made up of both useful and not useful information.
    # Store only the row's useful information in a dictionary.
    # This consists of when the data was last aggregated, the time of the last job,
    # the wall duration, and the number of jobs.
    output = {
        "updateTime": str(row[0]),
        "lastJobTime": str(row[16]),
        "wallDuration": row[17],
        "numberOfJobs": row[19]
    }

    # Append the output dictionary to the db query results log.
    # This log then gets parsed by filebeat and sent to OpenSearch.
    # jsonl is used over json so that the Filebeat parser for OpenSearch can consider each line
    # of the log file as a different log entry, removing the need for multi-line parsing.
    with open("/var/log/fed-services-e2e/apel_db_query_results_log.jsonl", "a") as f:
        json.dump(output, f)
        f.write("\n")

cursor.close()
connection.close()
