# Standalone Todo App
This is standalone Todo app source code. This source code can build to run on multiple operation systems like Windows, MacOS, Linux, Android and iOS.
How you can use and expand your feature. 
## Step 1: Fok or Clone Repository 
You can Fok to your own repository or clone to your local machine by run this command on terminal or powershell
```shell
git clone https://github.com/kuth-chi/flet-todo-with-sqlite.git
```
How to fok
![image](https://github.com/user-attachments/assets/06b1e4a9-0694-42ff-aa8d-08120712e1d5)

## Step 2: Create Python Development Environment or Virtual Environmnet
  1. Make sure Python3+ is installed on your machine
     - Using "Terminal" or "PowerShell"
       ```shell
        python --version
       ```
      Should be display "Python 3.xx.x"
     It mean you have installed Python. If not, you can [Download from HERE]("https://www.python.org/downloads/") 
  2. Create Python Virtual Environment:
     - Run command below on your "Terminals" or "PowerShell"
       ```shell
      python -m venv .venv
       ```
     - Activate virtual environment by command:
       ```shell
       .venv\Scripts\activate.ps1
       ```
       on Windows
  
       ```shell
       source venv/bin/activate
       ```
       on MacOS
  3. After Virtual Environment is activated
     - From the project directory
       Project:
       |--> .venv
       |--> app.py
       |--> requirements.txt
       |--> todo.db
     - You need to install project requirement libraries by run command below
       ```shell
        pip install -r requirements.txt
       ```
       wait until complete installation
       Let run command
       ```shell
       flet run -r --app.py
       ```

Enjoy continue developing !
