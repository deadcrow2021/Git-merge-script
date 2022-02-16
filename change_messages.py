import os

# change work directory for 'git log'
os.chdir('/home/deadcrow2021/Desktop/Union commit/geneva')

# path to work file
path_to_file = '/home/deadcrow2021/Desktop/Union commit/geneva/.git/COMMIT_EDITMSG'

# Delete all comments in main file

while True:
    file = open(path_to_file, 'r')
    file_text = file.read()
    messages = file_text.split('\n')
    messages = [message for message in messages if '#' not in message]
    messages = [message for message in messages if message != '']
    if not any("merged" in s for s in messages):
        meassage = ''
        try:
            message = messages[0] + ' - merged'
            with open(path_to_file, 'w') as file:
                file.write(message)
        except:
            pass