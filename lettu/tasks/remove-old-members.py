from hikari import MemberDeleteEvent
import lightbulb
import mariadb
from lettu import db
from datetime import date

from dateutil.relativedelta import relativedelta
from lightbulb.ext import tasks

plugin=lightbulb.Plugin("memberleave")

@tasks.task(tasks.CronTrigger('10 * * * *'), auto_start=True)
async def remove_old_members():
    cur = db.connect()
    curr_date = date.today()
    removal_date = curr_date - relativedelta(months=6)
    cur.execute("DELETE FROM Members WHERE LeftAt <= ?",(removal_date,))
    cur.close()

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)