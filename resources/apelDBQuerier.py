"""
Query the Apel EGI grid MySQL database for updates to the vsupersummaries table.
Write the query result into a log file that can be parsed by filebeat and sent to OpenSearch.
"""

from datetime import datetime, timezone
from dotenv import load_dotenv
import json
import mysql.connector
import os

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
WHERE GlobalUserName like "%rowan%"
  AND Month = %s
"""

cursor = connection.cursor()

cursor.execute(query, (month,))

for row in cursor.fetchall():
    # Store important parts of the query return in a dictionary.
    # So when the data was last aggregated, time of the last job, wall duration, and number of jobs.
    output = {
        "updateTime": str(row[0]),
        "lastJobTime": str(row[16]),
        "wallDuration": row[17],
        "numberOfJobs": row[19]
    }

    # Append the output dictionary to the db query results log.
    # This log then gets parsed by filebeat and sent to OpenSearch.
    with open("/var/log/fed-services-e2e/apel_db_query_results_log.jsonl", "a") as f:
        json.dump(output, f)
        f.write("\n")

cursor.close()
connection.close()
