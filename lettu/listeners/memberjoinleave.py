import hikari
import lightbulb
import mariadb
from datetime import date
from lettu import db

plugin = lightbulb.Plugin("on_member_create_delete")


@plugin.listener(hikari.MemberCreateEvent)
async def listener(event):
    if not event.member.is_bot:
        guild_id = event.guild_id
        member = event.member
        cur = db.connect()
        join_date = str(member.joined_at).split(" ")[0]
        try:
            cur.execute("INSERT INTO Members (GuildID, MemberID, JoinedAt) VALUES(?,?,?)",
                        (guild_id, member.id, join_date))
        except Exception as e:
            print(e)
        try:
            cur.execute(
                "UPDATE Members set LeftAt = NULL WHERE GuildID = ? AND MemberID = ?", (guild_id, member.id))
        except Exception as e:
            print(e)


@plugin.listener(hikari.MemberDeleteEvent)
async def listener(event):
    if not event.user.is_bot:
        guild_id = event.guild_id
        member = event.user
        leave_date = str(date.today())
        cur = db.connect()
        try:
            cur.execute("UPDATE Members SET LeftAt = ? WHERE GuildID = ? AND MemberID = ?",
                        (leave_date, guild_id, member.id))
        except Exception as e:
            print(e)


def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)
