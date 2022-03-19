<p align="center">
  <img src="https://live.staticflickr.com/65535/51937767187_4b2929a455_c.jpg">
</p>
<h1 align="center">🤖 BB.Bot</h1>
<h3 align="center">🔒 Moderation | 🎵 HQ Music Streaming | 📖 Memes | ⭐ Reaction Roles | ❓ Polls</h3>
<h4 align="center">Powered by Nextcord and GCP, BB.Bot is the bot for you.</h4>
<br>

<p align="center">
  <img src="https://img.shields.io/github/v/release/matthewflegg/beepboop?include_prereleases&label=Latest%20Version&style=social">
  <img src="https://img.shields.io/github/v/release/matthewflegg/beepboop?label=Latest%20Stable%20Version&style=social">
</p>
<br>

**BB.Bot** is a Discord bot powered by **Python** and GCP's **Compute Engine**. Featuring **24/7 uptime**, **HQ music streaming**, **admin commands**, and more, **BB.Bot** is the bot for you. **Available for free** and **regularly maintained**, our bot comes with **no additional costs** and **long-term support**.

* Click **[Here](https://discord.com/api/oauth2/authorize?client_id=947593856839458916&permissions=8&scope=bot)** to invite BB.Bot to your server.
* Click **[Here](https://discord.gg/Dacy34eM)** to join our Discord server.
<br><br>

## 📢 **Commands List**

### 🧭 Contents

* **[Help Commands](#-help-commands)**
* **[Admin Commands](#-admin-commands)**
* **[Music Commands](#-music-commands)**
* **[Role Commands](#-role-commands)**
* **[Misc Commands](#-misc-commands)**
<br><br>  

### 🔖 Help Commands

> **~help**

Sends an embed linking to **this page**.
<br><br>             

### 🔑 Admin Commands

> **~clear `number of messages`**

Clears a specified number of messages from a text channel.<br>
**Requires**: `Manage Messages`

> **~blacklist | ~bladd `word`**

Adds the word to a list of words that are disallowed. Any messages containing these words will be deleted.<br>
**Requires**: `Manage Messages`

> **~clearblacklist | ~blclear**

Clears the blacklist for the server.<br>
**Requires**: `Manage Messages`

> **~kick `member` `reason?`**

Kicks a specified user from the server.<br>
**Requires**: `Kick Members`

> **~ban `member` `reason?`**

Bans a specified user from the server.<br>
**Requires**: `Ban Members`

> **~softban `member` `number of days` `reason?`**

Temporarily bans a specified user from the server.<br>
**Requires**: `Ban Members`

> **~unban `member`**

Unbans a specified user from the server.<br>
**Requires**: `Ban Members`
<br><br>        

### 🔊 Music Commands

> **~connect** | **~join**

Joins the VC you're currently in. When you use `play`, the bot will join automatically before playing.

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

Adjust the volume of the music player.

> **~stop | ~del**

Stops the music player and clears all existing songs from the queue.
<br><br>    

### 🌟 Role Commands

> **~reactrole | ~crr `emoji` `@role` `message`**

Creates an embed that users can react to for a role.
**Requires**: `Manage Roles`

> **~removereactrole | ~rrr `@role`**

Deletes all reaction role messages for a particular role.
**Requires**: `Manage Roles`
<br><br>     

### 📒 Misc Commands

> **~choose `option a` `option b` `option c?` `...`**

Randomly chooses an option from a list. Use quote marks "" around the options if they are longer than one word.

> **~meme**

Sends a random meme from Reddit.

> **~poll `yes/no question`**

Creates a poll that users can react with yes or no to. 
