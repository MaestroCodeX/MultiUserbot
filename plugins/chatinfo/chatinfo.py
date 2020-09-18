from datetime import datetime

from pyrogram import Client, filters, emoji

from main import prefixes

chatinfo_message = {
    "id": f"{emoji.ID_BUTTON} <b>Id</b>: <code>[%id%]</code>",
    "type": f"{emoji.JAPANESE_SYMBOL_FOR_BEGINNER} <b>Type</b>: <code>[%type%]</code>",
    "title": f"{emoji.FLEUR_DE_LIS} <b>Title</b>: <code>[%title%]</code>",
    "invite_link": f"{emoji.LINK} <b>Invite Link</b>: <code>[%invite_link%]</code>",
    "first_name": f"{emoji.PERSON_LIGHT_SKIN_TONE_BLOND_HAIR} <b>Name</b>: <code>[%first_name%]</code>",
    "last_name": f"{emoji.BUST_IN_SILHOUETTE} <b>Last Name</b>: <code>[%last_name%]</code>",
    "username": f"{emoji.LINK} <b>Username</b>: <code>[%username%]</code>",
    "dc_id": f"{emoji.DESKTOP_COMPUTER} <b>Dc</b>: <code>[%dc_id%]</code>",
    "status": f"{emoji.MOBILE_PHONE_WITH_ARROW} <b>Status</b>: <code>[%status%]</code>",
    "last_online_date": f"{emoji.TWELVE_O_CLOCK} <b>Last Online Date</b>: <code>["
                        f"%last_online_date%]</code>",
    "next_offline_date": f"{emoji.SEVEN_THIRTY} <b>Next Offline Date</b>: <code>["
                         f"%next_offline_date%]</code>",
    "is_bot": f"{emoji.ROBOT} <b>Is Bot</b>: <code>[%is_bot%]</code>",
    "is_contact": f"{emoji.TELEPHONE} <b>Is Contact</b>: <code>[%is_contact%]</code>",
    "is_mutual_contact": f"{emoji.MOBILE_PHONE} <b>Is Mutual Contact</b>: <code>["
                         f"%is_mutual_contact%]</code>",
    "is_scam": f"{emoji.CROSS_MARK} <b>Is scam</b>: <code>[%is_scam%]</code>",
    "sticker_set_name": f"{emoji.DIAMOND_WITH_A_DOT} <b>Sticker Set</b>: <code>["
                        f"%sticker_set_name%]</code>",
    "members_count": f"{emoji.FAMILY_MAN_WOMAN_GIRL_BOY} <b>Members</b>: "
                     f"<code>[%members_count%]</code>",
    "bio": f"{emoji.TRIDENT_EMBLEM} <b>Bio</b>: <code>[%bio%]</code>",
}


@Client.on_message(
    filters.user("self") & filters.command("chatinfo", prefixes=prefixes)
)
def chatinfo_command(c, msg):
    target = c.get_chat(msg.chat.id)
    message = "{} Info {}\n\n".format(emoji.INFORMATION, emoji.INFORMATION)
    for key in chatinfo_message:
        try:
            message += (
                    chatinfo_message[key].replace(
                        f"[%{key}%]",
                        str(
                            (
                                target[key]
                                if key != "next_offline_date" and key != "last_online_date"
                                else (
                                    datetime.fromtimestamp(int(target[key])).strftime(
                                        "%H:%M:%S %d/%m/%y"
                                    )
                                )
                            )
                            if target[key]
                            else (target["raise AttributeError()"])
                        ),
                    )
                    + "\n"
            )
        except AttributeError:
            pass
    bio = c.get_chat(target.id).description
    if bio:
        message += chatinfo_message["bio"].replace(
            "[%bio%]", c.get_chat(target.id).description
        )
    message += f"\n\n<a href=\"https://t.me/c/{target.id if not str(target.id).startswith('-') else (str(target.id)[1:] if not str(target.id).startswith('-100') else str(target.id)[4:])}/1\">Chat Link</a> "
    msg.edit_text(message)
