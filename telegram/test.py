import psycopg2

# Connect to the database
conn = psycopg2.connect(
    host="localhost",
    database="vk_spider_info",
    user="postgres",
    password="postgres"
)

# Import data from CSV file
with conn.cursor() as cur:
    with open('/path/to/tg_posts.csv', 'r', encoding='utf-8') as f:
        cur.copy_from(f, 'tg_posts', sep=';', null='\\N', columns=('id', 'content', 'post_date', 'link', 'ref_links', 'whois_info'))
    conn.commit()
