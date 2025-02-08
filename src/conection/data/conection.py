import sqlite3 as sql
import os
from datetime import datetime

class Conection:
    
    def __init__(self) -> None:
        self.db_path = os.path.join('storage/data', 'estacionamiento.db')
        self.init_db()
        
    # Función para inicializar la base de datos
    def init_db(self):
        with sql.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS estacionamiento (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    placa TEXT NOT NULL,
                    hora_llegada TEXT NOT NULL,
                    hora_salida TEXT,
                    precio REAL
                )
            ''')
            conn.commit()

    # Función para registrar la llegada de un vehículo
    def registrar_llegada(self, placa):
        with sql.connect(self.db_path) as conn:
            cursor = conn.cursor()
            hora_llegada = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute('''
                INSERT INTO estacionamiento (placa, hora_llegada) VALUES (?, ?)
            ''', (placa, hora_llegada))
            conn.commit()

    # Función para registrar la salida de un vehículo y calcular el precio
    def registrar_salida(self, placa):
        with sql.connect(self.db_path) as conn:
            cursor = conn.cursor()
            hora_salida = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Obtener la hora de llegada
            cursor.execute('''
                SELECT hora_llegada FROM estacionamiento WHERE placa = ? AND hora_salida IS NULL
            ''', (placa,))
            resultado = cursor.fetchone()
            VALOR_ESTACIONAMIENTO = 2000
            if resultado:
                hora_llegada = datetime.strptime(resultado[0], '%Y-%m-%d %H:%M:%S')
                # Calcular el tiempo de estacionamiento
                tiempo_estacionado = (datetime.now() - hora_llegada).total_seconds() / 3600  # en horas
                precio = tiempo_estacionado * VALOR_ESTACIONAMIENTO 
                
                if precio < VALOR_ESTACIONAMIENTO:
                    precio = VALOR_ESTACIONAMIENTO
                
                # Actualizar la hora de salida y el precio
                cursor.execute('''
                    UPDATE estacionamiento SET hora_salida = ?, precio = ? WHERE placa = ? AND hora_salida IS NULL
                ''', (hora_salida, precio, placa))
                conn.commit()
                return precio
            else:
                return None

    # Función para obtener todos los datos
    def get_data(self):
        with sql.connect(self.db_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    '''SELECT * FROM estacionamiento'''
                )
                data = cursor.fetchall()
                return data
            except sql.Error as e:
                print(f"Error al obtener los datos: {e}")
                return []


