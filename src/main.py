import flet as ft
from views.forms import Forms


def main(page: ft.Page):
    page.title = 'PARKING'
    page.bgcolor = ft.Colors.GREY_300
    page.window.width = 800
    page.window.height = 800
    page.window.icon = './assets/icon.png'
    page.window.resizable = True
    page.update()
    
    form = Forms(page)
    
    page.add(form.build())

ft.app(target=main)

