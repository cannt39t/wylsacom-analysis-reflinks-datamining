import datetime
import vk_api
import whois
from urllib.parse import urlparse

from vk.database_work import add_data_to_database
from vk.get_ref_links import get_links_from_text

token = ""
group_id_root = 31038184

vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()

screen_name = (vk.groups.getById(group_id=group_id_root)[0]['screen_name'])

group_id_root = -group_id_root



def get_group_posts(group_id):
    all_posts = []
    all_comments = []
    offset = 0
    count = 100

    two_years_ago = datetime.datetime.now() - datetime.timedelta(days=365 * 2)
    start_time = int(two_years_ago.timestamp())

    while True:
        posts = vk.wall.get(owner_id=group_id, count=count, offset=offset, start_time=start_time)

        if len(posts['items']) == 0:
            break

        for post in posts['items']:
            date = datetime.datetime.fromtimestamp(post['date'])
            id = post['id']
            post_link = f'https://vk.com/{screen_name}?w=wall{group_id_root}_{id}'

            link = get_links_from_text(post['text'])
            if len(link) == 0:
                continue

            main_domain = urlparse(link).hostname
            main_domain = ".".join(main_domain.split(".")[-2:])

            # Retrieve the WHOIS information for the main domain
            w = whois.whois(main_domain)

            # Extract the company name from the WHOIS information
            company = w.get("org", main_domain)
            if company is None:
                company = main_domain

            post_data = {
                'post_id': post['id'],
                'text': post['text'],
                'likes': post['likes']['count'],
                'reposts': post['reposts']['count'],
                'views': post['views']['count'],
                'date': date,
                'link': post_link,
                'ref_links': link,
                'whois_info': company
            }

            all_posts.append(post_data)
            all_comments.append(get_comments_of_post(group_id_root, id))

        oldest_post_date = datetime.datetime.fromtimestamp(posts['items'][-1]['date'])
        if oldest_post_date < two_years_ago:
            break

        offset += count

    add_data_to_database(all_posts, all_comments)


def get_comments_of_post(group_id, post_id):
    res = []
    comments = vk.wall.getComments(owner_id=group_id, post_id=post_id, count=100, thread_items_count=10, need_likes=1,
                                   extended=1)

    all_comments = []

    all_comments.extend(comments['items'])

    print(all_comments)

    for c in comments['items']:
        date = datetime.datetime.fromtimestamp(c['date'])
        comment_data = {
            'comment_id': str(c['id']),
            'from_id': str(c['from_id']),
            'text': str(c['text']),
            'date': date,
            'likes': str(c['likes']['count']) if 'likes' in c else '0',
            'reposts': str(c['thread']['count']),
            'post_id': str(post_id)

        }
        # adding comment into bd
        res.append(comment_data)
    return res


if __name__ == '__main__':

    get_group_posts(group_id_root)
