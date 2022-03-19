:: Checking for a Python Installation
python --version > NUL

IF errorlevel 1 GOTO noPython

:: If the code reaches here then Python is installed
py -m venv venv
cd venv

Scripts\activate

pip install -r requirements.txt
py start.py

EXIT

:: If the code reaches here, Python is not installed
:noPython

echo "Python is not installed."
echo "Please install Python before continuing."