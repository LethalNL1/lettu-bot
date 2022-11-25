import hikari
import lightbulb
from lightbulb import commands
from lettu import db
from hikari import Role

roles = [
    "Birthday"
]


@lightbulb.option("role", "Mention the role you want to use.", required=True, type=Role)
@lightbulb.option("function", "Which role do you want to set?", required=True, choices=roles)
@lightbulb.add_checks(lightbulb.has_role_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.command("adm_set_role", "Set a role for a function.")
@lightbulb.implements(commands.SlashCommand)
async def adm_set_role(ctx: lightbulb.context.Context):
    if ctx.options.function == "Birthday":
        guild_id = ctx.guild_id
        role_id = ctx.options.role.id
        cur = db.connect()
        try:
            cur.execute(
                "UPDATE GuildSettings SET BirthdayRole = ? WHERE GuildID = ?", (role_id, guild_id))
        except Exception as e:
            print(e)
        cur.close()
        await ctx.respond(f"The birthday role has been updated to {ctx.options.role.mention}.")


def load(bot: lightbulb.BotApp):
    bot.command(adm_set_role)


def unload(bot: lightbulb.BotApp):
    bot.remove_command(bot.get_slash_command("adm_set_role"))
