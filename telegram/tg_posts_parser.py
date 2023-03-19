import json
import re
import whois

from urllib.parse import urlparse

import final_link_resolver

utm_pattern = r'https?:\/\/\S+\?(?:(?:amp;)?|\b)(?:ref|referer|referal|promo|promocode|coupon|code|invite|invited_by|friend|source|partner|utm_\w+)=\S+'

data = open('wylsared.txt')


def get_all_links():
    links_list = []

    data_lines = data.readlines()
    for line in data_lines:
        json_map = json.loads(line)
        links = json_map["outlinks"]
        if links and json_map["content"] is not None:
            for link in links:
                links_list.append(link)

    return links_list


def get_all_domains(links_list):
    domains_list = []
    for link in links_list:
        domains_list.append(final_link_resolver.get_domain_of_ref(link))
    return domains_list


def get_post_link(line):
    json_map = json.loads(line)
    post_link = json_map["url"]
    return post_link


def get_post_date(line):
    json_map = json.loads(line)
    date = json_map["date"]
    return date


def get_post_text(line):
    json_map = json.loads(line)
    content = json_map["content"]
    return content


def get_all_post_links(line):
    links_list = []
    json_map = json.loads(line)
    links = json_map["outlinks"]
    for link in links:
        links_list.append(link)
    return links_list


def get_post_ref_links(line):
    links_list = []

    json_map = json.loads(line)
    links = json_map["outlinks"]
    if links and json_map["content"] is not None:
        for link in links:
            links_list.append(link)

    ref_links = []

    for link in links_list:
        if "utm_source=telegram&amp" not in link:
            matches = re.findall(utm_pattern, link)
            if len(matches) != 0:
                ref_links.append(matches)
    return ref_links


def get_host_owner(link):
    main_domain = urlparse(link).hostname
    main_domain = ".".join(main_domain.split(".")[-2:])
    w = whois.whois(main_domain)
    company = w.get("org", "")
    if company is None:
        company = main_domain
    if company == "":
        company = final_link_resolver.get_domain_of_ref(link)
    return company
