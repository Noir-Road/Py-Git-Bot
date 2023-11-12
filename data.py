from telegram import Update
from telegram.ext import CallbackContext
from git_config import repo_name, repo_owner, git_token

# Get the stored name
def get_repo_name(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    if user_id in repo_name:
        update.message.reply_text(f"The repo name: {repo_name[user_id]}")
    else:
        update.message.reply_text("Repo name is null, set one using: /setreponame")

# Get the owner name
def get_repo_owner(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    if user_id in repo_owner:
        update.message.reply_text(f"The repo owner is: {repo_owner[user_id]}")
    else:
        update.message.reply_text("Repo owner is null, set one using: /setowner")

# Get token information
def get_token(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    if user_id in git_token:
        update.message.reply_text(f"The token is: {git_token[user_id]}")
    else:
        update.message.reply_text("Token is not yet assigned, please use to set one: /settoken")