which python3

# If not, then install it
# 0 is for true, 1 is for false.
if [ $? -eq 1 ]
then
    read -r -p "Installing Python 3.10. Continue? [Y/n] " input
    
    case $input in
        [yY][eE][sS]|[yY])
                sudo apt update
                sudo apt install software-properties-common
                sudo add-apt-repository ppa:deadsnakes/ppa
                sudo apt update
                sudo apt install python3.10
                ;;
        [nN][oO]|[nN])
                echo "Exiting setup."
                exit 0
                ;;
        *)
                echo "Invalid input."
                exit 1
                ;;
    esac
fi

read -r -p "[Optional] Creating a virtualenv. Continue? [Y/n] " input
 
case $input in
    [yY][eE][sS]|[yY])
            python3 -m pip install virtualenv
            python3 -m venv venv
            . venv/bin/activate
            ;;
    [nN][oO]|[nN])
            echo "Skipping virtualenv creation."
            ;;
    *)
            echo "Invalid input."
            exit 1
            ;;
esac

pip install -r requirements.txt

clear
python3 main.py
