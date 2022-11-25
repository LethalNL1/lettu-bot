import hikari
import lightbulb
from lettu import db
from hikari import VoiceStateUpdateEvent
from hikari import GuildMessageCreateEvent
from datetime import date

plugin = lightbulb.Plugin("on_activity")


@plugin.listener(VoiceStateUpdateEvent)
async def on_voice_update(event):
    if event.state.channel_id == None:
        if not event.state.member.is_bot:
            current_date = str(date.today())
            member_id = event.state.user_id
            guild_id = event.guild_id
            cur = db.connect()
            cur.execute("UPDATE Members SET LastActive = ? WHERE GuildID = ? AND MemberID = ?",
                        (current_date, guild_id, member_id))
            cur.close()


@plugin.listener(GuildMessageCreateEvent)
async def on_message_create(event):
    if not event.is_bot:
        current_date = str(date.today())
        member_id = event.author_id
        guild_id = event.guild_id
        cur = db.connect()
        cur.execute("UPDATE Members SET LastActive = ? WHERE GuildID = ? AND MemberID = ?",
                    (current_date, guild_id, member_id))
        cur.close()


def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)
