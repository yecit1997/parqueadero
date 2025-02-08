import flet as ft
from conection.data.conection import Conection

class Forms(ft.Control):
    def __init__(self, page):
        super().__init__()

        self.page = page
        self.base = Conection()
        
        # Campos del formulario
        self.placa = ft.TextField(label="Placa", 
                                  border_color=ft.Colors.BLUE_400,
                                  max_length=6,
                                  autofocus=True,
                                  )
        self.resultado_text = ft.Text()
        
      
        self.search_filed = ft.TextField(
            label='Buscar placa',
            suffix_icon=ft.Icons.SEARCH,
            border=ft.InputBorder.UNDERLINE,
            label_style=ft.TextStyle(color=ft.Colors.WHITE),
            border_color=ft.Colors.WHITE,
            show_cursor=True,
        )
        
        self.data_table = ft.DataTable(
            expand=True,
            border=ft.border.all(2,ft.Colors.BLUE_400),
            data_row_color={ft.ControlState.SELECTED: 'blue',
                            ft.ControlState.PRESSED: 'black'},
            
            border_radius=10,
            show_checkbox_column=True,
            
            columns=[
                ft.DataColumn(ft.Text('Placa', color='blue', weight='bold')),
                ft.DataColumn(ft.Text('Hora entrada', color='blue', weight='bold'), numeric=True),
                # ft.DataColumn(ft.Text('Correo', color='blue', weight='bold')),
                # ft.DataColumn(ft.Text('Teléfono', color='blue', weight='bold'), numeric=True)
            ]
        )
            

        self.form = ft.Container(
            col=3,
            bgcolor=ft.Colors.BLACK87,
            border_radius=10,
            padding=10,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.START,
                spacing=200,
                controls=[
                    ft.Container(
                        ft.Text(
                            "Ingrese la placa del vehiculo",
                            text_align="center",
                            size=30,
                            color=ft.Colors.BLUE_ACCENT,
                        ),
                        # padding=10,
                    ),
                    ft.Container(
                        content=ft.Column(
                            alignment=ft.MainAxisAlignment.SPACE_AROUND,
                            spacing=50,
                            controls=[
                                self.placa,
                                self.resultado_text,
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    expand=True,
                                    controls=[
                                    ft.ElevatedButton("Registrar Llegada",on_click= self.on_registrar_llegada),
                                    ft.ElevatedButton("Registrar Salida", on_click= self.on_registrar_salida),
                                    ]
                                ),
                            ],
                        )
                    ),
                ],
            ),
        )

        self.show_data()
        
        self.tabla = ft.Container(
            col=9, 
            bgcolor=ft.Colors.BLACK87, 
            border_radius=10, 
            content=ft.Column(
                controls=[
                    # Creamos un contenedor en el cual vamos a colocar una fila y esta a su
                    # vez contendra la barra de busqueda de la tabla
                    ft.Container(
                        
                        ft.Row(
                            controls=[
                                self.search_filed,
                            ]
                        )
                    ),
                    # Creamos una columna la cual es sus controlers contará
                    # con una fila responsi en la cual vamos a colocar nuestra tabla
                    ft.Column(
                        controls=[
                            ft.ResponsiveRow([
                                self.data_table,
                            ])
                        ]
                    )
                ]
            )
        )

        self.container = ft.ResponsiveRow(
            expand=True, 
            controls=[
                self.form, 
                self.tabla
                ]
            )

    def build(self):
        return self.container
    
    
    
# Comandos

    def on_registrar_llegada(self, e):
        placa = self.placa.value
        self.base.registrar_llegada(placa)
        self.resultado_text.value = f"Vehículo {placa} registrado como llegado."
        self.placa.value = ""
        self.page.update()
        
    def on_registrar_salida(self, e):
        placa = self.placa.value
        precio = self.base.registrar_salida(placa)
        if precio is not None:
            self.resultado_text.value = f"Vehículo {placa} registrado como salido. Precio: {precio:.2f} unidades."
        else:
            self.resultado_text.value = f"No se encontró el vehículo {placa}."
        self.placa.value = ""
        self.page.update()
        
    def show_data(self):
        self.data_table.rows = [] # Se leccionamos las filas de la tabla
        # Recorremos los objetos que tenemos en la base de datos
        for x in self.base.get_data():
            # En cada iteraccion los asignamos a una DataRow
            self.data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(x[1])),
                        ft.DataCell(ft.Text(x[2])),
                    ]
                )
            )
        self.page.update()
