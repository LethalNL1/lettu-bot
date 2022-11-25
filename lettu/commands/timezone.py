import hikari
import lightbulb
from lightbulb import commands
from lettu import db
import pytz


@lightbulb.option("zone", "Select your timezone from: https://kevinnovak.github.io/Time-Zone-Picker/ .", required=True)
@lightbulb.command("timezone", "Set your timezone")
@lightbulb.implements(commands.SlashCommand)
async def timezone(ctx: lightbulb.context.Context):
    guild_id = ctx.get_guild().id
    member_id = ctx.author.id
    timezones = [tz for tz in pytz.all_timezones]
    if ctx.options.zone in timezones:
        cur = db.connect()
        cur.execute("UPDATE Members SET Timezone = ? WHERE GuildID = ? AND MemberID = ?",
                    (ctx.options.zone, guild_id, member_id))
        cur.close()
        await ctx.respond(f"Your timezone has been updated to {ctx.options.zone}")
    else:
        await ctx.respond("Invalid timezone, to get your timezone go to https://kevinnovak.github.io/Time-Zone-Picker/. ")


def load(bot: lightbulb.BotApp):
    bot.command(timezone)


def unload(bot: lightbulb.BotApp):
    bot.remove_command(bot.get_slash_command("timezone"))
