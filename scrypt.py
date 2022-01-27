import subprocess
import re
import os
from pprint import pprint


os.chdir('/home/deadcrow2021/Рабочий стол/Union commit/geneva')

# path_to_file = '/home/deadcrow2021/Рабочий стол/Union commit/geneva/.git/rebase-merge/git-rebase-todo'
path_to_file = '/home/deadcrow2021/Рабочий стол/git scrypt/first.txt'
logs = '/home/deadcrow2021/Рабочий стол/Union commit/geneva/.git/logs/HEAD'

# Delete all comments in main file
file = open(path_to_file, 'r')
a = file.read()
commits = a.split('\n')
commits = [x for x in commits if '#' not in x]
commits = [x for x in commits if x != ''] # ['pick 4bedf4c init repo', 'pick 02160c9 user bitrix-env-adm change page /ru/consular-functions/pension/index.php on site /var/www/geneva',...

with open(path_to_file, 'w') as file:
    for i in commits:
        file.write(i + '\n')


leading_4_spaces = re.compile('^    ')

def get_commits():
    lines = subprocess.check_output(
        ['git', 'log', '--date=raw'], stderr=subprocess.STDOUT
    ).decode("utf-8").split('\n')
    log_commits = []
    current_commit = {}

    def save_current_commit():
        title = current_commit['message'][0]
        message = current_commit['message'][1:]
        if message and message[0] == '':
            del message[0]
        current_commit['title'] = title
        current_commit['message'] = '\n'.join(message)
        log_commits.append(current_commit)

    for line in lines:
        if not line.startswith(' '):
            if line.startswith('commit '):
                if current_commit:
                    save_current_commit()
                    current_commit = {}
                current_commit['hash'] = line.split('commit ')[1]
            else:
                try:
                    key, value = line.split(':', 1)
                    current_commit[key.lower()] = value.strip()
                except ValueError:
                    pass
        else:
            current_commit.setdefault(
                'message', []
            ).append(leading_4_spaces.sub('', line))
    if current_commit:
        save_current_commit()

    for i in log_commits:
        if i['title'].split(' ')[0] == 'user':
            user = ((i['title']).split(' '))[1]
            i['author'] = user
        date = int(i['date'][:i['date'].find('+')])
        i['date'] = date # or   date + 86400

    return log_commits

reversed_list_of_commits = get_commits()[::-1] # [{'hash': '4bedf4c7cddbc1130308e4657549170fb63d54b3', 'author': 'root <root@bitrix-env>', 'date': 1621842838, 'message': '', 'title': 'init repo'}, {'hash': '02160c9a3bc1aeccd6d2f8a6136060f48bd8a7d3', 'author': 'bitrix-env-adm', 'date': 1621845769, 'message': '', 'title': 'user bitrix-env-adm change page /ru/consular-functions/pension/index.php on site /var/www/geneva'},...

def get_page_from_one_commit(index):
    page = commits[index][commits[index].find('page'):].split(' ')[1]
    return page

# print(commits[:5])
# print(reversed_list_of_commits[:5])

for i in range(1, len(commits)): # init not included
    next_commit = 1

    if commits[i].split(' ')[0] == 'squash' or 'merged' in commits[i]:
        continue

    if i == len(commits)-1:
        break

    for j in range(i, len(commits)):
        if commits[i].split(' ')[1] in reversed_list_of_commits[i]['hash'] and \
           -(reversed_list_of_commits[i]['date'] - reversed_list_of_commits[i+next_commit]['date']) <= 86400 and \
           reversed_list_of_commits[i]['author'] == reversed_list_of_commits[i+next_commit]['author'] and \
           get_page_from_one_commit(i) == get_page_from_one_commit(i+next_commit):

            commits[i+next_commit] = commits[i+next_commit].replace('pick', 'squash')
            next_commit += 1
        else:
            break


with open('/home/deadcrow2021/Рабочий стол/git scrypt/result.txt', 'w') as file:
    for i in commits:
        file.write(i + '\n')
