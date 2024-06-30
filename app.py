# app.py

import sqlite3 as sqlite
import flet as ft
from datetime import datetime

# Create form for creating new task


class FormContainer(ft.UserControl):
    """ Create form for creating new task """

    def __init__(self, func):
        self.func = func
        super().__init__()

    def build(self):
        return ft.Container(
            width=280,
            height=80,
            bgcolor=ft.colors.BLUE_GREY_500,
            opacity=0,  # change value to 1 for 100% opacity
            border_radius=ft.border_radius.all(40),
            margin=ft.margin.only(left=-20, right=-20),
            animate=ft.animation.Animation(400, ft.AnimationCurve.DECELERATE),
            animate_opacity=200,
            padding=ft.padding.only(top=45, bottom=45),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.TextField(
                        label="New task",
                        height=58,
                        width=255,
                        color=ft.colors.BLACK,
                        border_color=ft.colors.BLUE_GREY_100,
                        hint_style=ft.TextStyle(
                            color=ft.colors.BLUE_GREY_100, size=12),
                    ),
                    ft.IconButton(
                        content=ft.Text("Add task"),
                        width=180,
                        height=44,
                        on_click=self.func,  # change to function
                        style=ft.ButtonStyle(
                            color=ft.colors.BLACK12,
                            bgcolor={"": ft.colors.BLACK},
                            shape={"": ft.RoundedRectangleBorder(radius=8)},
                        )
                    )
                ]
            )
        )

# Class to create new task by user
class CreateTask(ft.UserControl):
    """ Class to create new task by user """
    def __init__(self, task: str, date: str):
        self.task = task
        self.date = date
        super().__init__()
        
    def task_delete_edit(self, name: str, color: str):
        return ft.IconButton(
            icon=name,
            icon_size=18,
            icon_color=color,
            opacity=0,
            animate_opacity=200,
            on_click=None,
        )
        
        
    def hover_show_icon(self, e):
        """ Show icon while hovering over task """
        if e.data == "true":
            (
                e.control.content.controls[1].controls[0].opacity,
                e.control.content.controls[1].controls[1].opacity
            ) = (1,1)
            e.control.content.update()
            
        else:
            (
                e.control.content.controls[1].controls[0].opacity,
                e.control.content.controls[1].controls[1].opacity
            ) = (0,0)
            e.control.content.update()
    
    def build(self):
        return ft.Container(
            width=280,
            height=64,
            border=ft.border.all(0.85, ft.colors.WHITE54),
            border_radius=ft.border_radius.all(8),
            on_hover=lambda e: self.hover_show_icon(e), # Change later.. 
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            padding=ft.padding.all(10),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Column(
                        spacing=1,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Text(value=self.task, size=12), # change later to title
                            ft.Text(value=self.date, size=9, color=ft.colors.WHITE54), # change later to date
                        ]
                    ),
                    # Add icon delete and edit on right of task
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=0,
                        controls=[
                            self.task_delete_edit(ft.icons.DELETE_ROUNDED, ft.colors.RED_500),
                            self.task_delete_edit(ft.icons.EDIT_ROUNDED, ft.colors.WHITE70)
                        ],
                    )
                ]
            )
            
        )
    

def main(page: ft.Page):
    """ Main flet app"""
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.CrossAxisAlignment.CENTER
    
    # Add task to screen
    def add_task_to_screen(e):
        # Create new task and fetch data to display as task list the data there 2 attributes are {TITLE} + {DATE}
        
        # Date
        task_created_date = datetime.now().strftime("%b %d, %Y, %H:%M ")
        
        if form.content.controls[0].value:
            __main_column__.controls.append(
                # Create an instance of class CreateTask
                CreateTask(
                    task=form.content.controls[0].value, # Task creation title
                    date=task_created_date # Date of task creation
                )
            )
            __main_column__.update()
            # hide form container after submit
            create_to_do_task(e)

    # Create function show/hide
    def create_to_do_task(e):
        """ Create new task """
        if form.height != 200:
            form.height, form.opacity = 200, 1
            form.update()
        else:
            form.height, form.opacity = 80, 0
            form.update()

    # 1. Global variables for columns
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
                        on_click=lambda e: create_to_do_task(e),
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
                                # 2. insert here Global variables for columns
                                __main_column__,
                                # this is main control column
                                FormContainer(lambda e: add_task_to_screen(e)),
                            ]
                        )
                    )
                ]
            ),
        )
    )

    page.update()

    # 3. Create new task function call here is faster
    form = page.controls[0].content.controls[0].content.controls[1].controls[0]


if __name__ == "__main__":
    ft.app(target=main, port=8000)
