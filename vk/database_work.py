import psycopg2

def create_tables():

    conn = psycopg2.connect(
        host="localhost",
        database="vk_spider_info",
        user="postgres",
        password="postgres"
    )

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vk_posts (
                post_id TEXT PRIMARY KEY,
                text TEXT,
                likes INTEGER,
                reposts INTEGER,
                views INTEGER,
                date DATE,
                link TEXT,
                ref_links TEXT,
                whois_info TEXT
            )
        """)
        conn.commit()

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vk_comments (
                comment_id TEXT PRIMARY KEY,
                from_id TEXT,
                text TEXT,
                date DATE,
                likes INTEGER,
                reposts INTEGER,
                post_id TEXT REFERENCES vk_posts(post_id)
            )
        """)
        conn.commit()

    conn.close()


def add_data_to_database(posts, comments):
    conn = psycopg2.connect(
        host="localhost",
        database="vk_spider_info",
        user="postgres",
        password="postgres"
    )

    cur = conn.cursor()

    # Add posts to the database
    for post in posts:
        cur.execute("""
            INSERT INTO vk_posts (post_id, text, likes, reposts, views, date, link, ref_links, whois_info)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (post['post_id'], post['text'], post['likes'], post['reposts'], post['views'], post['date'],
              post['link'], post['ref_links'], post['whois_info']))

    # Add comments to the database
    for comment_list in comments:
        for comment in comment_list:
            cur.execute("""
                INSERT INTO vk_comments (comment_id, from_id, text, date, likes, reposts, post_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (int(comment['comment_id']), int(comment['from_id']), comment['text'], comment['date'],
                  int(comment['likes']), int(comment['reposts']), int(comment['post_id'])))

    conn.commit()
    cur.close()
    conn.close()



if __name__ == '__main__':
    create_tables()
