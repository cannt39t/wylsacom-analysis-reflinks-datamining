import re

import requests
import requests.exceptions
from urllib.parse import urlparse, parse_qs

url = "https://clck.ru/33WEPH"

def getFinalUrl(url: str):
    try:
        response = requests.get(url)
        final_url = response.url

        response = requests.get(url, allow_redirects=False)

        if final_url == "https://away.vk.com/away.php":
            redirect_url = response.headers['Location']
            parsed_url = urlparse(redirect_url)
            query_params = parse_qs(parsed_url.query)
            to_url = query_params['to'][0]
            return to_url
        else:
            return final_url
    except BaseException:
        return ""

def get_links_from_text(text):
    res = ""

    pattern_l = r"\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"

    urls = re.findall(pattern_l, text, re.IGNORECASE)

    for link in urls:
        final_link = getFinalUrl(link)
        if ref_or_not(final_link):
            res = final_link
    return res


regex = r"\bhttps?://\S+\?(?:(?:amp;)?|\b)(?:ref|referrer|referral|promo|promocode|coupon|code|invite|invited_by|friend|source|partner|utm_\w+)=\S+\b"

def ref_or_not(link):
    if 'ref' in link:
        return True
    matches = re.findall(regex, link)
    if len(matches) != 0:
        return True
    return False



