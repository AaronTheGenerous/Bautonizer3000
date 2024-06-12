
# Buttonizer3000
Buttonizer3000 is a Python-based automation tool for managing promotional buttons on articles on a webpage. 
It allows users to schedule tasks for adding or removing promotional images and links to articles at specified times.

## Features
Add promotional images and links to articles.
Remove promotional images from articles.
Schedule tasks to be executed at a future date and time.
Task scheduling uses a secondary script to periodically check and execute pending tasks.

## Installation
#### Prerequisites
Python 3.x
Pip (Python package installer)
Google Chrome
ChromeDriver
#### Clone the Repository

    git clone https://github.com/your-username/Buttonizer3000.git
    cd Buttonizer3000

#### Install Required Packages

    pip install -r requirements.txt

#### Setup ChromeDriver
Download the appropriate version of ChromeDriver for your Chrome version from here. Place the chromedriver.exe in the project directory.

## Usage
#### Running the GUI
The GUI allows you to schedule tasks for adding or removing promotional images and links.

    python main.py

#### Scheduling Tasks

 - Open the GUI. Choose the "Hinzufügen" (Add) or "Entfernen" (Remove) tab. 
 - Fill in the required details (e.g., article numbers, image URLs, dimensions). 
 - Select a date and time for the task. 
 - Click "Submit" to schedule the task.  
 - Scheduled tasks are saved in a file named scheduled_tasks.json.

#### Executing Scheduled Tasks
A separate script periodically checks and executes the scheduled tasks. 
This script should be run continuously or set up as a scheduled task in Task Scheduler.

    python exe_tasks.py

## Project Structure
Buttonizer3000/
├── main.py                 # Main GUI script
├── exe_tasks.py            # Script to execute scheduled tasks
├── selenium_script.py      # Contains the Selenium automation logic
├── requirements.txt        # Python dependencies
├── scheduled_tasks.json    # File to store scheduled tasks
├── README.md               # Project documentation
└── __init__.py             # To treat directories as packages
## Detailed File Descriptions
#### main.py
This script initializes the GUI for scheduling tasks. It allows users to input details for adding or removing promotional images and schedule the tasks.

#### exe_tasks.py
This script reads the scheduled_tasks.json file, checks if any tasks are due, and executes them using Selenium. It should be run continuously or at regular intervals using a task scheduler.

#### Buttonizer3000.py
Contains the main automation logic using Selenium WebDriver. It includes the definitions for SeleniumThread and other necessary functions to log in, add, or remove images and links from articles.

#### requirements.txt
Lists all the Python packages required to run the project. Use pip install -r requirements.txt to install the dependencies.

#### scheduled_tasks.json
Stores the scheduled tasks in JSON format. The tasks include details such as task type, schedule time, and article details.

## Setting Up Task Scheduler
#### To automatically run exe_tasks.py at regular intervals:

 - Open Task Scheduler.
 - Create a new basic task.
 - Set the trigger to run daily, every hour, or every minute, depending on how frequently you want to check for scheduled tasks.
 - Set the action to start a program and point it to your Python executable with exe_tasks.py as the argument.
 - Save the task.

## Contributing

 - List item
 - Fork the repository.
 - Create a new branch (git checkout -b feature-branch).
 - Make your changes.
 - Commit your changes (git commit -m 'Add new feature').
 - Push to the branch (git push origin feature-branch).
 - Create a new Pull Request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements
Selenium
PyQt5
