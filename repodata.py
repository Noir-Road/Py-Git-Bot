import requests
from telegram import Update
from git_config import repo_name, repo_owner, git_token

def repo_info(update: Update, context):
    """Show information about the GitHub repository."""

    # Check if repo_owner, repo_name, or git_token are not set
    if (
        update.message.from_user.id not in repo_owner
        or update.message.from_user.id not in repo_name
        or update.message.from_user.id not in git_token
        or not repo_owner[update.message.from_user.id]
        or not repo_name[update.message.from_user.id]
        or not git_token[update.message.from_user.id]
    ):
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