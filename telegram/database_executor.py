# driver for postgres
import psycopg2
import tg_posts_parser as parser


def fill_data_base(source_file):
    # enter your database parameters
    con = psycopg2.connect(
        host="localhost",
        database="vk_spider_info",
        user="postgres",
        password="postgres"
    )

    cur = con.cursor()

    cur.execute("drop table if exists tg_posts;")

    cur.execute('''create table tg_posts( id SERIAL PRIMARY KEY,
        content TEXT,
        post_date TEXT,
        link TEXT,
        ref_links TEXT,
        whois_info TEXT
    );
    ''')

    data = open(source_file)

    data_lines = data.readlines()
    for line in data_lines:
        content = parser.get_post_text(line)
        post_date = parser.get_post_date(line)
        link = parser.get_post_link(line)
        ref_links = parser.get_post_ref_links(line)
        post_links = parser.get_all_post_links(line)
        host_owner = ""

        for post_link in post_links:
            host_owner = parser.get_host_owner(post_link)
        if len(ref_links) != 0:
            cur.execute('''
            INSERT INTO tg_posts (content, post_date, link, ref_links, whois_info) values (%s, %s, %s, %s, %s)
            ''', (content, post_date, link, ref_links, host_owner))

    con.commit()
    con.close()


if __name__ == '__main__':
    fill_data_base('wylsared.txt')
