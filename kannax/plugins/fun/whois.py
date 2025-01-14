# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# Editado por fnixdev

import os

from pyrogram.errors.exceptions.bad_request_400 import BotMethodInvalid

from kannax import Message, kannax


@kannax.on_cmd(
    "whois",
    about={
        "header": "use isso para obter quaisquer detalhes do usuário",
        "usage": "basta responder a qualquer mensagem do usuário ou adicionar user_id ou username",
        "examples": "{tr}whois [user_id | username]",
    },
    allow_channels=False,
)
async def who_is(message: Message):
    await message.edit("`Coletando informações Whois .. Espere um pouco!`")
    user_id = message.input_str
    if user_id:
        try:
            from_user = await message.client.get_users(user_id)
            from_chat = await message.client.get_chat(user_id)
        except Exception:
            await message.err(
                "nenhum user_id ou mensagem válida especificada, use .help whois para mais informações"
            )
            return
    elif message.reply_to_message:
        from_user = await message.client.get_users(
            message.reply_to_message.from_user.id
        )
        from_chat = await message.client.get_chat(message.reply_to_message.from_user.id)
    else:
        await message.err(
            "no valid user_id or message specified, do .help whois for more info"
        )
        return
    if from_user or from_chat is not None:
        pp_c = await message.client.get_profile_photos_count(from_user.id)
        message_out_str = "<b>INFORMAÇÃO DE USUÁRIO:</b>\n\n"
        message_out_str += (
            f"<b>🗣 Primeiro Nome:</b> <code>{from_user.first_name}</code>\n"
        )
        message_out_str += f"<b>🗣 Ultimo Nome:</b> <code>{from_user.last_name}</code>\n"
        message_out_str += f"<b>👤 Username:</b> @{from_user.username}\n"
        message_out_str += f"<b>🏢 DC ID:</b> <code>{from_user.dc_id}</code>\n"
        message_out_str += f"<b>🤖 É bot:</b> <code>{from_user.is_bot}</code>\n"
        message_out_str += f"<b>🚫 É Restrito:</b> <code>{from_user.is_scam}</code>\n"
        message_out_str += "<b>✅ É verificado pelo Telegram:</b> "
        message_out_str += f"<code>{from_user.is_verified}</code>\n"
        message_out_str += f"<b>🕵️‍♂️ User ID:</b> <code>{from_user.id}</code>\n"
        message_out_str += f"<b>🖼 Fotos do Perfil:</b> <code>{pp_c}</code>\n"
        try:
            cc_no = len(await message.client.get_common_chats(from_user.id))
        except BotMethodInvalid:
            pass
        else:
            message_out_str += f"<b>👥 Bate-papos Comuns:</b> <code>{cc_no}</code>\n"
        message_out_str += f"<b>📝 Bio:</b> <code>{from_chat.bio}</code>\n\n"
        message_out_str += (
            f"<b>👁 Visto por Ultimo:</b> <code>{from_user.status}</code>\n"
        )
        message_out_str += "<b>🔗 Link Permanente para o Perfil:</b> "
        message_out_str += (
            f"<a href='tg://user?id={from_user.id}'>{from_user.first_name}</a>"
        )
        if message.chat.type in ("private", "bot"):
            s_perm = True
        else:
            s_perm = message.chat.permissions.can_send_media_messages
        if from_user.photo and s_perm:
            local_user_photo = await message.client.download_media(
                message=from_user.photo.big_file_id
            )
            await message.client.send_photo(
                chat_id=message.chat.id,
                photo=local_user_photo,
                caption=message_out_str,
                parse_mode="html",
                disable_notification=True,
            )
            os.remove(local_user_photo)
            await message.delete()
        else:
            cuz = "Nenhum DP encontrado"
            if not s_perm:
                cuz = "Chat Send Media Forbidden"
            message_out_str = "<b>📷 " + cuz + " 📷</b>\n\n" + message_out_str
            await message.edit(message_out_str)
