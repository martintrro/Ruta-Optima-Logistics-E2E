import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "ruta_optima_logistica.db")

class LogisticaDB:
    @staticmethod
    def inicializar():
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            
            # Esquema Estrella (Dimensiones y Hechos)
            cursor.execute('''CREATE TABLE IF NOT EXISTS dim_destinos (
                                id_destino INTEGER PRIMARY KEY, ciudad TEXT, zona TEXT)''')
                                
            cursor.execute('''CREATE TABLE IF NOT EXISTS dim_clientes (
                                id_cliente INTEGER PRIMARY KEY, empresa TEXT, sector TEXT)''')
                                
            cursor.execute('''CREATE TABLE IF NOT EXISTS fact_manifiestos (
                                id_paquete INTEGER PRIMARY KEY AUTOINCREMENT,
                                id_cliente INTEGER, id_destino INTEGER,
                                peso_kg REAL, costo_envio REAL, fecha TEXT,
                                FOREIGN KEY(id_cliente) REFERENCES dim_clientes(id_cliente),
                                FOREIGN KEY(id_destino) REFERENCES dim_destinos(id_destino))''')
            
            # Data Seeding (Autogeneración de 5 registros mínimos)
            cursor.execute("SELECT COUNT(*) FROM dim_destinos")
            if cursor.fetchone()[0] == 0:
                print("Iniciando despliegue de Base de Datos Ruta-Óptima...")
                
                cursor.executemany("INSERT INTO dim_destinos VALUES (?, ?, ?)", 
                                   [(101, "Bogotá", "Centro"), (102, "Medellín", "Norte"), 
                                    (103, "Cali", "Sur"), (104, "Barranquilla", "Costa"), 
                                    (105, "Bucaramanga", "Oriente")])
                                    
                cursor.executemany("INSERT INTO dim_clientes VALUES (?, ?, ?)", 
                                   [(1, "Tech Solutions", "Tecnología"), (2, "AgroExport", "Alimentos"), 
                                    (3, "Moda Fast", "Textil")])
                
                # Manifiestos base
                manifiestos = [
                    (1, 101, 1.5, 8000, "2026-05-01"),   # Documento
                    (2, 102, 12.0, 25000, "2026-05-05"), # Paquetería
                    (3, 103, 45.0, 85000, "2026-05-10"), # Carga
                    (1, 104, 0.5, 6000, "2026-05-15"),   # Documento
                    (3, 105, 18.5, 45000, "2026-05-20")  # Carga
                ]
                cursor.executemany("INSERT INTO fact_manifiestos (id_cliente, id_destino, peso_kg, costo_envio, fecha) VALUES (?, ?, ?, ?, ?)", manifiestos)
                
            conn.commit()