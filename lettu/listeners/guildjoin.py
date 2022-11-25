import hikari
import lightbulb
from lettu import db

plugin = lightbulb.Plugin("on_server_join")


@plugin.listener(hikari.GuildJoinEvent)
async def on_server_join(event):
    guild_id = event.guild_id
    members = event.members
    system_channel = (await event.guild.fetch_system_channel()).id
    cur = db.connect()
    try:
        cur.execute("INSERT INTO Guilds (GuildID) VALUES(?)", (guild_id,))
    except Exception as e:
        print(e)
    try:
        cur.execute("INSERT INTO GuildSettings (GuildID,AnnounceChannel) VALUES(?,?)",
                    (guild_id, system_channel))
    except Exception as e:
        print(e)
    for member in members.values():
        if not member.is_bot:
            join_date = str(member.joined_at).split(" ")[0]
            try:
                cur.execute("INSERT INTO Members (GuildID, MemberID, JoinedAt) VALUES(?,?,?)",
                            (guild_id, member.id, join_date))
            except Exception as e:
                print(e)
    cur.close()


def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)
