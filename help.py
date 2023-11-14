from telegram import Update

# COMMANDS list with command descriptions
COMMANDS = [
    ("**Usage:**", "\nRemember to set up the following:\n"),
    ("/setreponame", "Set the repository name."),
    ("/setowner", "Set the repository owner."),
    ("/settoken", "Set the GitHub token.\n"),
    ("**Commands:**", "\nThe following list are the commands available\n"),
    "/help - Get information about available commands and their descriptions.",
    "/gitlog [branch name] [x] - Retrieve detailed Git log information from a specific branch and commits.",
    #"/file [/to/file.txt] - Print the contents of a file from the repository.",
    "/ls [/folder/file] - Retrieve a list of files and folders in the repository.",
    "/updates - Retrieve a list of the latest updates made on the repository.",
    "/branches - Get a list of branches in the repository.",
    "/switch [branch name] - Switch to a different branch in the repository.",
    "/repo - Get detailed information about the repository."
    #"/contact - Contact the developer for support and inquiries.",
    #"/version - Get the version information for GitBotX."
]

def help(update: Update, context):
    """Send a message with the available commands and their descriptions."""
    commands = []
    for command in COMMANDS:
        if isinstance(command, tuple):
            commands.append(f"{command[0]} {command[1]}")
        else:
            commands.append(command)

    message = "🤖 **Available Commands:**\n\n" + "\n".join(commands)
    update.message.reply_text(message, disable_web_page_preview=True)


# Maximum length of each message chunk
MAX_MESSAGE_LENGTH = 4096