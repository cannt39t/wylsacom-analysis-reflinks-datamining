import psycopg2
import csv

def create_csv():
    # Connect to the database
    conn = psycopg2.connect(
        host="localhost",
        database="data_mining",
        user="postgres",
        password="qwerty007"
    )

    # Export data from table
    with conn.cursor() as cur:
        with open('tg_posts.csv', 'w', newline='', encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(('id', 'content', 'post_date', 'link', 'ref_links', 'whois_info'))
            cur.copy_to(f, 'tg_posts', sep=';')
