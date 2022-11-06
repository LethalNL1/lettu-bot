import hikari
import lightbulb
from lightbulb.ext import tasks
from lettu import db
from datetime import datetime
import pytz

plugin=lightbulb.Plugin("check_birthday")

@tasks.task(tasks.CronTrigger('0,30 * * * *'), auto_start=True) 
async def check_birthday():
    bot = check_birthday._app
    utc = pytz.timezone('UTC').localize(datetime.utcnow())
    cur = db.connect()
    cur.execute("SELECT MemberID, Timezone, Birthday, GuildSettings.GuildID, GuildSettings.BirthdayRole, GuildSettings.AnnounceChannel, GuildSettings.DefaultTimezone FROM Members JOIN GuildSettings ON Members.GuildID=GuildSettings.GuildID WHERE Birthday IS NOT NULL AND GuildSettings.EnabledBirthday = 1;")
    for member_id, timezone, birthday, guild_id, birthday_role, announce_channel, default_timezone in cur:
        if timezone == None:
            zone = pytz.timezone(default_timezone)
        else:
            zone = pytz.timezone(timezone)
        zone_date = str(utc.astimezone(zone))[5:10]
        zone_year = str(utc.astimezone(zone))[:4]
        birthday_date = str(birthday)[5:]
        birthday_year = str(birthday)[:4]
        if zone_date == birthday_date:
            if [guild_id, member_id] in bot.d.birthdays:
                return
            else:
                bot.d.birthdays.append([guild_id, member_id])
                guild = await bot.rest.fetch_guild(guild_id)
                member = await bot.rest.fetch_member(guild,member_id)
                channel = await bot.rest.fetch_channel(announce_channel)
                if birthday_role != None:
                    roles = await bot.rest.fetch_roles(guild)
                    for server_role in roles:
                        if str(server_role.id) == birthday_role:
                            role = server_role
                    await bot.rest.add_role_to_member(guild,member.user,role)
                if birthday_year != "1880":
                    birthday_message = f"**Today is {member.mention}'s birthday!** They are now **{int(zone_year) - int(birthday_year)} years** old. Wish them a happy birthday!"
                else:
                    birthday_message = f"**Today is {member.mention}'s birthday!** Wish them a happy birthday!"
                await bot.rest.create_message(channel, birthday_message)
        else:
            if [guild_id, member_id] in bot.d.birthdays:
                bot.d.birthdays.pop(bot.d.birthdays.index([guild_id, member_id]))
                if birthday_role != None:
                    guild = await bot.rest.fetch_guild(guild_id)
                    member = await bot.rest.fetch_member(guild,member_id)
                    roles = await bot.rest.fetch_roles(guild)
                    for server_role in roles:
                        if str(server_role.id) == birthday_role:
                            role = server_role
                    await bot.rest.remove_role_from_member(guild,member.user,role)
    cur.close()

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)