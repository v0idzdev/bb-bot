# Beep Boop Bot
Beep Boop Bot is provided under the GNU General Public License 3.0. This means you can run, share, study and modify the software as you wish. While you don't technically have to, if you use the souce code for this bot credit would be appreciated.

## Contents

1. **[Self Hosting](#SelfHosting)**
  * [Pre-requisites](#Pre-requisites)
2. **[Commands List](#CommandsList)**
  * [Help / Docs](#Help/Docs)
  * [Admin](#Admin)
  * [Greetings](#Greetings)
  * [Miscellaneous](#Miscellaneous)

## Self Hosting

### Pre-requisites

* An installation of Python 3.9.7+ | Windows: https://phoenixnap.com/kb/how-to-install-python-3-windows | Linux: https://opensource.com/article/20/4/install-python-linux        
* A bot token, using the Discord Developer Portal - Follow **step 1** only: https://www.digitalocean.com/community/tutorials/how-to-build-a-discord-bot-with-node-js     

Install dependencies by running:
<pre>pip install -r requirements.txt</pre>

### Setting Up the Bot For Self-Hosting

1. Run the following in cmd.exe or a bash terminal to verify your Python installation:
<pre>python --version</pre>
Alternatively, run:
<pre>python3 --version</pre>
2. Ensure you have a copy of your bot's token
3. Download the repository as a .zip
4. Unzip the .zip file
5. Navigate to the root directory: "./beepboop/
6. Create a file called ".env". Enter:
<pre>"TOKEN=[your_token]"</pre>
where [your_token] is your bot's token
7. Open cmd.exe or a bash terminal. Run:
<pre>python3 [path/to/root/directory]/app.py</pre>
Example:
<pre>python3 C:\\Users\\Username\\Documents\\beepboop\\app.py</pre>
Or:
<pre>python3 usr/files/beepboop.py</pre>
Alternatively, you can use the cd command to use cmd.exe or a bash terminal from within the root directory
8. Done!

## Commands List

### Help / Docs
Commands for help and documentation

##### .docs
Sends an embed linking to this page
<pre>Usage: .docs</pre>

##### .help
Displays the default help message, showing all the commands. The official documentation (this page) is recommended, however, as it's a lot more helpful
<pre>Usage: .help</pre>

### Admin
Commands for administrators, mods, etc.

##### .ban
Bans a user from a server. Requires the 'Ban members' permission
<pre>Usage: .ban [discord user to ban] [reason (optional)]</pre>

##### .kick
Kicks a user from a server. Requires the 'Kick members' permission
<pre>Usage: .kick [discord user to kick] [reason (optional)]</pre>

##### .restrict
Assigns a role called 'Restrict' to a user. This role must exist on the server already - you can configure the restrictions however you'd like. Requires 'Manage roles' permission
<pre>Usage: .restrict [discord user to restrict] [duration in seconds]</pre>

### Greetings
Greeting related commands

##### .hello
Replies with hello to the user of the command. Replies with hello again if used twice in a row
<pre>Usage: .hello -> Beep Boop Bot: "Hello [user]!"</pre>
Alternatively, if you use it twice in a row:
<pre>-> Beep Boop Bot: "Hello again, [user]"</pre>

The greetings category also contains an event listener that mentions a user with a welcome message when they join a server. Currently, the welcome message is not customisable. However, this feature will be added

### Miscellaneous
Misc. commands for doing dumb stuff

##### .choose
Chooses a random option from a list.
<pre>Usage: .choose a b c -> Beep Boop Bot: "a"</pre>
If you're using more than one word as an option, use "" so the bot knows where one option starts and another ends
<pre>Usage: .choose "option a" "option b" "option c" -> Beep Boop Bot: option c</pre>

##### .russianroulette
Has a 1 in 6 chance of kicking the user
<pre>Usage: .russianroulette -> (NO KICK) Beep Boop Bot: "You were lucky... This time ;)"</pre>
If the user was unlucky and got kicked:
<pre>-> (KICK) Beep Boop Bot: "Oops... You lost"</pre>

##### .beep
Beep Boop Bot replies with "boop"
<pre>Usage: .beep</pre>
