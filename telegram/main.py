import subprocess
import csv_executor
import database_executor

print('Input a channel name, for example : @durov, - its name "durov"')
channel_name = input()
print('Input a .txt source file name where you will store parsed posts info')
source_file = input()

cmd = 'snscrape --jsonl --since 2022-01-01 telegram-channel %s > %s' % (channel_name, source_file)
args_list = cmd.split(" ")
process = subprocess.run(args_list, shell=True)

csv_executor.create_csv()

# firstly you need to configure your database in file database_executor.py
database_executor.fill_data_base(source_file)



