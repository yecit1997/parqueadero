import flet as ft
from conection.data.conection import Conection


class Forms(ft.Control):
    def __init__(self, page):
        super().__init__()

        self.page = page
        self.base = Conection()

        # Campos del formulario
        self.placa = ft.TextField(
            label="Placa",
            border_color=ft.Colors.BLUE_400,
            max_length=6,
            autofocus=True,
        )

        self.resultado_text = ft.Text()

        self.search_filed = ft.TextField(
            label="Buscar placa",
            suffix_icon=ft.Icons.SEARCH,
            border=ft.InputBorder.UNDERLINE,
            label_style=ft.TextStyle(color=ft.Colors.WHITE),
            border_color=ft.Colors.WHITE,
            show_cursor=True,
            on_change=self.search_contact,
        )

        self.name_parking = ft.Text(
            "PAR-KING",
            text_align="center",
            size=30,
            color=ft.Colors.WHITE,
        )

        self.dar_salida = ft.IconButton(
            tooltip="Editar",
            icon=ft.Icons.EDIT,
            icon_color=ft.Colors.WHITE,
            on_click=self.salida,
        )

        self.boton_mode = ft.IconButton(
            icon=ft.Icons.DARK_MODE,  # LIGHT_MODE
            icon_color="blue400",
            icon_size=20,
            tooltip="Pause record",
            on_click=self.modo_theme,
        )

        self.data_table = ft.DataTable(
            expand=True,
            border=ft.border.all(2, ft.Colors.BLUE_400),
            data_row_color={
                ft.ControlState.SELECTED: "blue",
                ft.ControlState.PRESSED: "black",
            },
            border_radius=10,
            show_checkbox_column=True,
            columns=[
                ft.DataColumn(ft.Text("Placa", color="blue", weight="bold")),
                ft.DataColumn(
                    ft.Text("Hora entrada", color="blue", weight="bold"),
                ),
                ft.DataColumn(ft.Text("Hora salida", color="blue", weight="bold")),
            ],
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
                        self.name_parking,
                        alignment=ft.alignment.center,
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
                                        ft.ElevatedButton(
                                            "Registrar Llegada",
                                            on_click=self.on_registrar_llegada,
                                        ),
                                        ft.ElevatedButton(
                                            "Registrar Salida",
                                            on_click=self.on_registrar_salida,
                                        ),
                                    ],
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
            padding=10,
            content=ft.Column(
                controls=[
                    # Creamos un contenedor en el cual vamos a colocar una fila y esta a su
                    # vez contendra la barra de busqueda de la tabla
                    ft.Container(
                        ft.Row(
                            controls=[
                                ft.Row(
                                    controls=[
                                        self.search_filed,
                                        self.dar_salida,
                                    ],
                                ),
                                self.boton_mode,
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        )
                    ),
                    # Creamos una columna la cual es sus controlers contará
                    # con una fila responsi en la cual vamos a colocar nuestra tabla
                    ft.Column(
                        expand=True,
                        scroll="auto",
                        controls=[
                            ft.ResponsiveRow(
                                [
                                    self.data_table,
                                ]
                            )
                        ],
                    ),
                ]
            ),
        )

        self.container = ft.ResponsiveRow(
            expand=True,
             
            controls=[self.form, self.tabla]
            )

    def build(self):
        return self.container

    """
    --------------------------------------------------------------------------
        CREAMOS LAS FUNCIONALIDADES PARA CADA UNO DE LOS BOTONES
    --------------------------------------------------------------------------
    """

    def on_registrar_llegada(self, e):
        if self.placa.value.strip() != "":
            placa = self.placa.value.strip().upper()
            data = self.base.get_data()

            # Verificar si la placa ya está registrada sin hora de salida
            placa_existente_sin_salida = any(
                x[1] == placa and x[3] is None for x in data
            )
            if placa_existente_sin_salida:
                self.resultado_text.value = (
                    f"Vehículo {placa} ya se encuentra registrado.\nEsperando salida."
                )
            else:
                # Verificar si la placa está registrada con hora de salida
                placa_existente_con_salida = next(
                    (x for x in data if x[1] == placa and x[3] is not None), None
                )
                if placa_existente_con_salida:
                    # Actualizar el registro existente
                    self.base.actualizar_registro(placa_existente_con_salida[0], placa)
                    self.resultado_text.value = f"Vehículo {placa} reingreso."
                else:
                    # Registrar una nueva llegada
                    self.base.registrar_llegada(placa)
                    self.resultado_text.value = (
                        f"Vehículo {placa} registrado como llegado."
                    )
                self.placa.value = ""
        else:
            self.resultado_text.value = "Debe ingresar una placa"

        self.show_data()

    def on_registrar_salida(self, e):
        placa = self.placa.value
        placa = placa.upper()
        precio = self.base.registrar_salida(placa)
        if precio is not None:
            self.resultado_text.value = f"Vehículo {placa} registrado como salido. Precio: $ {precio:.2f} pesos."
        else:
            self.resultado_text.value = f"No se encontró el vehículo {placa}."
        self.placa.value = ""
        self.show_data()

    def show_data(self):
        self.data_table.rows = []  # Se leccionamos las filas de la tabla
        # Recorremos los objetos que tenemos en la base de datos
        for x in self.base.get_data():
            # En cada iteraccion los asignamos a una DataRow
            self.data_table.rows.append(
                ft.DataRow(
                    on_select_changed=self.get_index,
                    cells=[
                        ft.DataCell(ft.Text(x[1])),
                        ft.DataCell(ft.Text(x[2])),
                        ft.DataCell(ft.Text(x[3])),
                    ],
                )
            )
        self.page.update()

    def search_contact(self, e):
        search = self.search_filed.value.upper()
        placa = list(filter(lambda x: search in x[1], self.base.get_data()))
        self.data_table.rows = []
        if not self.search_filed == "":
            if len(placa) > 0:
                for x in placa:
                    self.data_table.rows.append(
                        ft.DataRow(
                            on_select_changed=self.get_index,
                            cells=[
                                ft.DataCell(ft.Text(x[1])),
                                ft.DataCell(ft.Text(x[2])),
                                ft.DataCell(ft.Text(x[3])),
                            ],
                        )
                    )
                    self.page.update()
        else:
            self.show_data()
        # self.page.update()

    def modo_theme(self, e):
        if e.name:
            if self.boton_mode.icon == "DARK_MODE":
                self.boton_mode.icon = "LIGHT_MODE"
                self.tabla.bgcolor = ft.Colors.BLACK87
                self.form.bgcolor = ft.Colors.BLACK87
                self.page.theme_mode = ft.ThemeMode.DARK
                self.search_filed.border_color = ft.Colors.WHITE
                self.search_filed.label_style = ft.TextStyle(color=ft.Colors.WHITE)
                self.name_parking.color = ft.Colors.WHITE
            else:
                self.boton_mode.icon = "DARK_MODE"
                self.tabla.bgcolor = ft.Colors.WHITE
                self.form.bgcolor = ft.Colors.WHITE
                self.page.theme_mode = ft.ThemeMode.LIGHT
                self.search_filed.border_color = ft.Colors.BLACK
                self.search_filed.label_style = ft.TextStyle(color=ft.Colors.BLACK)
                self.name_parking.color = ft.Colors.BLACK87

        self.page.update()

    def get_index(self, e):
        if e.control.selected:
            e.control.selected = False
        else:
            e.control.selected = True

        placa = e.control.cells[0].content.value

        for row in self.base.get_data():
            if row[1] == placa:
                self.selected__row = row
                break
        self.page.update()

    def salida(self, e):
        try:
            self.placa.value = self.selected__row[1]
            self.page.update()
        except TypeError:
            print("Se produjo un error")
