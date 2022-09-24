import os

import hikari
import lightbulb
import miru

from lightbulb.ext import tasks
# from lettu import GUILD_ID
from lettu import db

def create_bot() -> lightbulb.BotApp:

    with open("./secrets/token") as f:
        _token = f.read().strip()

    bot = lightbulb.BotApp(
        token=_token,
        intents=hikari.Intents.ALL,
        # default_enabled_guilds=GUILD_ID,
    )
    
    miru.load(bot)

    bot.load_extensions_from("./lettu/commands")
    bot.load_extensions_from("./lettu/listeners")
    bot.load_extensions_from("./lettu/tasks")
    tasks.load(bot)
    bot.d.birthdays = []
    # bot.d.lobbies = []

    return bot

if __name__ == "__main__":
    if os.name != "nt":
        import uvloop
        uvloop.install()
    
    create_bot().run(activity=hikari.presences.Activity(name="the voices in my head", type=2))                                                                                              