import hikari
import lightbulb
from lightbulb.ext import tasks
from lettu import db
from datetime import date
from dateutil.relativedelta import relativedelta

plugin=lightbulb.Plugin("auto_kick")

@tasks.task(tasks.CronTrigger('* * * * *'), auto_start=True)
async def auto_kick():
    bot = auto_kick._app
    cur = db.connect()
    cur.execute("SELECT MemberID, LastActive, GuildSettings.GuildID, GuildSettings.AutoKickInterval, GuildSettings.EnabledKickWarning, GuildSettings.AdminChannel FROM Members INNER JOIN GuildSettings ON Members.GuildID = GuildSettings.GuildID WHERE GuildSettings.EnabledAutoKick = 1 AND LeftAt IS NULL AND GuildSettings.AutoKickInterval IS NOT NULL")
    for member_id, last_active, guild_id, autokick_interval, enabled_kick_warning, admin_channel in cur:
        amount, unit = autokick_interval.split(" ")
        current_date = date.today()
        if unit == "Weeks":
            amount = int(amount)
            kick_date = current_date - relativedelta(weeks=amount)
        elif unit == "Months":
            kick_date = current_date - relativedelta(months=amount)
        else:
            kick_date = current_date - relativedelta(years=amount)                
        guild = await bot.rest.fetch_guild(guild_id)
        member = await bot.rest.fetch_member(guild,member_id)
        try:
            channel = await bot.rest.fetch_channel(admin_channel)
        except:
            owner = await bot.rest.fetch_member(guild,guild.owner_id)
            channel = await bot.rest.create_dm_channel(owner.user)
        dm_channel = await bot.rest.create_dm_channel(member.user)
        warning_date = kick_date + relativedelta(days=3)
        if str(warning_date) == str(last_active) and enabled_kick_warning == 1:
            await bot.rest.create_message(channel, f"{member.mention} will be kicked in 3 days for being inactive for {autokick_interval}.")           
            await bot.rest.create_message(dm_channel, f"You will be kicked from {guild.name} in 3 days for being inactive for too long ({autokick_interval}). If you want to stay in this server, you should send a message or join and leave a vc there. After that you should not get kicked.")
        elif kick_date >= last_active:
            print(member.username)
            print(f"{type(kick_date)} {kick_date}")
            print(f"{type(last_active)} {last_active}")
            await bot.rest.create_message(channel, f"{member.username} has been kicked for being inactive too long ({autokick_interval}).")
            await bot.rest.create_message(dm_channel, f"You have been kicked from {guild.name} for being inactive for too long ({autokick_interval}).")      
    cur.close()
            

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)