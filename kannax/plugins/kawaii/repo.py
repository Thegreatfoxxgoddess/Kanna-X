# repo

from kannax import Config, Message, kannax


@kannax.on_cmd("repo", about={"header": "get repo link and details"})
async def see_repo(message: Message):
    """see repo"""
    output = f"• **repo** : [my repo]({Config.UPSTREAM_REPO})"
    await message.edit(output)
