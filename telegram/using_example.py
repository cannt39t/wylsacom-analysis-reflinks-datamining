import tg_posts_parser as parser
import subprocess

# You can put any other telegram channel name instead of 'wylsared', also you can choose
# any file name you want, choose period of time
cmd = '''snscrape --jsonl --since 2022-01-01 telegram-channel wylsared > wylsared.txt'''
args_list = cmd.split(" ")
process = subprocess.run(args_list, shell=True)

# Example of getting all links from all the posts you have chosen to parse
links = parser.get_all_links()
print(links)

# Example of getting all domains of the links
domains = parser.get_all_domains(links)
print(domains)

# For using other functions you need to load your file line by line
data = open('wylsared.txt')
data_lines = data.readlines()

# Simple example of using parser
for line in data_lines:
    print(parser.get_post_link(line))
    print(parser.get_post_ref_links(line))
    print(parser.get_post_text(line))
    print(parser.get_post_date(line))

    # This one is working slowly because it uses external web-service
    print(parser.get_host_owner(line))







