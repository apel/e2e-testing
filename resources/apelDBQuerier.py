"""
Query the MySQL database for updates to the vsupersummaries table.
"""

from datetime import datetime, timezone
from dotenv import load_dotenv
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
    updateTime = row[0]
    earliestTime = row[15]
    latestTime = row[16]
    wallDuration = row[17]
    numJobs = row[19]
    print(updateTime, earliestTime, latestTime, wallDuration, numJobs)

cursor.close()
connection.close()
