![Latest Version](https://img.shields.io/github/v/release/matthewflegg/beepboop?include_prereleases&label=Latest%20Version&style=social)
![Latest Stable Version](https://img.shields.io/github/v/release/matthewflegg/beepboop?label=Latest%20Stable%20Version&style=social)

# Beep Boop Bot Documentation
**Welcome to the official documentation for Beep Boop Bot.**

This page refers to the **pre-release** version of Beep Boop Bot `V1.X.X`. If you're looking for the documentation for the version that is **currently online** `v0.1.3`, you'll find it in the **README.md** on the **main** branch. 

## Commands List

### Help Commands

> **~help**

Sends an embed linking to **this page**.<br>

### Admin/Moderator Commands

> **~clear `number of messages`**

Clears a specified number of messages from a text channel.<br>
**Requires**: `Manage Messages`

> **~blacklist `word`**

Adds the word to a list of words that are disallowed. Any messages containing these words will be deleted.<br>
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

### Music Commands

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

### Misc Commands

> **~choose `option a` `option b` `option c?` `...`**

Randomly chooses an option from a list. Use quote marks "" around the options if they are longer than one word.

> **~meme**

Sends a random meme from Reddit.

> **~poll `yes/no question`**

Creates a poll that users can react with yes or no to. 
