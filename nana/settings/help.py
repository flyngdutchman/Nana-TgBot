import re
import pyrogram

from pyrogram import Filters, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQueryHandler
from nana import setbot, Owner, log, Command
from __main__ import HELP_COMMANDS
from nana.helpers.misc import paginate_modules


HELP_STRINGS = f"""
Hello! I am {setbot.get_me()['first_name']}, your Assistant!
I can help you for many things.

**Main** commands available::
 - /start: get your bot status
 - /stats: get your userbot status
 - /settings: settings your userbot
 - /getme: get your userbot profile info
 - /help: get all modules help

You can use {", ".join(Command)} on your userbot to execute that commands.
Here is current modules you have
"""


def help_parser(client, chat_id, text, keyboard=None):
	if not keyboard:
		keyboard = InlineKeyboardMarkup(paginate_modules(0, HELP_COMMANDS, "help"))
	client.send_message(chat_id, text, reply_markup=keyboard)


@setbot.on_message(Filters.user(Owner) & Filters.command(["help"]))
def help_command(client, message):
	if message.chat.type != "private":
		keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="Bantuan", url=f"t.me/{setbot.get_me()['username']}?start=help")]])
		message.reply("Hubungi saya di PM untuk mendapatkan daftar perintah.", reply_markup=keyboard)
		return
	help_parser(client, message.chat.id, HELP_STRINGS)


def help_button(client, query):
	mod_match = re.match(r"help_module\((.+?)\)", query.data)
	prev_match = re.match(r"help_prev\((.+?)\)", query.data)
	next_match = re.match(r"help_next\((.+?)\)", query.data)
	back_match = re.match(r"help_back", query.data)
	if True:
		if mod_match:
			module = mod_match.group(1)
			text = "This is help for the module **{}**:\n".format(HELP_COMMANDS[module].__MODULE__) \
				   + HELP_COMMANDS[module].__HELP__

			query.message.edit(text=text,
								  reply_markup=InlineKeyboardMarkup(
										[[InlineKeyboardButton(text="⬅️ Back", callback_data="help_back")]]))

		elif prev_match:
			curr_page = int(prev_match.group(1))
			query.message.edit_text(text=HELP_STRINGS,
								  reply_markup=InlineKeyboardMarkup(
										paginate_modules(curr_page - 1, HELP_COMMANDS, "help")))

		elif next_match:
			next_page = int(next_match.group(1))
			query.message.edit(text=HELP_STRINGS,
								  reply_markup=InlineKeyboardMarkup(
										paginate_modules(next_page + 1, HELP_COMMANDS, "help")))

		elif back_match:
			query.message.edit(text=HELP_STRINGS,
								  reply_markup=InlineKeyboardMarkup(paginate_modules(0, HELP_COMMANDS, "help")))


help_callback_handler = CallbackQueryHandler(help_button)
setbot.add_handler(help_callback_handler)