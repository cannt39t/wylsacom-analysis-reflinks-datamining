import csv
import psycopg2

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="vk_spider_info",
    user="postgres",
    password="postgres"
)

# Open a cursor and execute a SELECT statement to fetch data from the yt_videos table
with conn.cursor() as cur:
    cur.execute("SELECT * FROM yt_videos")

    # Open a new file called yt_videos.csv and write the rows from the query result to it
    with open("yt_videos.csv", "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter='\t')
        csv_writer.writerow([i[0] for i in cur.description])  # write header row
        for row in cur:
            csv_writer.writerow([str(cell).replace("\n", "\\n") for cell in row])

# Close the cursor and the connection
cur.close()
conn.close()
