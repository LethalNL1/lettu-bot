import hikari
import lightbulb
from lightbulb.ext import tasks
from lettu import db
from datetime import date

plugin = lightbulb.Plugin("check_anniversary")


@tasks.task(tasks.CronTrigger('5 0 * * *'), auto_start=True)
async def check_birthday():
    bot = check_birthday._app
    cur = db.connect()
    curr_date = str(date.today())[5:]
    curr_year = str(date.today())[:4]
    cur.execute("SELECT MemberID, JoinedAt, GuildSettings.GuildID, GuildSettings.AnnounceChannel FROM Members JOIN GuildSettings ON Members.GuildID=GuildSettings.GuildID WHERE GuildSettings.EnabledAnniversary = 1;")
    for member_id, joined_at, guild_id, announce_channel in cur:
        if str(joined_at)[5:] == curr_date:
            year_joined = str(joined_at)[:4]
            year = int(curr_year) - int(year_joined)
            if year != 0:
                guild = await bot.rest.fetch_guild(guild_id)
                member = await bot.rest.fetch_member(guild, member_id)
                channel = await bot.rest.fetch_channel(announce_channel)
                await bot.rest.create_message(channel, f"**Today is {member.mention}'s anniversary!** They have been in this server for **{year} years**.")


def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)
