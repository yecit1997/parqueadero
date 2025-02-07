import flet as ft


class Forms(ft.Control):
    def __init__(self, page):
        super().__init__()

        self.page = page
        
        
        # Campos del formulario
        self.placa = ft.TextField(label='Placa', border_color=ft.Colors.BLUE_400)
        self.hora_entrada = ft.TextField(label='Hora entrada', border_color=ft.Colors.BLUE_400)
        self.hora_salida = ft.TextField(label='Hora salida', border_color=ft.Colors.BLUE_400)
        
        self.form = ft.Container(
            bgcolor='#222222',
            border_radius=10,
            # expand=1,
            content= ft.Column(
                # alignment=ft.MainAxisAlignment.SPACE_AROUND,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text('Ingrese los datos del vehiculo',
                            size=35,
                            text_align='center',
                            font_family='vivaldi',),
                    self.placa,
                    self.hora_entrada,
                    self.hora_salida,
                ]
            )
        )
        
        self.content = ft.Row(
            expand=True,
            controls=[
                self.form,
            ]
        )
    
    def build(self):
        return self.content
        
        
