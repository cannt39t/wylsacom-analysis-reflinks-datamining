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
            CREATE TABLE yt_videos (
                video_id TEXT PRIMARY KEY,
                description TEXT,
                date DATE,
                link TEXT,
                views INTEGER,
                likes INTEGER,
                duration TEXT,
                comments_number INTEGER,
                ref_link TEXT,
                whois_info TEXT
            )
        """)
        conn.commit()
    conn.close()


def add_data_to_database(video):
    conn = psycopg2.connect(
        host="localhost",
        database="vk_spider_info",
        user="postgres",
        password="postgres"
    )

    cur = conn.cursor()

    cur.execute("""
        INSERT INTO yt_videos(video_id, description, date, link, views, likes, duration, comments_number, ref_link, whois_info)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (video['video_id'], video['description'], video['date'], video['link'], video['views'], video['likes'],
          video['duration'], video['comments_number'], video['ref_link'], video['whois_info']))



    conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':

    create_tables()
