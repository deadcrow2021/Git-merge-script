import subprocess
import datetime
import argparse
import time
import re
import os

arg_parser = argparse.ArgumentParser(description='Get number of commits.')
arg_parser.add_argument("-n", "--number", help="Get number of commits", default=0, type=int)
args = arg_parser.parse_args()

BASEDIR = os.path.dirname(os.path.realpath(__file__))
now = datetime.datetime.now()
seconds_since_midnight = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()

os.chdir(BASEDIR)
if args.number > 0:
    lines = subprocess.check_output(
        ['git', 'log', '--oneline', '-{}'.format(args.number)],
        stderr=subprocess.STDOUT
        ).decode("utf-8").split('\n')
else:
    lines = subprocess.check_output(
        ['git', 'log', '--oneline'],
        stderr=subprocess.STDOUT
        ).decode("utf-8").split('\n')


with open(os.path.join(BASEDIR, 'git_rebase_file'), 'w') as file:
    for commit in lines[::-1]:
        if commit == '':
            continue
        try:
            try:
                file.write('pick ' + commit + '\n')
            except:
                file.write('pick ' + commit)
        except:
            try:
                file.write('pick ' + commit.encode('utf-8') + '\n')
            except:
                file.write('pick ' + commit.encode('utf-8'))


def get_commits():
    log_commits = []
    current_commit = {}

    if args.number > 0:
        lines = subprocess.check_output(
            ['git', 'log', '--date=raw', '-{}'.format(args.number)],
            stderr=subprocess.STDOUT
            ).decode("utf-8").split('\n')
    else:
        lines = subprocess.check_output(
            ['git', 'log', '--date=raw'],
            stderr=subprocess.STDOUT
            ).decode("utf-8").split('\n')


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
        commit['date'] = date

    return log_commits


def get_page_from_commit_by(index):
    page = commits[index][commits[index].find('page'):].split(' ')[1]
    return page


def get_date_diff(commits_list, index):
    commit_date = commits_list[index]['date'] - commits_list[index-1]['date']
    return commit_date


# Delete all comments in main file
file = open(os.path.join(BASEDIR, 'git_rebase_file'), 'r')
file_text = file.read()
commits = file_text.split('\n')
commits = [commit for commit in commits if commit != '']

leading_4_spaces = re.compile('^    ')

# commits from git log
list_of_commits = get_commits()
reversed_list_of_commits = list_of_commits[::-1]

for commit_index in range(0, len(commits)):
    next_commit_index = 1

    if commits[commit_index].split(' ')[0] == 'fixup' in commits[commit_index]: # pass squashed commit
        continue

    if int(reversed_list_of_commits[commit_index]['date']) > (time.time() - seconds_since_midnight): # dont' check today's commits
        break

    if commit_index == len(commits)-1: # pass last commit
        break


    # Check if hash in work file and log file are the same,
    # check date, author, page name
    for commit in range(commit_index, len(commits)):
        if commits[commit_index].split(' ')[1] not in reversed_list_of_commits[commit_index]['hash']:
            break
        if get_date_diff(reversed_list_of_commits, commit_index + next_commit_index) > 86400:
            break
        if reversed_list_of_commits[commit_index]['author'] != reversed_list_of_commits[commit_index+next_commit_index]['author']:
            break
        if get_page_from_commit_by(commit_index) != get_page_from_commit_by(commit_index+next_commit_index):
            break

        if subprocess.check_output(['git', 'diff', '{}^..{}'.format(
                    reversed_list_of_commits[commit_index]['hash'],
                    reversed_list_of_commits[commit_index + next_commit_index]['hash'])]).decode('utf-8') == '':
            break
 
        commits[commit_index+next_commit_index] = commits[commit_index+next_commit_index].replace('pick', 'fixup')
        next_commit_index += 1

with open(os.path.join(BASEDIR, 'git_rebase_file'), 'w') as file:
    for commit in commits:
        file.write(commit + '\n')
