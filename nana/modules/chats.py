import os

from nana import app, Command, DB_AVAIABLE
from pyrogram import Filters
from nana.modules.database.chats_db import update_chat, get_all_chats


MESSAGE_RECOUNTER = 0

__MODULE__ = "Chats"
__HELP__ = """
This module is collect your chat list, when message was received from unknown chat, and that chat was not in database, then save that chat info to your database.

──「 **Export chats** 」──
-> `chatlist`
Send your chatlist to your saved messages
"""

def get_msgc():
	return MESSAGE_RECOUNTER

@app.on_message(Filters.group, group=10)
async def UpdateMyChats(client, message):
	global MESSAGE_RECOUNTER
	if DB_AVAIABLE:
		update_chat(message.chat)
	MESSAGE_RECOUNTER += 1


@app.on_message(Filters.user("self") & Filters.command(["chatlist"], Command))
async def get_chat(client, message):
	if not DB_AVAIABLE:
		await message.edit("Your database is not avaiable!")
		return
	all_chats = get_all_chats()
	chatfile = 'List of chats that I joined.\n'
	for chat in all_chats:
		if str(chat.chat_username) != "None":
			chatfile += "{} - ({}): @{}\n".format(chat.chat_name, chat.chat_id, chat.chat_username)
		else:
			chatfile += "{} - ({})\n".format(chat.chat_name, chat.chat_id)

	with open("nana/cache/chatlist.txt", "w", encoding="utf-8") as writing:
		writing.write(str(chatfile))
		writing.close()

	await client.send_document("self", document="nana/cache/chatlist.txt", caption="Here is the chat list that I joined.")
	await message.edit("My chat list exported to my saved messages.")
	os.remove("nana/cache/chatlist.txt")
