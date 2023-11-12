from telegram import Update
from telegram.ext import CallbackContext

# Dictionary
repo_name = {}
repo_owner = {}
git_token = {}

# Ask for the repo name
def set_repo_name(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Please enter the repo name")
    context.user_data["waiting_for_name"] = True

# Ask for the repo owner
def set_repo_owner(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Please enter the repo owner")
    context.user_data["waiting_for_repo_owner"] = True

# Ask for the github token
def set_token(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Please enter the Github Token: ")
    context.user_data["waiting_for_token"] = True

#region Handlers => Set states
def handle_name(update: Update, context: CallbackContext) -> None:
    if "waiting_for_name" in context.user_data:
        repo_name[update.message.from_user.id] = update.message.text

def handle_repo_owner(update: Update, context: CallbackContext) -> None:
    if "waiting_for_repo_owner" in context.user_data:
        repo_owner[update.message.from_user.id] = update.message.text

def handle_token(update: Update, context: CallbackContext) -> None:
    if "waiting_for_token" in context.user_data:
        git_token[update.message.from_user.id] = update.message.text
#endregion

# Handle user input text after using a setter
def handle_text(update: Update, context: CallbackContext) -> None:
    message_text = update.message.text

    if context.user_data.get("waiting_for_name"):
        # Store repo name in the dictionary
        repo_name[update.message.from_user.id] = message_text

        # Exit from the waiting state and acknowledge input data
        update.message.reply_text(f"Repo name is: {message_text}")
        context.user_data.pop("waiting_for_name")

    elif context.user_data.get("waiting_for_repo_owner"):
        repo_owner[update.message.from_user.id] = message_text
    
        update.message.reply_text(f"Repo owner is: {message_text}")
        context.user_data.pop("waiting_for_repo_owner")

    elif context.user_data.get("waiting_for_token"):
        git_token[update.message.from_user.id] = message_text

        update.message.reply_text(f"GitToken stored: {message_text}")
        context.user_data.pop("waiting_for_token")