# ToDo App

This project is a simple to-do list application built with Python using the `flet` library for creating UI elements and `SQLite` for database management.

## Requirements

You will need the following dependencies listed in the `requirements.txt` file to successfully run the project:

- flet 0.20.2
- db-sqlite3 0.0.1

## Installation

1. Clone the project repository to your local computer:
    ```python
   git clone https://github.com/Dogherty/ToDoApp.git
2. Create and activate a virtual environment for the project:
    ```python
   python -m venv myenv
    source myenv/bin/activate

3. Open the project directory
    ```python
   cd ToDoList

4. Install the Python dependencies specified in requirements.txt:
	```python
	pip install -r requirements.txt

5. Run the application:
    ```python
   python todo.py


<strong>(Warning)</strong> If you encounter the error `Error in database connection and app initialization: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to obtain local issuer certificate (_ssl.c:1007)>`, follow these steps:

1. Import ssl library:
   ```python
   import flet as ft
   import sqlite3
   import ssl # import this library

2. Put the following string into second try\except block in `main`:
   ```python
   ssl._create_default_https_context = ssl._create_unverified_context # add this string
   conn = sqlite3.connect('todo.db')
   cursor = conn.cursor()
   ```
	This line of code bypasses the SSL certificate validation error by allowing connections to protected resources without requiring certificate validation.

This error occurs due to failed SSL certificate validation during initialization of the database and application connection. 

## Usage

1. Add a new task by typing the task name in the input field and pressing Enter or clicking the "+" button.
2. To mark a task as completed, check the checkbox next to the task name.
3. Edit a task by clicking the edit button (pencil icon) next to the task name. Make changes in the text field and click the check mark icon to save.
4. Delete a task by clicking the delete button (trash icon) next to the task name.
5. Use the tabs at the top to filter tasks by "all", "active", or "completed".

## Contributing
Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create your feature branch: git checkout -b ToDoApp.
3. Commit your changes: git commit -am 'Add some feature'.
4. Push to the branch: git push origin ToDoApp.
5. Submit a pull request.

## Image

<img src="https://i.imgur.com/auou5LN.jpeg" alt="Image" width="700" height="713">

