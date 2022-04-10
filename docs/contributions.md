# 🚀 Contribution Guide

This guide assumes you know how to **use pip** from the command line, create and self-host **Discord bots**, and have experience with creating **forks**, **cloning repositories** and submitting **pull requests**.
<br><br>

## 📢 Guidelines

⚠️ For **development** versions of the bot, the prefix is `'?'`. This is so that we don't get the main & dev versions mixed up!

1. **Fork** this repository and **clone** your fork to your local machine.
3. Install dependencies by running `pip install -r requirements.txt`.
	- Optionally, you can run this from a **[virtual environment](https://docs.python.org/3/library/venv.html)**, which is recommended.
	- Please avoid using **pipenv**.
4. Make some changes.
	- Only make changes on the **dev** branch.
	 - You can create other branches and merge them into **dev**, if you choose to.
	 - When creating branches, it is recommended to create them from **dev**.
	 - Any pull requests where **master** has been changed will **be rejected**.
5. When you've finished making changes, submit a pull request from **your dev branch** into **dev**.
	- Try to add a few bullet points about what you've changed.
	- Keep the title concise, if possible.

👋🏻 Good luck! Join our **[Discord server](https://discord.gg/nNtGYsq3)** to propose features, report bugs, and talk to other developers.<br><br>

## ❗ Do's & Dont's

- ❌ ***Don't*** make changes to the **master** branch. This branch is for **stable**, **tested** releases only.
- ❌ ***Don't*** change too many things at once per pull request. Please try to keep it simple.
- ❌ ***Don't*** add any tags to your commits. These might get confused with tags on **origin**. 
- ✔️ ***Do*** try to follow the code style that is used throughout the project.
	- *Some files may have different code styles*. Try and stick to the code style of the file.
	- Comments are appreciated, but not 100% necessary.
- ✔️ ***Do*** test code as you write it. If there are any errors that **can't** be fixed, mention them in your **pull request**.



