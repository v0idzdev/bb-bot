# Check if Python is installed
which python3


# If not, then install it
# 0 is for true, 1 is for false.
if [ $? -eq 1 ]
then
    echo "Python 3 is not installed. Installing now."
    sudo apt update
    sudo apt install software-properties-common
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt update
    sudo apt install python3.10
fi

#Configure project
pip install virtualenv
python3.10 -m venv venv

# activating virtual env
. venv/bin/activate

# installing dependencies
pip install -U -r requirements.txt

clear
# starting script
python3 main.py
