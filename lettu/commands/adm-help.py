import hikari
import lightbulb
from lightbulb import commands


@lightbulb.add_checks(lightbulb.has_role_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.command("adm_help", "Show commands used to set the bot up and how to use them.")
@lightbulb.implements(commands.SlashCommand)
async def adm_help(ctx: lightbulb.context.Context):
    message = "Commands starting with adm are admin commands used to toggle features, set roles and channels, and configure the bot to the servers needs. It is recommended to configure each of these settings for stability (things are more likely to break if not set).\n\n**/adm_set_channel**\nTakes a type, which is the type of channel you want to set. You can set both the Admin channel and Announcement channel. The Admin channel is used for Autokick warnings. The announcement channel is used for announcing Anniversaries and birthdays.\nThe second argument takes a channel, you can pick one by typing the name of the channel with a # in front.\n\n**/adm_set_role**\nUsed to set a role for a certain functionality. The only feature currently available that needs a role is birthdays. You can tag a role to give to the members once it's their birthday. When their Birthday is over it will automatically take it away.\n\n**/adm_default_timezone**\nSet the server default timezone. Takes a timezone from the IANA Database, see: https://kevinnovak.github.io/Time-Zone-Picker/. \n\n**/adm_toggle**\nToggle certain features on and off.\n\n**/adm_set_interval**\nSet the interval of autokick, can specify the units and amount."
    await ctx.respond(message)


def load(bot: lightbulb.BotApp):
    bot.command(adm_help)


def unload(bot: lightbulb.BotApp):
    bot.remove_command(bot.get_slash_command("adm_help"))
