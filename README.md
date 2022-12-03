# lettu-bot
Lettu is a Discord bot written in python. Lettu uses the Hikari and Lightbulb libraries to communicate with Discord's API. Lettu saves it's information in a remote MariaDB database. This is my first project, any advice, questions or contributions will be appreciated.

## Features
Lettu aims to be a general purpose and administration discord bot.

Lettu can:
- Announce birthdays of members
	- Give them a birthday role
	- Remove the role automatically
- Announce anniversaries of members
- Kick Members who have not been active (FUTURE)
	- Set the roles auto kick applies to (FUTURE)
	- Remind people in dm that they are about to get kicked (FUTURE)
	- Remind server admins that someone is about to get kicked (FUTURE)
- Listen for activity
	- Award points to users for being active (FUTURE)
	- Award roles to users for having points (FUTURE)
	- Remove points from users who are inactive (FUTURE)
	- Remove roles from users losing points (FUTURE)
- Interact with my Minecraft server
	- Query the status of my minecraft server
	- Turn the server on
	- Whitelist their minecraft account on the server

Members can:
- Add their birthday
- Add their timezone
- Syncronize this information across all servers Lettu and them are in
- Gain points and roles for being active (FUTURE)
- Lose points and roles for being inactive (FUTURE)
- Get kicked for being inactive (FUTURE)

Admins can:
- Toggle features of the bot on or off
- Set the channel to announce admin messages
- Set the channel to announce normal messages
- Set the default timezone of the server
- Set the interval of inactivity before a user is kicked (FUTURE)
- Blacklist roles from being autokicked (FUTURE)
- Blacklist roles from gaining points (FUTURE)
- Set the amount of points gained per action (FUTURE)
- Set the amount of points lost per timeframe (FUTURE)

## Installation
In order to make the bot run without any errors, please follow the steps down below.

### MariaDB
Lettu communicates with a MariaDB Database. Please refer to the MariaDB documentation or your distribution's documentation for issues.

1. Create a database named lettu
2. Create the following tables:
```
CREATE TABLE `GuildSettings` (
	  `GuildID` varchar(18) NOT NULL,
	  `AdminChannel` varchar(18) DEFAULT NULL,
	  `AnnounceChannel` varchar(18) DEFAULT NULL,
	  `EnabledBirthday` tinyint(1) NOT NULL DEFAULT 0,
	  `DefaultTimezone` varchar(32) DEFAULT NULL,
	  `BirthdayRole` varchar(18) DEFAULT NULL,
	  `EnabledAnniversary` tinyint(1) NOT NULL DEFAULT 0,
	  `EnabledAutoKick` tinyint(1) NOT NULL DEFAULT 0,
	  `AutoKickInterval` varchar(10) DEFAULT NULL,
	  `EnabledKickWarning` tinyint(1) NOT NULL DEFAULT 0,
	  PRIMARY KEY (`GuildID`),
	  CONSTRAINT `GuildSettings_ibfk_1` FOREIGN KEY (`GuildID`) REFERENCES `Guilds` (`GuildID`)
)

CREATE TABLE `Guilds` (
	  `GuildID` varchar(18) NOT NULL,
	  PRIMARY KEY (`GuildID`)
)

CREATE TABLE `Members` (
	  `GuildID` varchar(18) NOT NULL,
	  `MemberID` varchar(18) NOT NULL,
	  `AP` int(11) DEFAULT 0,
	  `Timezone` varchar(32) DEFAULT NULL,
	  `Birthday` date DEFAULT NULL,
	  `JoinedAt` date NOT NULL,
	  `LastActive` date DEFAULT curdate(),
	  `LeftAt` date DEFAULT NULL,
	  PRIMARY KEY (`GuildID`,`MemberID`),
	  CONSTRAINT `Members_ibfk_1` FOREIGN KEY (`GuildID`) REFERENCES `Guilds` (`GuildID`)
)
```
3. Configure remote access to the database. This includes opening up your MariaDB port in your firewall.
4. Install the MariaDB Python connector.
5. Create credentials.py in the lettu-bot/lettu folder and use the following format.
```
USER="database-username"
PASSWORD="database-password"
HOST="ip.address.of.server"
PORT=3306
DBNAME="database-name"
```

### Bot token
1. Insert your bot token in the lettu-bot/secrets/.token file.
2. Rename the file to "token".

### Pip3

1. Install the python package manager, pip3, on your system.
2. Go into lettu-bot/lettu
3. pip3 install -r requirements.txt

### Done!
The installation process is now finished, enjoy using and modifying Lettu to your needs!