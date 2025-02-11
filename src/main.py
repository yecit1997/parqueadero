import flet as ft
from views.forms import Forms


def main(page: ft.Page):
    page.title = 'PARKING'
    page.bgcolor = ft.Colors.GREY_300
    page.window.width = 500
    page.window.height = 800
    # page.window.min_width = 800
    # page.window.min_height = 800
    page.window.resizable = True
    # page.vertical_alignment = ft.MainAxisAlignment.START
    # page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()
    
    form = Forms(page)
    
    page.add(form.build())

ft.app(target=main)

