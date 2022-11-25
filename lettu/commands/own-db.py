import hikari
import lightbulb
from lightbulb import commands
from lettu import db


@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.command("own_db", "populate the database")
@lightbulb.implements(commands.SlashCommand)
async def own_db(ctx: lightbulb.context.Context):
    bot = ctx.app
    guilds = await bot.rest.fetch_my_guilds()
    guild_list = []
    cur = db.connect()
    for guild in guilds:
        guild_id = guild.id
        guild_list.append(guild_id)
        try:
            cur.execute("INSERT INTO Guilds (GuildID) VALUES(?)", (guild_id,))
        except Exception as e:
            print(e)
    for guild_id in guild_list:
        try:
            system_channel = (await (await bot.rest.fetch_guild(guild_id)).fetch_system_channel()).id
        except:
            pass
        try:
            cur.execute(
                "INSERT INTO GuildSettings (GuildID,AnnounceChannel) VALUES(?,?)", (guild_id, system_channel))
        except Exception as e:
            print(e)
        member_list = (await bot.rest.fetch_guild(guild_id)).get_members()
        for member in member_list:
            member_id = int(member)
            member = (await bot.rest.fetch_guild(guild_id)).get_member(member_id)
            join_date = str(member.joined_at).split(" ")[0]
            try:
                print(guild_id, member.id, join_date)
                cur.execute("INSERT INTO Members (GuildID, MemberID, JoinedAt) VALUES(?,?,?)",
                            (guild_id, member.id, join_date))
            except Exception as e:
                print(e)


def load(bot: lightbulb.BotApp):
    bot.command(own_db)


def unload(bot: lightbulb.BotApp):
    bot.remove_command(bot.get_slash_command("own_db"))
