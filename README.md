# 🚚 Ruta-Óptima: Ecosistema de Logística y Enrutamiento B2B (Reto 1)

Solución tecnológica diseñada para la clasificación automatizada de carga (Documento, Paquetería, Carga), la generación de manifiestos y la auditoría de facturación de fletes de transporte terrestre.

**Integración de Ingeniería:** Este ecosistema unifica el **Taller 13** (Arquitectura Python, SQLite, Tkinter GUI) y el **Taller 12** (Power BI, DAX Avanzado, Q&A) en un solo producto de software funcional, garantizando que los datos transaccionales se conviertan instantáneamente en visualizaciones gerenciales.

## 👥 Equipo de Desarrollo y Arquitectura
* **Juan José Caballero** (Arquitectura de Base de Datos y Orquestación SQLite)
* **Martín Trujillo** (Desarrollo Frontend Tkinter e Integración de Sistemas)
* **Daniel Camilo Piraquive** (Inteligencia de Negocios, DAX y Diseño UI/UX)

## 🏗️ Motor Operativo (Taller 13)
* **Backend Relacional (`database.py`):** Motor SQLite3 bajo un Modelo Estrella (`fact_manifiestos`, `dim_destinos`, `dim_clientes`). Inyecta un *Data Seeding* de 5 registros mínimos para asegurar despliegues inmediatos en sucursales logísticas.
* **Frontend Transaccional (`app_logistica.py`):** GUI industrial diseñada en `Tkinter` que permite el control total (CRUD) sobre los manifiestos de despacho. Incorpora manejo de excepciones de usuario con bloques `try-except` y mitigación de fallos vía `messagebox`.

## 📊 Inteligencia de Negocios (Taller 12)
* **Extracción de Datos:** Tablero `RutaOptima_Dashboard.pbix` conectado en vivo a la base de datos a través de un script puente nativo de Python (`pandas`), eludiendo fallos de configuración de rutas estáticas.
* **Modelado Logístico DAX:** Implementación de Inteligencia de Tiempo (Tabla Calendario), Métricas de Volumen y Costo (`SUM`, `DIVIDE`, `CALCULATE`), y una Columna Calculada condicional (`IF`) que categoriza automáticamente el tipo de paquete según su peso físico.
* **Toma de Decisiones:** Dashboard regido bajo la regla de los 5 segundos con paleta de colores industrial. Contiene una pestaña **Q&A - Respuestas de Negocio** para auditar el volumen y la facturación de la flota.

## 🚀 Despliegue del Sistema
1. Clonar el repositorio localmente.
2. Ejecutar `python main.py` para levantar la terminal de despachos y estructurar la bóveda de datos automáticamente.
3. Registrar nuevos envíos desde la aplicación de escritorio.
4. Abrir Power BI, acceder a *Transformar Datos* y modificar la variable `ruta_db` en el origen del script de Python con la ruta de la máquina local.
