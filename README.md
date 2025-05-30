# Python To-Do List Application

A modern and aesthetic desktop To-Do List application built with Python and Tkinter. This application helps you manage your tasks efficiently with features like task prioritization, completion tracking, and persistent storage.

## Features

* **Add Tasks:** Quickly add new tasks to your list.
* **Edit Tasks:** Modify the description of existing tasks.
* **Remove Tasks:** Delete individual tasks.
* **Mark as Complete/Incomplete:** Toggle the completion status of tasks by clicking on them. Completed tasks are visually distinguished (strikethrough and different color).
* **Task Prioritization:** Assign 'High', 'Medium', or 'Low' priority to tasks.
    * Priority is displayed alongside the task.
* **Clear Completed Tasks:** Remove all completed tasks at once.
* **Persistent Storage:** Tasks are automatically saved to a `todo_tasks.json` file and reloaded when the app starts.
* **Modern UI:**
    * Clean and visually appealing interface with a defined color palette.
    * Uses "Segoe UI" font (falls back to "Arial").
    * Unicode icons for buttons.
    * Status bar for feedback and task counts.
* **Cross-Platform:** Built with Tkinter, which is part of Python's standard library, making it generally cross-platform. `ttk` theming is used to enhance the look on different OS.

## How to Run

1.  **Prerequisites:**
    * Python 3 installed on your system.
    * Tkinter (usually comes with Python standard installations. If not, you might need to install it separately, e.g., `sudo apt-get install python3-tk`).

2.  **Clone the repository (or download the Python file):**
    ```bash
    git clone <your-repository-url>
    cd <repository-directory>
    ```
    Or simply download the `.py` file.

3.  **Run the application:**
    ```bash
    python3 your_todo_app_filename.py
    ```
    (Replace `your_todo_app_filename.py` with the actual name of your Python script).

4.  A `todo_tasks.json` file will be created in the same directory to store your tasks.

## Technologies Used

* **Python 3:** Core programming language.
* **Tkinter:** Python's standard GUI (Graphical User Interface) package, used for creating the desktop application interface.
* **`tkinter.ttk`:** Themed Tkinter widgets for a more modern look (e.g., for the scrollbar and combobox).
* **JSON:** For saving and loading tasks to/from a local file.

## Code Structure Overview

* **`TodoApp` Class:** Encapsulates all the application logic and UI setup.
    * `__init__(self, root)`: Initializes the main window, fonts, tasks list, sets up the UI, loads tasks, and handles window closing.
    * `get_priority_display(self, priority_level)`: Helper to get display text and color for priorities.
    * `setup_ui(self)`: Creates and arranges all the GUI widgets (title, input field, buttons, listbox, status bar).
    * `refresh_task_list(self)`: Updates the listbox display based on the current `self.tasks` list.
    * `add_task(self)`: Adds a new task.
    * `toggle_task_complete_click(self, event)`: Handles marking tasks as complete/incomplete via listbox click.
    * `edit_task(self)`: Allows editing the selected task's description.
    * `set_task_priority(self)`: Opens a dialog to set the priority for the selected task.
    * `remove_task(self)`: Removes the selected task.
    * `remove_completed_tasks(self)`: Deletes all tasks marked as completed.
    * `update_status_bar(self)`: Updates the status bar with task counts.
    * `save_tasks(self)`: Saves the current tasks to `todo_tasks.json`.
    * `load_tasks(self)`: Loads tasks from `todo_tasks.json` on startup.
    * `on_closing(self)`: Ensures tasks are saved when the application window is closed.

## Future Enhancements (Ideas)

* **Task Sorting:** Allow sorting tasks by priority, due date, or alphabetically.
* **Due Dates:** Add functionality to set and display due dates for tasks.
* **Reminders/Notifications:** Implement desktop notifications for upcoming or overdue tasks.
* **Sub-tasks:** Allow creating nested tasks.
* **Themes:** Add options for users to choose different color themes.
* **Advanced Search/Filter:** Implement more robust ways to find specific tasks.
* **Drag and Drop Reordering:** Allow users to reorder tasks using drag and drop.
* **Keyboard Shortcuts:** Add more keyboard shortcuts for common actions.
