import requests
from telegram import ParseMode, Update
import telegram
from git_config import repo_name, repo_owner, git_token
import base64
from help import MAX_MESSAGE_LENGTH


# Get the last or latest gitlog information
def gitlog(update, context):
    user_id = update.message.from_user.id
    if not check_repo_info(user_id):
        update.message.reply_text('Please set the repository owner, name, and GitHub token first.')
        return

    # Get the list of branches
    url = f'https://api.github.com/repos/{repo_owner[update.message.from_user.id]}/{repo_name[update.message.from_user.id]}/branches'
    headers = {'Authorization': f'token {git_token[update.message.from_user.id]}'}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        update.message.reply_text('An error occurred while fetching the list of branches.')
        return

    data = response.json()
    branches = [branch['name'] for branch in data]

    # Parse the branch name and number of commits from the message
    message = update.message.text.split()

    if len(message) < 2:
        update.message.reply_text('Please specify the branch name.')
        return

    branch_name = message[1]

    if branch_name not in branches:
        update.message.reply_text(f'Invalid branch name. Please choose from the available branches: {", ".join(branches)}.')
        return

    if len(message) > 2:
        try:
            num_commits = int(message[2])
            if num_commits <= 0:
                raise ValueError()
        except ValueError:
            update.message.reply_text('Invalid number of commits specified. Please provide a positive integer value.')
            return
    else:
        num_commits = 1

    # Get the commit log for the specified branch
    url = f'https://api.github.com/repos/{repo_owner[update.message.from_user.id]}/{repo_name[update.message.from_user.id]}/commits?sha={branch_name}'
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        update.message.reply_text(f'An error occurred while fetching the git log for branch "{branch_name}".')
        return

    data = response.json()

    if not data:
        update.message.reply_text(f'No commits found for branch "{branch_name}".')
        return

    commits = data[:num_commits]
    message = ''

    for commit in commits:
        author = commit['commit']['author']['name']
        hash = commit['sha']
        commit_date = commit['commit']['author']['date'].split('T')[0]  # Extract the date part
        commit_message = commit['commit']['message']
        message += f"\n<b>Author:</b> {author}\n<b>Hash:</b> {hash}\n<b>Date:</b> {commit_date}\n<b>Message:</b> {commit_message}\n\n"

    update.message.reply_text(message, parse_mode='HTML', reply_markup=telegram.ReplyKeyboardRemove())

# Prints a file from the repo directly on Telegram
def file_handler(update: Update, context):
    user_id = update.message.from_user.id
    if not check_repo_info(user_id):
        update.message.reply_text('Please set the repository owner, name, and GitHub token first.')
        return

    # Retrieve the selected branch from the user's context
    branch_name = context.user_data.get('branch', 'main')

    # Parse the file path from the message
    message = update.message.text.split()

    if len(message) < 2:
        update.message.reply_text('Please provide the file path along with the command.\n\n'
                                  'Example: /file path/to/file.txt')
        return

    # Join all the elements of the message after the command ("/file") into the file path
    file_path = ' '.join(message[1:])

    # Enclose the file path in double quotes to handle spaces
    file_path = f'"{file_path}"'

    # Fetch the file content from the GitHub repository
    url = f'https://api.github.com/repos/{repo_owner[update.message.from_user.id]}/{repo_name[update.message.from_user.id]}/contents/{file_path}?ref={branch_name}'
    headers = {'Authorization': f'token {git_token[update.message.from_user.id]}'}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        update.message.reply_text('An error occurred while fetching the file from the repository.')
        return

    data = response.json()

    if 'content' not in data:
        update.message.reply_text('File not found.')
        return

    file_content = base64.b64decode(data['content']).decode('utf-8')

    # Split the file content into chunks
    message_chunks = [file_content[i:i + MAX_MESSAGE_LENGTH] for i in
                      range(0, len(file_content), MAX_MESSAGE_LENGTH)]

    # Send each message chunk as a separate message
    for chunk in message_chunks:
        formatted_content = f"```\n{chunk}\n```"  # Add backticks around the content
        update.message.reply_text(formatted_content, parse_mode='Markdown')



# Show all available branches in the repository.
def branches(update: Update, context):
    user_id = update.message.from_user.id
    if not check_repo_info(user_id):
        update.message.reply_text('Please set the repository owner, name, and GitHub token first.')
        return
    # Fetch the list of branches
    url = f'https://api.github.com/repos/{repo_owner[update.message.from_user.id]}/{repo_name[update.message.from_user.id]}/branches'
    headers = {'Authorization': f'token {git_token[update.message.from_user.id]}'}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        update.message.reply_text('An error occurred while fetching the branches.')
        return

    data = response.json()
    branch_names = [branch['name'] for branch in data]

    if not branch_names:
        update.message.reply_text('No branches found in the repository.')
        return

    message = 'Available branches:\n\n' + '\n'.join(branch_names)
    update.message.reply_text(message)

# Show a list of the folders
def ls(update: Update, context):
    user_id = update.message.from_user.id
    if not check_repo_info(user_id):
        update.message.reply_text('Please set the repository owner, name, and GitHub token first.')
        return

    # Retrieve the selected branch from the user's context
    branch_name = context.user_data.get('branch', 'main')

    # Parse the folder path from the message
    message = update.message.text.split()
    folder_path = ""
    if len(message) > 1:
    # Join the parts inside quotes and remove the quotes
        folder_path = " ".join(part.strip('"') for part in message[1:])

    # Fetch the contents of the folder from the GitHub repository
    url = f'https://api.github.com/repos/{repo_owner[update.message.from_user.id]}/{repo_name[update.message.from_user.id]}/contents/{folder_path}?ref={branch_name}'
    headers = {'Authorization': f'token {git_token[update.message.from_user.id]}'}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        update.message.reply_text('An error occurred while fetching the folder contents.')
        return

    data = response.json()
    files = [
        file['name']
        for file in data
        if file['type'] == 'file' and not (file['name'].endswith('.meta') or file['name'].endswith('.asset'))
    ]
    folders = [folder['name'] for folder in data if folder['type'] == 'dir']

    if not files and not folders:
        update.message.reply_text('No files or folders found in the specified folder.')
        return

    file_message = "Files:\n\n" + "\n".join(files) if files else "No files found in the folder."
    folder_message = "Folders:\n\n" + "\n".join(folders) if folders else "No folders found in the folder."

    message = file_message + "\n\n" + folder_message

    update.message.reply_text(message)


# Show information about the GitHub repository.
def repo_info(update: Update, context):
    user_id = update.message.from_user.id
    if not check_repo_info(user_id):
        update.message.reply_text('Please set the repository owner, name, and GitHub token first.')
        return

    # Fetch repository information
    url = f'https://api.github.com/repos/{repo_owner[update.message.from_user.id]}/{repo_name[update.message.from_user.id]}'
    headers = {'Authorization': f'token {git_token[update.message.from_user.id]}'}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        update.message.reply_text('An error occurred while fetching the repository information.')
        return

    data = response.json()
    repo_title = data['name']
    repo_description = data['description']
    repo_url = data['html_url']

    message = f"Repository Name: {repo_title}\n\n"
    message += f"Description: {repo_description}\n\n"
    message += f"URL: {repo_url}"

    update.message.reply_text(message)

# Switch between multiple branches on the repo, needs to specify and parse the branch name
def switch(update: Update, context):
    user_id = update.message.from_user.id
    if not check_repo_info(user_id):
        update.message.reply_text('Please set the repository owner, name, and GitHub token first.')
        return
    
    # Parse the branch name from the message
    message = update.message.text.split()

    if len(message) < 2:
        update.message.reply_text('Please provide the branch name along with the command.\n\n'
                                  'Example: /switch branch_name')
        return

    branch_name = message[1]

    # Store the selected branch in the user's context
    context.user_data['branch'] = branch_name

    update.message.reply_text(f'Switched to branch "{branch_name}"')

# Print/Fetch repository information
def repo_info(update: Update, context):
    user_id = update.message.from_user.id
    if not check_repo_info(user_id):
        update.message.reply_text('Please set the repository owner, name, and GitHub token first.')
        return

    # Fetch repository information
    url = f'https://api.github.com/repos/{repo_owner[update.message.from_user.id]}/{repo_name[update.message.from_user.id]}'
    headers = {'Authorization': f'token {git_token[update.message.from_user.id]}'}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        update.message.reply_text('An error occurred while fetching the repository information.')
        return

    data = response.json()
    repo_title = data['name']
    repo_description = data['description']
    repo_url = data['html_url']

    message = f"Repository Name: {repo_title}\n\n"
    message += f"Description: {repo_description}\n\n"
    message += f"URL: {repo_url}"

    update.message.reply_text(message)


# Unknown commands
def unknown_command(update, context):
    message = "Sorry, I didn't understand that command. Please use /help to see the available commands."
    update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)


# Simple return function to get stored data of the repo name, owner & git token
def check_repo_info(user_id):
    return (
        user_id in repo_owner
        and user_id in repo_name
        and user_id in git_token
        and repo_owner[user_id]
        and repo_name[user_id]
        and git_token[user_id]
    )