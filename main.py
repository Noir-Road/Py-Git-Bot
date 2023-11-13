from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from git_config import set_repo_name, set_repo_owner, set_token, handle_text
from data import get_repo_name, get_repo_owner, get_token
from git_commands import gitlog, branches, switch, file_handler, ls, repo_info, unknown_command
from help import help

def main() -> None:
    updater = Updater('6063228763:AAFISjIjC9WcLmtgwZBopBdA_m3DgQ85nM4')

    dp = updater.dispatcher

    # Set repo data stored
    dp.add_handler(CommandHandler('setreponame', set_repo_name))
    dp.add_handler(CommandHandler('setowner', set_repo_owner))
    dp.add_handler(CommandHandler('settoken', set_token))
    dp.add_handler(CommandHandler('repoinfo', repo_info))
    dp.add_handler(CommandHandler('branch', branches))
    dp.add_handler(CommandHandler('switch', switch))
    dp.add_handler(CommandHandler('file', file_handler))
    dp.add_handler(CommandHandler('ls', ls))

    # View a list of commnads & set-up
    dp.add_handler(CommandHandler('help', help))

    # Git commands
    dp.add_handler(CommandHandler('gitlog', gitlog))
    #### need to add the rest of the handles

    # See data stored
    dp.add_handler(CommandHandler('getreponame', get_repo_name))
    dp.add_handler(CommandHandler("getowner", get_repo_owner))
    dp.add_handler(CommandHandler('gettoken', get_token))

    # Fallback handler for unknown commands
    dp.add_handler(MessageHandler(Filters.command, unknown_command))

    # User response handler
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

    # Bot Trigger
    updater.start_polling()

    # Keep bot running
    updater.idle()

if __name__ == '__main__':
    main()
