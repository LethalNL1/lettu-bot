import hikari
import lightbulb
from lightbulb import commands
from mcstatus import JavaServer
from wakeonlan import send_magic_packet
from datetime import datetime
from lettu import credentials
from lettu import db
from mojang import API
import os
import time
import json


server = JavaServer.lookup(f"{credentials.MC_DOM}:25565")
start_time = 8
end_time = 23

choice = ["status", "start", "whitelist"]

allowed_guilds = [921149168494452766]
allowed_channels = [1041166235766902824]


@lightbulb.option("name", "Your Minecraft name", type=str, required=False)
@lightbulb.option("choice", "Select the option you want", choices=choice, required=True)
@lightbulb.command("minecraft", "Interact with the minecraft server.")
@lightbulb.implements(commands.SlashCommand)
async def minecraft(ctx: lightbulb.context.Context):
    member_id = ctx.author.id
    if ctx.guild_id in allowed_guilds:
        if ctx.channel_id in allowed_channels:
            bot = ctx.app
            owner = ctx.get_guild().get_member(160699201586462728)
            if ctx.options.choice == "status":
                try:
                    server.ping()
                    online = server.status().players.online
                    await ctx.respond(
                        f"**{credentials.MC_DOM}**\n**State:** Up\n**Online players:** {online}\n\nIf you have issues connecting please contact {owner.mention}. Don't forget to whitelist yourself using /minecraft choice:whitelist name:<Your minecraft name>.")
                except:
                    await ctx.respond(
                        f"**{credentials.MC_DOM}**\n**State:** Down\n\nYou can start it by using /minecraft choice:start")
            elif ctx.options.choice == "start":
                try:
                    server.ping()
                    await ctx.respond(
                        f"Server ({credentials.MC_DOM}) is already running. If you have issues connecting please contact {owner.mention}. Don't forget to whitelist yourself using /minecraft choice:whitelist name:<Your minecraft name>.")
                except:
                    curr_time = datetime.now()
                    if curr_time.hour > 7 and curr_time.hour < 23:
                        response = os.system(f"ping -c 1 {credentials.MC_IP}")
                        if response == 0:
                            print("Minecraft server unreachable. Restarting...")
                            os.system(
                                f"ssh {credentials.USER}@{credentials.MC_IP} sudo systemctl restart minecraft-server")
                            os.system("exit")
                            status = 1
                            while status == 1:
                                try:
                                    server.ping()
                                    status = 0
                                except:
                                    time.sleep(1)
                            print("The server has restarted successfully!")
                        else:
                            print("Server is down. Starting...")
                            send_magic_packet(credentials.MC_MAC)
                            status = 1
                            while status == 1:
                                try:
                                    server.ping()
                                    status = 0
                                except:
                                    time.sleep(1)
                            print("The server has started successfully!")
                    else:
                        await ctx.respond(
                            f"Cannot start the server from {end_time}:00 to {start_time}:00 (Europe/Amsterdam time).\n You can try contacting {owner.mention} if you really want to play.")
            else:
                if ctx.options.name:
                    api = API()
                    uuid = api.get_uuid(ctx.options.name)
                    if uuid:
                        if os.path.exists("whitelist.json"):
                            os.remove("whitelist.json")
                        file = open("whitelist.json", "w")
                        file.write("[\n\n]")
                        file.close()
                        cur = db.connect()
                        cur.execute(
                            "UPDATE Members SET McName = ? WHERE MemberID = ?", (ctx.options.name, member_id))
                        cur.execute(
                            "SELECT DISTINCT McName from Members WHERE McName IS NOT NULL")
                        for McName in cur:
                            try:
                                uuid = api.get_uuid(McName[0])
                                uuid_format = f"{uuid[:8]}-{uuid[8:12]}-{uuid[12:16]}-{uuid[16:20]}-{uuid[20:]}"
                                entry = {
                                    "uuid": str(uuid_format),
                                    "name": McName[0]
                                },
                                file = open("whitelist.json", "r+")
                                file_data = json.load(file)
                                file_data.append(entry[0])
                                file.seek(0)
                                json.dump(file_data, file, indent=2)
                            except Exception as e:
                                print(e)
                        file.close()
                        os.system(
                            f"scp whitelist.json {credentials.USER}@{credentials.MC_IP}:/home/{credentials.USER}/minecraft/whitelist.json")
                        await ctx.respond(f"Added {ctx.options.name} to whitelist.")
                    else:
                        await ctx.respond("This minecraft user doesn't exist, please try again.")
                else:
                    await ctx.respond("Please use the whitelist option together with the name option. /minecraft choice:whitelist name:(your minecraft username)")
        else:
            await ctx.respond(
                "Please use this command in the dedicated minecraft channel of this server.")
    else:
        await ctx.respond("You are not allowed to use this command in this guild.")


def load(bot: lightbulb.BotApp):
    bot.command(minecraft)


def unload(bot: lightbulb.BotApp):
    bot.remove_command(bot.get_slash_command("minecraft"))
