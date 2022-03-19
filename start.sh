#Check if Python is installed
which python3

#If not, then install it
if [ $? -eq 0 ]
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

python3 -m venv venv
cd venv

Scripts/activate

pip install -r requirements.txt
python3 start.py