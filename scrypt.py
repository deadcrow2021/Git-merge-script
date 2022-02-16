import subprocess
import re
import os


def get_commits():
    lines = subprocess.check_output(
        ['git', 'log', '--date=raw'],
        stderr=subprocess.STDOUT
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

    for commit in log_commits:
        if commit['title'].split(' ')[0] == 'user':
            user = ((commit['title']).split(' '))[1]
            commit['author'] = user
        date = int(commit['date'][:commit['date'].find('+')])
        commit['date'] = date # or   date + 86400

    return log_commits


def get_page_from_commit_by(index):
    page = commits[index][commits[index].find('page'):].split(' ')[1]
    return page


def get_date_diff(commits_list, index):
    commit_date = commits_list[index]['date'] - commits_list[index-1]['date']
    return commit_date


# change work directory for 'git log'
os.chdir('/home/deadcrow2021/Desktop/Union commit/geneva')

# path to work file
path_to_file = '/home/deadcrow2021/Desktop/Union commit/geneva/.git/rebase-merge/git-rebase-todo'

# Delete all comments in main file
file = open(path_to_file, 'r')
file_text = file.read()
commits = file_text.split('\n')
commits = [commit for commit in commits if '#' not in commit]
commits = [commit for commit in commits if commit != ''] # ['pick 4bedf4c init repo', 'pick 02160c9 user bitrix-env-adm change page /ru/consular-functions/pension/index.php on site /var/www/geneva',...

# fill file only with commits
with open(path_to_file, 'w') as file:
    for i in commits:
        file.write(i + '\n')


leading_4_spaces = re.compile('^    ')
reversed_list_of_commits = (get_commits()[::-1]) # [{'hash': '4bedf4c7cddbc1130308e4657549170fb63d54b3', 'author': 'root <root@bitrix-env>', 'date': 1621842838, 'message': '', 'title': 'init repo'}, {'hash': '02160c9a3bc1aeccd6d2f8a6136060f48bd8a7d3', 'author': 'bitrix-env-adm', 'date': 1621845769, 'message': '', 'title': 'user bitrix-env-adm change page /ru/consular-functions/pension/index.php on site /var/www/geneva'},...
reversed_list_of_commits = reversed_list_of_commits[len(reversed_list_of_commits)-len(commits):len(reversed_list_of_commits)]

for commit_index in range(1, len(commits)):
    next_commit_index = 1

    if commits[commit_index].split(' ')[0] == 'squash' or 'merged' in commits[commit_index]: # pass squashed commit
        continue

    if commit_index == len(commits)-1: # pass last commit
        break

    # Check if hash in work file and log file are the same,
    # check date, author, page name
    for commit in range(commit_index, len(commits)):
        if commits[commit_index].split(' ')[1] in reversed_list_of_commits[commit_index]['hash']:
            if get_date_diff(reversed_list_of_commits, commit_index + next_commit_index) <= 86400:
                if reversed_list_of_commits[commit_index]['author'] == reversed_list_of_commits[commit_index+next_commit_index]['author']:
                    if get_page_from_commit_by(commit_index) == get_page_from_commit_by(commit_index+next_commit_index):
                        commits[commit_index+next_commit_index] = commits[commit_index+next_commit_index].replace('pick', 'squash')
                        next_commit_index += 1
        else:
            break

with open(path_to_file, 'w') as file:
    for commit in commits:
        file.write(commit + '\n')
