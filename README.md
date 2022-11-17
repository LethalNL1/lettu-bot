# lettu-bot
Lettu is a Discord bot written in python. Lettu uses the Hikari and Lightbulb libraries to communicate with Discord's API. Lettu saves it's information in a remote MariaDB database. This is my first project, any advice, questions or contributions will be appreciated. 

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