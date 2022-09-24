import hikari
import lightbulb
from lightbulb import commands
from lettu import db
import datetime
import pytz

months = [
    ["January", "01"],
    ["February", "02"],
    ["March", "03"],
    ["April", "04"],
    ["May", "05"],
    ["June", "06"],
    ["July", "07"],
    ["August", "08"],
    ["September", "09"],
    ["October", "10"],
    ["November", "11"],
    ["December", "12"],
]

@lightbulb.option("year", "Set the year",required=False, max_value=2022, min_value=1900, type=int)
@lightbulb.option("month", "Set the month",choices=[month[0] for month in months], required=True)
@lightbulb.option("day", "Set the day",required=True, max_value=31, min_value=1, type=int)
@lightbulb.command("birthday", "Celebrate your birthday.")
@lightbulb.implements(commands.SlashCommand)

async def birthday(ctx: lightbulb.context.Context):
    member_id = ctx.author.id
    guild_id = ctx.guild_id
    if len(str(ctx.options.day)) == 1:
        day = f"0{ctx.options.day}"
    else:
        day = ctx.options.day
    month = months[[month[0] for month in months].index(ctx.options.month)][1]
    if not ctx.options.year:
        year = "1880"
    else:
        year = ctx.options.year
    valid = True
    try:
        datetime.datetime(int(year), int(month), int(day))
    except ValueError:
        valid = False
    if valid == True:
        date = f"{year}-{month}-{day}"
        cur = db.connect() 
        cur.execute("UPDATE Members SET Birthday = ? WHERE GuildID = ? AND MemberID = ?",(date,guild_id,member_id))
        cur.close()
        if year != "1880":
            await ctx.respond(f"Your birthday has been updated to {day} {ctx.options.month} {year}.")
        else:
            await ctx.respond(f"Your birthday has been updated to {day} {ctx.options.month}")
    else:
        await ctx.respond("Not a valid date.")


def load(bot: lightbulb.BotApp):
    bot.command(birthday)

def unload(bot: lightbulb.BotApp):
    bot.remove_command(bot.get_slash_command("birthday"))

