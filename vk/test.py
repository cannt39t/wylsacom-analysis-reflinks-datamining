import psycopg2
import csv

# Connect to the database
conn = psycopg2.connect(
    host="localhost",
    database="vk_spider_info",
    user="postgres",
    password="postgres"
)

# Export data from vk_posts table
with conn.cursor() as cur:
    with open('vk_posts.csv', 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(('post_id', 'text', 'likes', 'reposts', 'views', 'date', 'link', 'ref_links', 'whois_info'))
        cur.copy_to(f, 'vk_posts', sep=';')

with conn.cursor() as cur:
    with open('vk_comments.csv', 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(('comment_id', 'from_id', 'text', 'date', 'likes', 'reposts', 'post_id'))
        cur.copy_to(f, 'vk_comments', sep=';')

# Close the connection
conn.close()
