import hikari
import lightbulb
from lightbulb import commands


@lightbulb.command("help", "Show available commands and how to use them")
@lightbulb.implements(commands.SlashCommand)
async def help(ctx: lightbulb.context.Context):
    msg = "As a normal user there is 2 things you can set up. You can setup your birthday using /birthday and you can set up your timezone using /timezone.\n\n**/birthday**\nTakes a month name (eg. August) and the number of the day without a leading zero (eg. 9, NOT 09.). Optionally, you can choose to add your birth year. This will cause your age to appear in birthday messages.\n\n**/timezone**\nTakes a timezone using a timezone in the IANA time zone database. For easy setup click the following link: https://kevinnovak.github.io/Time-Zone-Picker/. You can click on your location, it will give you the timezone. You can copy & paste this in the command and it will work.\n\n**/sync**\nOne-time syncronize your data from this server in all the servers lettu bot and you are both in."
    await ctx.respond(msg)


def load(bot: lightbulb.BotApp):
    bot.command(help)


def unload(bot: lightbulb.BotApp):
    bot.remove_command(bot.get_slash_command("help"))
