import re
import requests
import urllib.parse
import whois


def getFinalUrl(url: str):
    try:
        response = requests.get(url, timeout=10)
        final_url = response.url
        return final_url
    except requests.exceptions.Timeout:
        print(f"Timeout occurred while connecting to {url}")
        return ""
    except Exception as e:
        print(f"An error occurred while connecting to {url}: {e}")
        return ""


pattern = r'\b(http[s]?:\/\/\S+\.\S+\/\S*\?(ref|utm_source)=\S+)\b'


def get_links_from_text(text):
    res = ""

    pattern_l = r"\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"

    urls = re.findall(pattern_l, text, re.IGNORECASE)

    set_urls = set(urls)
    set_owns = {'https://t.me/Wylsared', 'com.wylsacom.media', 'http://twitter.com/wylsacom',
                'https://zen.yandex.ru/wylsacom', 'https://vk.com/wylsacom', 'http://wylsa.com'}
    urls = set_urls.difference(set_owns)

    for link in urls:
        if 'instagram' in link:
            return res
        final_link = getFinalUrl(link)
        if ref_or_not(final_link):
            res = final_link
    return res


def define_sponsor(link):
    main_domain = urllib.parse.urlparse(link).hostname
    main_domain = ".".join(main_domain.split(".")[-2:])
    w = whois.whois(main_domain)
    company = w.get("org", main_domain)
    if company == None:
        company = main_domain
    return company


def ref_or_not(link):
    regex = r"\bhttps?://\S+\?(?:(?:amp;)?|\b)(?:ref|referrer|referral|promo|promocode|coupon|code|invite|invited_by|friend|source|partner|utm_\w+)=\S+\b"
    if 'ref' in link:
        return True
    matches = re.findall(regex, link)
    if len(matches) != 0:
        return True
    return False