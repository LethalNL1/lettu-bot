import hikari
import lightbulb
from lightbulb import commands
from lettu import db

units = [
    "Weeks",
    "Months",
    "Years",
]


@lightbulb.option("amount", "Amount of certain unit", required=True, max_value=52, type=int)
@lightbulb.option("unit", "The units used for the interval", choices=units, required=True)
@lightbulb.add_checks(lightbulb.has_role_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.command("adm_set_interval", "Set interval for the autokick feature.")
@lightbulb.implements(commands.SlashCommand)
async def adm_set_interval(ctx: lightbulb.context.Context):
    guild_id = ctx.guild_id
    interval = f"{ctx.options.amount} {ctx.options.unit}"
    cur = db.connect()
    cur.execute(
        "UPDATE GuildSettings SET AutoKickInterval = ? WHERE GuildID = ?", (interval, guild_id))
    cur.close()
    await ctx.respond(f"The Autokick interval has been set to {interval.lower()}.")


def load(bot: lightbulb.BotApp):
    bot.command(adm_set_interval)


def unload(bot: lightbulb.BotApp):
    bot.remove_command(bot.get_slash_command("adm_set_interval"))
