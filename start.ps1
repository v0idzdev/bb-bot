# Install chocolatey, a package manager for Windows.
# This code is copy-pasted from https://docs.chocolatey.org/en-us/choco/setup.
Set-ExecutionPolicy Bypass -Scope Process -Force;

[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072;
Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install Python 3.10.x
choco install python

# Configure project
py -m pip install virtualenv
py -m venv venv

# Activating virtual environment
. venv\Scripts\activate.bat

# Installing dependencies
py -m pip install python-dotenv
py -m pip install -r requirements.txt

# Starting script
py main.py