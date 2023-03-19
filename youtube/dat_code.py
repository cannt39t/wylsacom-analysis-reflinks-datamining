import psycopg2
import csv

# Connect to the database
conn = psycopg2.connect(
    host="localhost",
    database="yt_spider_info",
    user="postgres",
    password="postgres"
)

# Export data from vk_posts table
with conn.cursor() as cur:
    with open('yt_posts.csv', 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(('video_id', 'description', 'date', 'link', 'views', 'likes', 'duration', 'comments_number', 'ref_links', 'whois_info'))
        cur.copy_to(f, 'yt_videos_ref', sep=';')

# Close the connection
conn.close()