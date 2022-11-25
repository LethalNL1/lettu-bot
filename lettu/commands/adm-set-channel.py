import hikari
import lightbulb
from lightbulb import commands
from lettu import db
from hikari import TextableGuildChannel

types = [
    "Admin",
    "Announcements",
]


@lightbulb.option("channel", "Select the channel.", required=True, type=TextableGuildChannel)
@lightbulb.option("type", "Which type of messages do you want to assign to a channel?", choices=types, required=True)
@lightbulb.add_checks(lightbulb.has_role_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.command("adm_set_channel", "Set a channel for the bot to post messages in.")
@lightbulb.implements(commands.SlashCommand)
async def adm_set_channel(ctx: lightbulb.context.Context):
    if ctx.options.type == "Admin":
        column = "AdminChannel"
    elif ctx.options.type == "Announcements":
        column = "AnnounceChannel"
    guild_id = ctx.guild_id
    channel_id = ctx.options.channel.id
    cur = db.connect()
    query = f"UPDATE GuildSettings SET {column} = ? WHERE GuildID = ?"
    cur.execute(query, (channel_id, guild_id))
    cur.close()
    channel = ctx.get_guild().get_channel(channel_id)
    await ctx.respond(f"The {ctx.options.type} channel has been updated to {channel.mention}.")


def load(bot: lightbulb.BotApp):
    bot.command(adm_set_channel)


def unload(bot: lightbulb.BotApp):
    bot.remove_command(bot.get_slash_command("adm_set_channel"))
