import hikari
import lightbulb
from lightbulb import commands
from lettu import db
import pytz


@lightbulb.option("set", "Set the timezone you want to use.", required=True)
@lightbulb.add_checks(lightbulb.has_role_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.command("adm_default_timezone", "Set the server default timezone.")
@lightbulb.implements(commands.SlashCommand)
async def adm_default_timezone(ctx: lightbulb.context.Context):
    guild_id = ctx.guild_id
    timezones = [tz for tz in pytz.all_timezones]
    if ctx.options.set in timezones:
        cur = db.connect()
        cur.execute("UPDATE GuildSettings SET DefaultTimezone = ? WHERE GuildID = ?",
                    (ctx.options.set, guild_id))
        cur.close()
        await ctx.respond(f"The server's default timezone has been updated to {ctx.options.set}")
    else:
        await ctx.respond("Invalid timezone, to get your timezone go to https://kevinnovak.github.io/Time-Zone-Picker/ .")


def load(bot: lightbulb.BotApp):
    bot.command(adm_default_timezone)


def unload(bot: lightbulb.BotApp):
    bot.remove_command(bot.get_slash_command("adm_default_timezone"))
