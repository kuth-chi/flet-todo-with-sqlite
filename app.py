import sqlite3 as sqlite
import flet as ft
from datetime import datetime

# Create form for creating new task
# Create Database connection this case we use SQLite3
class Database:
    def __init__(self):
        self.db = None

    def connect_to_db(self):
        try:
            self.db = sqlite.connect("todo.db")
            c = self.db.cursor()
            c.execute(
                "CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, task VARCHAR(255) NOT NULL, date VARCHAR(50) NOT NULL)"
            )
            print("Database connected and table ensured.")
        except sqlite.DatabaseError as e:
            print("Error: Database not found")
            print(e)

    def read_db(self):
        """ Read data from database """
        c = self.db.cursor()
        c.execute("SELECT task, date FROM tasks")
        rows = c.fetchall()
        print(f"Read from database: {rows}")
        return rows

    def insert_db(self, values):
        """ Insert new task into database """
        c = self.db.cursor()
        c.execute("INSERT INTO tasks (task, date) VALUES (?, ?)", values)
        self.db.commit()
        print(f"Inserted into database: {values}")

    def delete_db(self, value):
        """ Delete task from database """
        c = self.db.cursor()
        c.execute("DELETE FROM tasks WHERE task=?", value)
        self.db.commit()
        print(f"Deleted from database: {value}")

    def update_db(self, value):
        """ Update task in database """
        c = self.db.cursor()
        c.execute("UPDATE tasks SET task=? WHERE task=?", value)
        self.db.commit()
        print(f"Updated in database: {value}")

    def close_db(self):
        """ Close connection to database """
        if self.db:
            self.db.close()
            print("Database connection closed.")


class FormContainer(ft.Container):
    """ Create form for creating new task """

    def __init__(self, func):
        self.func = func
        super().__init__()

        self.text_field = ft.TextField(
            label="New task",
            height=58,
            width=255,
            color=ft.colors.BLACK,
            border_color=ft.colors.BLUE_GREY_100,
            hint_style=ft.TextStyle(color=ft.colors.BLUE_GREY_100, size=12),
        )

        self.add_button = ft.IconButton(
            content=ft.Text("Add task"),
            width=180,
            height=44,
            on_click=self.func,
            style=ft.ButtonStyle(
                color=ft.colors.BLACK12,
                bgcolor={"": ft.colors.BLACK},
                shape={"": ft.RoundedRectangleBorder(radius=8)},
            ),
        )

        self.form_column = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[self.text_field, self.add_button],
        )

        self.content = self.form_column
        self.width = 280
        self.height = 80
        self.bgcolor = ft.colors.BLUE_GREY_500
        self.opacity = 0  # change value to 1 for 100% opacity
        self.border_radius = ft.border_radius.all(40)
        self.margin = ft.margin.only(left=-20, right=-20)
        self.animate = ft.animation.Animation(400, ft.AnimationCurve.DECELERATE)
        self.animate_opacity = 200
        self.padding = ft.padding.only(top=45, bottom=45)


# Class to create new task by user
class CreateTask(ft.Container):
    """ Class to create new task by user """

    def __init__(self, task: str, date: str, func1, func2):
        self.task = task
        self.date = date
        self.func1 = func1
        self.func2 = func2
        super().__init__()

        self.width = 280
        self.height = 64
        self.border = ft.border.all(0.85, ft.colors.WHITE54)
        self.border_radius = ft.border_radius.all(8)
        self.on_hover = self.hover_show_icon
        self.clip_behavior = ft.ClipBehavior.HARD_EDGE
        self.padding = ft.padding.all(10)
        self.content = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Column(
                    spacing=1,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Text(value=self.task, size=12),
                        ft.Text(value=self.date, size=9, color=ft.colors.WHITE54),
                    ]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=0,
                    controls=[
                        self.task_delete_edit(ft.icons.DELETE_ROUNDED, ft.colors.RED_500, self.func1),
                        self.task_delete_edit(ft.icons.EDIT_ROUNDED, ft.colors.WHITE70, self.func2)
                    ],
                )
            ]
        )

    def task_delete_edit(self, name: str, color: str, func):
        return ft.IconButton(
            icon=name,
            icon_size=18,
            icon_color=color,
            opacity=0,
            animate_opacity=200,
            on_click=lambda e: func(self),
        )

    def hover_show_icon(self, e):
        """ Show icon while hovering over task """
        if e.data == "true":
            e.control.content.controls[1].controls[0].opacity = 1
            e.control.content.controls[1].controls[1].opacity = 1
            e.control.content.update()
        else:
            e.control.content.controls[1].controls[0].opacity = 0
            e.control.content.controls[1].controls[1].opacity = 0
            e.control.content.update()


def main(page: ft.Page):
    """ Main flet app"""
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.CrossAxisAlignment.CENTER

    def add_task_to_screen(e):
        task_created_date = datetime.now().strftime("%b %d, %Y, %H:%M ")
        db = Database()
        db.connect_to_db()
        
        task_value = form.text_field.value
        print(f"Task value: {task_value}, Date: {task_created_date}")
        
        if task_value:
            db.insert_db((task_value, task_created_date))
            db.close_db()

            __main_column__.controls.append(
                CreateTask(
                    task_value,  
                    task_created_date,  
                    delete_function,
                    update_function,
                )
            )
            __main_column__.update()
            create_to_do_task(e)
        else:
            db.close_db()

    def delete_function(e):
        __main_column__.controls.remove(e)
        __main_column__.update()

    def update_function(e):
        form.height, form.opacity = 200, 1
        form.text_field.value = e.task  # Update the text field with task value
        form.add_button.content.value = "Update"
        form.add_button.on_click = lambda _: finalize_update(e)
        form.update()

    def finalize_update(e):
        """
        - Update task value
        - Update date if needed
        """
        e.task = form.text_field.value  
        e.date = datetime.now().strftime("%b %d, %Y, %H:%M ")  
        
        # Update the displayed task and date in the UI
        e.content.controls[0].controls[0].value = e.task
        e.content.controls[0].controls[1].value = e.date

        e.content.update()  # Update the UI to reflect changes
        create_to_do_task(e)  # Optional: perform any additional actions after update


    def create_to_do_task(e):
        if form.height != 200:
            form.height, form.opacity = 200, 1
            form.update()
        else:
            form.height, form.opacity = 80, 0
            form.text_field.value = None
            form.add_button.content.value = "Add task"
            form.add_button.on_click = lambda _: add_task_to_screen(e)
            form.update()

    __main_column__ = ft.Column(
        scroll=ft.ScrollMode.HIDDEN,
        expand=True,
        alignment=ft.MainAxisAlignment.START,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text(
                        "Todo List",
                        color=ft.colors.BLUE_50,
                        size=18,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.IconButton(
                        icon=ft.icons.ADD_CIRCLE_ROUNDED,
                        icon_size=18,
                        on_click=create_to_do_task
                    ),
                ]
            ),
            ft.Divider(
                height=8,
                color=ft.colors.WHITE24,
            ),
        ],
    )

    page.add(
        ft.Container(
            width=1500,
            height=1024,
            bgcolor=ft.colors.BLUE_GREY_900,
            margin=10,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        width=280,
                        height=600,
                        bgcolor="#0f0f0f",
                        border_radius=ft.border_radius.all(40),
                        border=ft.border.all(0.5, ft.colors.WHITE),
                        padding=ft.padding.only(top=35, left=20, right=20),
                        clip_behavior=ft.ClipBehavior.HARD_EDGE,
                        content=ft.Column(
                            alignment=ft.MainAxisAlignment.CENTER,
                            expand=True,
                            controls=[
                                __main_column__,
                                FormContainer(add_task_to_screen),
                            ]
                        )
                    )
                ]
            ),
        )
    )

    page.update()
    form = page.controls[0].content.controls[0].content.controls[1]

    # Load existing tasks from the database
    db = Database()
    db.connect_to_db()
    tasks = db.read_db()
    db.close_db()

    for task, date in tasks:
        __main_column__.controls.append(
            CreateTask(
                task,  
                date,  
                delete_function,
                update_function,
            )
        )
    __main_column__.update()


if __name__ == "__main__":
    ft.app(target=main, port=8000)