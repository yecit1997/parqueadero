import flet as ft
from views.forms import Forms


def main(page: ft.Page):
    page.title = 'PARKING'
    page.bgcolor = ft.Colors.GREY_300
    page.window_min_width = 500
    page.window_min_height = 500
    page.window_resizable = False
    page.update()
    
    form = Forms(page)
    
    page.add(form.build())

ft.app(main)
