<p align="center">
  <img src="https://i.postimg.cc/vm6mgHK3/Banner.png" alt="BB.Bot's banner image."><br>
<h1 align="center">🤖 BB.Bot</h1>
<h3 align="center">🔒 Moderation | 🎵 HQ Music Streaming | 😆 Memes | ⭐ Reaction Roles | ❓ Polls</h3>
<h4 align="center">Powered by discord.py and GCP, BB.Bot is the bot for you.</h4>
<br>

<p align="center">
  <img src="https://img.shields.io/github/v/release/matthewflegg/beepboop?include_prereleases&label=Latest%20Version&style=social">
  <img src="https://img.shields.io/github/v/release/matthewflegg/beepboop?label=Latest%20Stable%20Version&style=social">
</p>
<br>

**BB.Bot** is a Discord bot powered by **Python** and **GCP's Compute Engine**. Featuring 24/7 uptime, HQ music streaming, admin commands, and more, BB.Bot will bring your server to life. **Available for free** and **regularly maintained**, our bot comes with **no additional costs** and **long-term support**.

* Click **[here](https://discord.com/api/oauth2/authorize?client_id=947593856839458916&permissions=8&scope=bot%20applications.commands)** to invite BB.Bot to your server.
* Click **[here](https://discord.gg/tdFRB8uU)** to join our Discord server.<br>
* Click **[here](#-self-hosting)** for self-hosting instructions.
* Click **[here](https://github.com/matthewflegg/bb-bot/blob/master/CONTRIBUTIONS.md)** for information about contributing.

Currently, BB.Bot `2.0.0` is in development. If you're thinking of contributing, please do so on the `release/v2.0.0` branch.
<br><br>

## 📢 **Commands List**

* We use `...argument` to denote a **list of arguments**, like `argument a`, `argument b`, etc...
* We use `argument?` to denote an **optional argument**. You can use the command **with** or **without** one.<br><br>

### 🧭 Contents

* **[Help Commands](#-help-commands)**
* **[Admin Commands](#-admin-commands)**
* **[Music Commands](#-music-commands)**
* **[Role Commands](#-role-commands)**
* **[Misc Commands](#-misc-commands)**
* **[Info Commands](#-info-commands)**
<br><br>  

### 🔖 Help Commands

> **~help**

Sends an embed containing a list of commands and categories.     
You can use **`~help <command>`** or **`~help <category>`** to see more information.

> **~docs**

Sends an embed linking to **this page**.
<br><br>             

### 🔑 Admin Commands

> **~clear `number of messages?`**

Clears a specified number of messages from a text channel. Using the command on its own will clear **all** messages<br>
**Requires**: `Manage Messages`

> **~blacklist | ~bladd `...words?`**

Allows the user to choose words to ban on the server with a dropdown menu.<br>
**Requires**: `Manage Messages`

❗ Optionally, you can type words after the command if you'd prefer not to use the dropdown.

> **~clearblacklist | ~blclear**

Clears the blacklist for the server.<br>
**Requires**: `Manage Messages`

> **~showblacklist | ~blshow**

Shows the blacklist for the server.<br>
**Requires**: `Manage Messages`

⚠️ Other users will be able to see the words on the list. Only use this in an admin/mod-only channel.

> **~blacklistremove | ~blrem `...words?`**

Allows the user to choose words to remove from the blacklist with a dropdown menu.<br>
**Requires**: `Manage Messages`

❗ Optionally, you can type words after the command if you'd prefer not to use the dropdown.

> **~kick `member` `reason?`**

Kicks a specified user from the server.<br>
**Requires**: `Kick Members`

> **~ban `member` `reason?`**

Bans a specified user from the server.<br>
**Requires**: `Ban Members`

> **~softban `member` `number of days` `reason?`**

Temporarily bans a specified user from the server.<br>
**Requires**: `Ban Members`

⚠️ It is **not** recommended to use this when self-hosting, unless your bot will be running 24/7.

> **~unban `member`**

Unbans a specified user from the server.<br>
**Requires**: `Ban Members`
<br><br>        

### 🔊 Music Commands

> **~connect** | **~join**

Joins the VC you're currently in.

💿 When you use `play`, the bot will join automatically before playing, so this isn't needed most of the time.

> **~play | ~p `song to search for`**

Searches YouTube for a song and then plays the top result.

> **~pause | ~ps**

Pauses the song currently playing if there is one.

> **~resume | ~r**

Resumes the song currently playing if there's one currently paused.

> **~skip | ~s**

Skips the song currently playing if there is one.

> **~queue | ~q | ~songs**

Shows a list of songs that are queued.

> **~nowplaying | ~np**

Shows the song currently playing if there is one.

> **~volume | ~vol `volume as a percentage`**

🎧 Tip: You can use this command to have finer control over volume - you can set the volume to 8.78, for instance.

Adjust the volume of the music player.

> **~stop | ~del**

Stops the music player and clears all existing songs from the queue.

⚠️ This command kicks the bot from the VC.
<br><br>    

### 🌟 Role Commands

> **~reactrole | ~crr `emoji` `@role` `message`**

Creates an embed that users can react to for a role.<br>
**Requires**: `Manage Roles`

> **~removereactrole | ~rrr `@role`**

Deletes all reaction role messages for a particular role.<br>
**Requires**: `Manage Roles`
<br><br>     

### 📒 Misc Commands

❓ Currently, we're testing out **[slash commands](https://support.discord.com/hc/en-us/articles/1500000368501-Slash-Commands-FAQ)** for this category.

> **~choose `...options`** or **/choose `...options`**

Randomly chooses an option from a list. Use quote marks "" around the options if they are longer than one word.

⚠️ `/choose` does not currently support choices with multiple words.

> **~meme** or **/meme**

Sends a random meme from Reddit.

> **~poll `yes/no question`** or **/poll `yes/no question`**

Creates a poll that users can react with yes or no to.<br>

> **~twitch `streamer name`** or **/twitch `streamer name`**

Gets information about a Twitch stream if the streamer is currently streaming.

> **~echo `text`** or **/echo `text`**

Repeats a message in a text channel.

> **~ping** or **/ping**

Shows your current ping/latency in milliseconds.

> **~youtube | ~yt `search term`** or **/youtube `search term`**

Searches YouTube for a video and sends you a link to it. You can choose to view it on YouTube or in Discord.
<br><br>  

### 💡 Info Commands

❓ Just like misc commands, we're also testing out **[slash commands](https://support.discord.com/hc/en-us/articles/1500000368501-Slash-Commands-FAQ)** for this category.

> **~joined `@member?`** or **/joined `@member?`**

Shows the join date of a member on a server. If no member is specified, it shows your join date.

> **~toprole `@member?`** or **/toprole `@member?`**

Shows a member's highest ranking role on a server. If no member is specified, it shows your top role.

> **~permissions | ~perms `@member?`** or **/permissions `@member?`**

Shows the permissions a member has on a server. If no member is specified, it shows your permissions.
<br><br>

## 🚀 Self Hosting
How to set up **BB.Bot** for self-hosting, step by step.<br>

⚠️ For **development** versions of the bot, the prefix is `'?'`. This is so that we don't get the main & dev versions mixed up!

* Click **[here](https://realpython.com/installing-python/)** for more information on **installing Python**.
* Click **[here](https://discordpy.readthedocs.io/en/stable/discord.html)** for more information on **setting up a Discord bot** using the **Discord Developer Portal**.
* Click **[here](https://dev.twitch.tv/docs/authentication/register-app)** for more information on **registering a Twitch API application**.
<br><br>

### 🔖 Prerequisites

* **Python** 3.10+<br>
* A **Discord API application with a Bot user**, with:<br>
    * **All** priveleged gateway intents
    * `Administrator` permissions
    * `bot` and `applications.commands` scopes.
* A registered **Twitch API application**.
<br><br>

### ⏳ Installing

1. Install a **.ZIP** from the **[releases](https://github.com/matthewflegg/bb-bot/releases)** page.<br>
3. **Extract it** to your preferred file location.<br>
4. **Create a file** in the **root directory** called `.env`. It should look like this:
```
TOKEN=<Your Discord Bot Token>
TEST_GUILD_ID=<Your Server's ID. This is optional>
TWITCH_CLIENT_ID=<Your Twitch Client ID>
TWITCH_CLIENT_SECRET=<Your Twitch Client Secret>
```

### 🔌 Running

##### 🐧 Linux/UNIX
* Go to the **root directory** and run `chmod +x scripts/start.sh`.
* Then **run the script** using `./scripts/start.sh`.

##### 🏠 Windows
* Press **Windows + X**.
* Choose **Windows PowerShell (Admin)**.
* Go to the **root directory** and run `Set-ExecutionPolicy Bypass`.
* Finally, **run** `.\scripts\start.ps1`.
