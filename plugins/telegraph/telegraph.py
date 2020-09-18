import io

import requests
from pyrogram import Client, filters, emoji
from pyrogram.types import Message
from telegraph import utils

from main import prefixes

HEADERS = {"Origin": "https://telegra.ph"}


@Client.on_message(
    filters.user("self") & filters.command("telegraph", prefixes=prefixes)
)
def telegraph(c: Client, msg: Message):
    if len(msg.command) > 1:
        targetmsg = msg
        text = (
                targetmsg.text[len("/telegraph"):]
                or targetmsg.caption[len("/telegraph"):]
        )
        author = targetmsg.from_user.first_name
        title = msg.chat.username or msg.chat.title or msg.chat.first_name
    elif msg.reply_to_message:
        targetmsg = msg.reply_to_message
        text = targetmsg.text
        author = targetmsg.from_user.first_name
        title = msg.chat.username or msg.chat.title or msg.chat.first_name
    else:
        msg.edit_text(
            "Please reply to a message or specify the text with <code>/telegraph Some Text Here</code>"
        )
        return 1

    if not text:
        msg.edit_text(
            f"{emoji.NEWSPAPER} Telegraph\n"
            f"\n"
            f"{emoji.CROSS_MARK} <b>Error:</b> <code>Invalid message</code>"
        )

    nodes = utils.html_to_nodes(text.replace("'", "\\u0027"))

    if len(nodes) == 0:
        msg.edit_text(
            f"{emoji.NEWSPAPER} Telegraph\n"
            f"\n"
            f"{emoji.CROSS_MARK} <b>Error:</b> <code>Invalid text!</code>"
        )

    content = (
            "["
            + "".join(
        [
            '{{"tag": "p", "children": [{}]}},'.format(
                i if isinstance(i, str) else f'"{i}"'
            )
            for i in nodes[:-1]
        ]
    )
            + '{{"tag": "p", "children": [{}]}}'.format(
        nodes[-1] if isinstance(nodes[-1], str) != str else f'"{nodes[-1]}"'
    )
            + "]"
    )

    files = {
        "Data": (
            "content.html",
            io.BytesIO(content.replace("'", '"').encode()),
            "plain/text",
        )
    }
    data = {
        "title": title,
        "author": author,
        "author_url": "https://github.com/GodSaveTheDoge",
        "save_hash": "",
        "page_id": "0",
    }

    r = requests.post(
        "https://edit.telegra.ph/save", files=files, data=data, headers=HEADERS
    ).json()

    if "error" in r.keys():
        msg.edit_text(
            f"{emoji.NEWSPAPER} Telegraph\n"
            f"\n"
            f"{emoji.CROSS_MARK} <b>Error:</b> <code>{r['error']}</code>"
        )
        return 1

    msg.edit_text(
        f"{emoji.NEWSPAPER} Telegraph\n"
        f"\n"
        f"{emoji.PAGE_WITH_CURL} <b>Title:</b> <code>{title}</code>\n"
        f"{emoji.LINK} <b>Link:</b> https://telegra.ph/{r['path']}\n"
        f"{emoji.PEN} <b>Author:</b> <code>{author}</code>",
        parse_mode="html",
    )
