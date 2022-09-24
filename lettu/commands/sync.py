import hikari
import lightbulb
from lightbulb import commands
from lettu import db

@lightbulb.command("sync", "Easily one-time synchronize your settings across servers.")
@lightbulb.implements(commands.SlashCommand)

async def sync(ctx: lightbulb.context.Context):
    guild_id = ctx.guild_id
    print(guild_id)
    member_id = ctx.author.id
    print(member_id)
    cur = db.connect()
    cur.execute("SELECT Timezone, Birthday FROM Members WHERE MemberID = ? AND GuildID = ?",(member_id,guild_id))
    for timezone, birthday in cur:
        pass
    cur.execute("UPDATE Members SET Timezone = ?, Birthday = ? WHERE MemberID = ? AND GuildID != ?",(timezone, birthday, member_id, guild_id))
    cur.close()
    await ctx.respond("Your settings have been synced!")

def load(bot: lightbulb.BotApp):
    bot.command(sync)

def unload(bot: lightbulb.BotApp):
    bot.remove_command(bot.get_slash_command("sync"))