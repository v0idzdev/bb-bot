:: Checking for a Python Installation
python --version > NUL

IF errorlevel 1 GOTO noPython

:: If the code reaches here then Python is installed
py -m venv venv
:: cd'ing into venv/ directory should throw No Such File As requirements.txt

venv\Scripts\activate

pip install -r requirements.txt
py main.py

EXIT

:: If the code reaches here, Python is not installed
:noPython

echo "Python is not installed."
echo "Please install Python before continuing."