# Beep Boop Bot
Beep Boop Bot is provided under the GNU General Public License 3.0. This means you can run, share, study and modify the software as you wish. While you don't technically have to, if you use the souce code for this bot credit would be appreciated.

## Contents

1. [Self Hosting] (#Self Hosting)
2. [Commands List] (#Commands List)

## Self Hosting

### Pre-requisites

##### Install Python 3.9.7+ 
**Windows**:
https://www.python.org/downloads/

**Linux**:
1. Install development packages
Debian:
<pre>$ sudo apt update
$ sudo apt install build-essential zlib1g-dev \
libncurses5-dev libgdbm-dev libnss3-dev \
libssl-dev libreadline-dev libffi-dev curl</pre>
Fedora:
<pre>$ sudo dnf groupinstall development</pre>
2. Download the latest version of Python 3 as a .tar.gz
https://www.python.org/downloads/release/python-3102/
3. Extract the tarball using the extractor of your choice
<pre>$ tar -xf Python-3.?.?.tar.xz</pre>
4. Configure the script
<pre>$ cd Python-3.*
./configure</pre>
5. Start the build process
If you're installing Python for the first time:
<pre>$ sudo make altinstall</pre>
If you're replacing an existing installation:
Use your package manager to uninstall Python
<pre>$ sudo make install</pre>
6. Verify the install
Try:
<pre>python3 --version</pre>
Alternatively, you can run:
<pre>python --version</pre>



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

## Setup - Python

