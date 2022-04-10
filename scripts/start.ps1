$yes = New-Object System.Management.Automation.Host.ChoiceDescription "&Yes", "Description."
$cancel = New-Object System.Management.Automation.Host.ChoiceDescription "&Cancel", "Description."
$options = [System.Management.Automation.Host.ChoiceDescription[]]($yes, $cancel)

$title = "Would you like to install Python?"
$message = "Choose Yes to continue. Choose No to exit."
$result = $host.ui.PromptForChoice($title, $message, $options, 1)

switch ($result) {
    0 {
        Write-Host "Installing Python 3.10..."
        Set-ExecutionPolicy Bypass -Scope Process -Force;
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072;
        Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
        choco install python
    } 
    
    1 {
        Write-Host "Exiting setup."
        Exit
    }
}

$title = "[Optional] Creating a virtualenv. Continue?"
$message = "Choose Yes to create a virtualenv. Choose No to continue with installation."
$result = $host.ui.PromptForChoice($title, $message, $options, 1)

switch ($result) {
    0 {
        py -m pip install virtualenv
        py -m venv venv
        . venv\Scripts\activate.bat
    } 
    
    1 {
        Write-Host "Skipping virtualenv creation."
    }
}

py -m pip install python-dotenv
py -m pip install -r requirements.txt

py main.py
