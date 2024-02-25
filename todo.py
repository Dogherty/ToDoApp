import flet as ft
import sqlite3

class Task(ft.UserControl):
    """
    Represents a task in the to-do list.

    Attributes:
        task_id (int): The unique identifier for the task.
        task_name (str): The name of the task.
        completed (bool): The status of the task, whether it's completed or not.
        task_status_change (callable): A callback function to handle status change of the task.
        task_delete (callable): A callback function to handle deletion of the task.
        display_task (ft.Checkbox): The UI element representing the task.
        edit_name (ft.TextField): The UI element for editing the task name.
        display_view (ft.Row): The UI element for displaying the task.
        edit_view (ft.Row): The UI element for editing the task name.
    """
    def __init__(self, task_id, task_name, task_status_change, task_delete):
        """
        Initializes a Task object with the given parameters.
        """
        super().__init__()
        self.task_id = task_id
        self.completed = False
        self.task_name = task_name
        self.task_status_change = task_status_change
        self.task_delete = task_delete
        self.display_task = None

    def build(self):
        """
        Builds the UI elements for displaying and editing the task.
        """
        try:
            # Create or update UI elements based on task state
            if self.display_task is None:
                self.display_task = ft.Checkbox(
                    value=False, label=self.task_name, on_change=self.status_changed
                )
            else:
                self.display_task.label = self.task_name

            self.edit_name = ft.TextField(expand=1)

            # Create UI for displaying task and editing task name
            self.display_view = ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self.display_task,
                    ft.Row(
                        spacing=0,
                        controls=[
                            ft.IconButton(
                                icon=ft.icons.CREATE_OUTLINED,
                                tooltip="Edit To-Do",
                                on_click=self.edit_task,
                            ),
                            ft.IconButton(
                                ft.icons.DELETE_OUTLINE,
                                tooltip="Delete To-Do",
                                on_click=self.delete_task,
                            ),
                        ],
                    ),
                ],
            )

            self.edit_view = ft.Row(
                visible=False,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self.edit_name,
                    ft.IconButton(
                        icon=ft.icons.DONE_OUTLINE_OUTLINED,
                        icon_color=ft.colors.GREEN,
                        tooltip="Update To-Do",
                        on_click=self.save_task,
                    ),
                ],
            )
            return ft.Column(controls=[self.display_view, self.edit_view])
        except Exception as e:
            print(f"Error in Task build(): {e}")

    async def edit_task(self, e):
        """
        Handles the event when the edit button is clicked.
        """
        try:
            # Display the edit UI and hide the display UI
            self.edit_name.value = self.display_task.label
            self.display_view.visible = False
            self.edit_view.visible = True
            await self.update_async()
        except Exception as e:
            print(f"Error in edit_task(): {e}")

    async def save_task(self, e):
        """
        Handles the event when the save button is clicked.
        """
        try:
            # Save changes to the task name, update UI, and commit changes to the database
            self.display_task.label = self.edit_name.value
            self.display_view.visible = True
            self.edit_view.visible = False
            cursor.execute("UPDATE tasks SET task_name=? WHERE id=?", (self.edit_name.value, self.task_id))
            conn.commit()
            await self.update_async()
        except Exception as e:
            print(f"Error in save_task(): {e}")

    async def status_changed(self, e):
        """
        Handles the event when the status of the task is changed.
        """
        try:
            # Update task completion status, update UI, and commit changes to the database
            self.completed = self.display_task.value
            await self.task_status_change(self)

            cursor.execute("UPDATE tasks SET completed=? WHERE id=?", (1 if self.completed else 0, self.task_id))
            conn.commit()
        except Exception as e:
            print(f"Error in status_changed(): {e}")

    async def delete_task(self, e):
        """
        Handles the event when the delete button is clicked.
        """
        try:
            # Delete the task from UI and database, then update UI
            await self.task_delete(self)
            cursor.execute("DELETE FROM tasks WHERE id=?", (self.task_id,))
            conn.commit()
        except Exception as e:
            print(f"Error in delete_task(): {e}")


class TodoApp(ft.UserControl):
    """
    Represents the to-do list application.

    Attributes:
        new_task (ft.TextField): The UI element for adding new tasks.
        tasks (ft.Column): The UI element for displaying the list of tasks.
        filter (ft.Tabs): The UI element for filtering tasks.
        items_left (ft.Text): The UI element for displaying the count of active items left.
    """
    def build(self):
        """
        Builds the UI elements for the to-do list application.
        """
        try:
            # Create UI elements for the to-do list
            self.new_task = ft.TextField(
                hint_text="What needs to be done?", on_submit=self.add_task, expand=True
            )
            self.tasks = ft.Column()

            self.filter = ft.Tabs(
                scrollable=False,
                selected_index=0,
                on_change=self.tabs_changed,
                tabs=[ft.Tab(text="all"), ft.Tab(text="active"), ft.Tab(text="completed")],
            )

            # Load existing tasks from the database and update UI
            self.load_tasks()
            cursor.execute("SELECT * FROM tasks WHERE completed=0")
            comp = cursor.fetchall()
            self.items_left = ft.Text(f"{len(comp)} active item(s) left")

            return ft.Column(
                width=600,
                controls=[
                    ft.Row(
                        [ft.Text(value="Todos", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM)],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        [ft.Text(value="Hello, cute! Your task list:", theme_style=ft.TextThemeStyle.BODY_LARGE)],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        controls=[
                            self.new_task,
                            ft.FloatingActionButton(
                                icon=ft.icons.ADD, on_click=self.add_task
                            ),
                        ],
                    ),
                    ft.Column(
                        spacing=25,
                        controls=[
                            self.filter,
                            self.tasks,
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    self.items_left,
                                    ft.OutlinedButton(
                                        text="Clear completed", on_click=self.clear_task
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            )
        except Exception as e:
            print(f"Error in TodoApp build(): {e}")

    def load_tasks(self):
        """
        Loads tasks from the database and adds them to the task list.
        """
        try:
            cursor.execute("SELECT * FROM tasks")
            rows = cursor.fetchall()
            for row in rows:
                task_id, task_name, completed = row
                task = Task(task_id, task_name, self.task_status_change, self.task_delete)
                task.completed = bool(completed)

                task.build()

                task.display_task.value = bool(completed) if task.display_task else False
                self.tasks.controls.append(task)
        except Exception as e:
            print(f"Error in load_tasks(): {e}")

    async def add_task(self, e):
        """
        Handles the event when a new task is added.
        """
        try:
            if self.new_task.value:
                cursor.execute("INSERT INTO tasks (task_name, completed) VALUES (?, ?)", (self.new_task.value, 0))
                conn.commit()

                task_id = cursor.lastrowid
                task = Task(task_id, self.new_task.value, self.task_status_change, self.task_delete)
                self.tasks.controls.append(task)
                self.new_task.value = ""
                await self.new_task.focus_async()
                await self.update_async()
        except Exception as e:
            print(f"Error in add_task(): {e}")

    async def task_status_change(self, task):
        """
        Handles the event when the status of a task is changed.
        """
        try:
            await self.update_async()
        except Exception as e:
            print(f"Error in task_status_change(): {e}")

    async def task_delete(self, task):
        """
        Handles the event when a task is deleted.
        """
        try:
            self.tasks.controls.remove(task)
            await self.update_async()
            cursor.execute("DELETE FROM tasks WHERE id=?", (task.task_id,))
            conn.commit()
        except Exception as e:
            print(f"Error in task_delete(): {e}")

    async def tabs_changed(self, e):
        """
        Handles the event when the filter tab is changed.
        """
        try:
            await self.update_async()
        except Exception as e:
            print(f"Error in tabs_changed(): {e}")

    async def clear_task(self, e):
        """
        Handles the event when the clear completed button is clicked.
        """
        try:
            for task in self.tasks.controls[:]:
                if task.completed:
                    await self.task_delete(task)
        except Exception as e:
            print(f"Error in clear_task(): {e}")

    async def update_async(self):
        """
        Updates the task list based on the filter tab.
        """
        try:
            status = self.filter.tabs[self.filter.selected_index].text
            count = 0
            for task in self.tasks.controls:
                task.visible = (
                    status == "all"
                    or (status == "active" and not task.completed)
                    or (status == "completed" and task.completed)
                )
                if not task.completed:
                    count += 1
            self.items_left.value = f"{count} active item(s) left"
            await super().update_async()
        except Exception as e:
            print(f"Error in update_async(): {e}")

async def main(page: ft.Page):
    """
    Initializes the to-do list application.

    Args:
        page: The page to add the application to.
    """
    try:
        page.title = "ToDo App"
        page.window_width = '600'
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.scroll = ft.ScrollMode.ADAPTIVE
        await page.add_async(TodoApp())
    except Exception as e:
        print(f"Error in main(): {e}")

try:
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY,
                        task_name TEXT,
                        completed INTEGER
                    )''')
    conn.commit()
    ft.app(main)
except Exception as e:
    print(f"Error in database connection and app initialization: {e}")
