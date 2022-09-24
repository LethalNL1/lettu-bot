import hikari
import lightbulb
from lightbulb import commands
from lettu import db

features = ["Birthdays",
            "Anniversaries",
            "Autokick",
            "Autokick Warnings"
            ]

@lightbulb.option("feature", "Select the feature you want to enable", choices=features, required=True)
@lightbulb.add_checks(lightbulb.has_role_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.command("adm_toggle", "Enable certain features of the bot")
@lightbulb.implements(commands.SlashCommand)

async def adm_toggle(ctx: lightbulb.context.Context):
    feature = ctx.options.feature
    guild_id = ctx.guild_id
    cur = db.connect()
    cur.execute("SELECT EnabledBirthday, EnabledAnniversary, EnabledAutoKick, EnabledKickWarning FROM GuildSettings WHERE GuildID = ?",(guild_id,))
    for (EnabledBirthday, EnabledAnniversary, EnabledAutoKick, EnabledKickWarning) in cur:
        pass
    if feature == "Birthdays":
        if EnabledBirthday == 0:
            cur.execute("UPDATE GuildSettings SET EnabledBirthday = 1 WHERE GuildID = ?",(guild_id,))
            state = "are now enabled"
        else:
            cur.execute("UPDATE GuildSettings SET EnabledBirthday = 0 WHERE GuildID = ?",(guild_id,))     
            state = "are now disabled"   
    elif feature == "Anniversaries":
        if EnabledAnniversary == 0:
            cur.execute("UPDATE GuildSettings SET EnabledAnniversary = 1 WHERE GuildID = ?",(guild_id,))
            state = "are now enabled"
        else:
            cur.execute("UPDATE GuildSettings SET EnabledAnniversary = 0 WHERE GuildID = ?",(guild_id,))     
            state = "are now disabled"
    elif feature == "Autokick":
        if EnabledAutoKick == 0:
            cur.execute("UPDATE GuildSettings SET EnabledAutoKick = 1 WHERE GuildID = ?",(guild_id,))
            state = "is now enabled"
        else:
            cur.execute("UPDATE GuildSettings SET EnabledAutoKick = 0 WHERE GuildID = ?",(guild_id,))     
            state = "is now disabled"  
    else:
        if EnabledKickWarning == 0:
            cur.execute("UPDATE GuildSettings SET EnabledKickWarning = 1 WHERE GuildID = ?",(guild_id,))
            state = "are now enabled"
        else:
            cur.execute("UPDATE GuildSettings SET EnabledKickWarning = 0 WHERE GuildID = ?",(guild_id,))     
            state = "are now disabled"  
 

    cur.close()
    return await ctx.respond(f"{feature} {state}.")


def load(bot: lightbulb.BotApp):
    bot.command(adm_toggle)

def unload(bot: lightbulb.BotApp):
    bot.remove_command(bot.get_slash_command("adm_toggle"))


