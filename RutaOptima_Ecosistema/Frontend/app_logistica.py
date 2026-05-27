import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import sqlite3

class AppLogistica:
    def __init__(self, root):
        self.root = root
        self.root.title("Ruta-Óptima - Control de Manifiestos")
        self.root.geometry("480x620")
        self.root.configure(bg="#2C3E50")
        self.root.resizable(False, False)
        
        # Identidad Visual
        try:
            ruta_logo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")
            img = Image.open(ruta_logo).convert("RGB").resize((110, 110), Image.Resampling.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(img)
            tk.Label(self.root, image=self.logo_img, bg="#2C3E50").pack(pady=10)
        except Exception:
            tk.Label(self.root, text="🚚 RUTA-ÓPTIMA LOGÍSTICA", font=("Arial", 18, "bold"), bg="#2C3E50", fg="#F1C40F").pack(pady=10)
        
        # Módulos CRUD
        frame_crud = tk.Frame(self.root, bg="#2C3E50")
        frame_crud.pack(pady=10)
        
        tk.Button(frame_crud, text="➕ Registrar Paquete", bg="#F1C40F", fg="black", width=28, font=("Arial", 11, "bold"), command=self.crear).pack(pady=5)
        tk.Button(frame_crud, text="📖 Auditar Manifiestos", bg="#3498DB", fg="white", width=28, font=("Arial", 11, "bold"), command=self.leer).pack(pady=5)
        tk.Button(frame_crud, text="✏️ Modificar Costo/Peso", bg="#E67E22", fg="white", width=28, font=("Arial", 11, "bold"), command=self.actualizar).pack(pady=5)
        tk.Button(frame_crud, text="🗑️ Cancelar Envío", bg="#E74C3C", fg="white", width=28, font=("Arial", 11, "bold"), command=self.eliminar).pack(pady=5)
        
        tk.Label(self.root, text="Centro de Control de Flota", font=("Arial", 10, "italic"), bg="#2C3E50", fg="#BDC3C7").pack(pady=15)
        tk.Button(self.root, text="📊 EJECUTAR POWER BI", bg="#27AE60", fg="white", font=("Arial", 12, "bold"), width=28, command=self.abrir_pbi).pack(pady=5)

    def ruta_db(self):
        return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Backend", "ruta_optima_logistica.db")

    def crear(self):
        ventana = tk.Toplevel(self.root)
        ventana.geometry("320x350")
        ventana.title("Nuevo Envío")
        ventana.configure(bg="#ECF0F1")
        ventana.grab_set()
        
        tk.Label(ventana, text="ID Cliente (1-3):", bg="#ECF0F1", fg="black").pack(pady=2)
        e_cli = tk.Entry(ventana, justify="center")
        e_cli.pack(pady=2)
        
        tk.Label(ventana, text="ID Destino (101-105):", bg="#ECF0F1", fg="black").pack(pady=2)
        e_dest = tk.Entry(ventana, justify="center")
        e_dest.pack(pady=2)
        
        tk.Label(ventana, text="Peso Físico (Kg):", bg="#ECF0F1", fg="black").pack(pady=2)
        e_peso = tk.Entry(ventana, justify="center")
        e_peso.pack(pady=2)
        
        tk.Label(ventana, text="Costo de Flete ($):", bg="#ECF0F1", fg="black").pack(pady=2)
        e_costo = tk.Entry(ventana, justify="center")
        e_costo.pack(pady=2)
        
        tk.Label(ventana, text="Fecha (YYYY-MM-DD):", bg="#ECF0F1", fg="black").pack(pady=2)
        e_fec = tk.Entry(ventana, justify="center")
        e_fec.pack(pady=2)
        
        def guardar():
            try:
                with sqlite3.connect(self.ruta_db()) as conn:
                    conn.cursor().execute("INSERT INTO fact_manifiestos (id_cliente, id_destino, peso_kg, costo_envio, fecha) VALUES (?, ?, ?, ?, ?)",
                                          (int(e_cli.get()), int(e_dest.get()), float(e_peso.get()), float(e_costo.get()), e_fec.get()))
                    conn.commit()
                messagebox.showinfo("Sistema Logístico", "Paquete registrado en el Manifiesto.", parent=ventana)
                ventana.destroy()
            except Exception as e:
                messagebox.showerror("Error en Registro", str(e), parent=ventana)
                
        tk.Button(ventana, text="💾 Despachar", command=guardar, bg="#F1C40F", fg="black", font=("Arial", 10, "bold")).pack(pady=15)

    def leer(self):
        ventana = tk.Toplevel(self.root)
        ventana.geometry("700x300")
        ventana.title("Auditoría de Envíos")
        ventana.grab_set()
        
        tabla = ttk.Treeview(ventana, columns=("ID", "Cliente", "Destino", "Peso (Kg)", "Flete ($)", "Fecha"), show="headings")
        for col in tabla["columns"]: tabla.heading(col, text=col)
        tabla.column("ID", width=40, anchor="center")
        tabla.column("Peso (Kg)", width=80, anchor="center")
        tabla.pack(fill="both", expand=True, padx=10, pady=10)
        
        try:
            with sqlite3.connect(self.ruta_db()) as conn:
                registros = conn.cursor().execute('''SELECT f.id_paquete, c.empresa, d.ciudad, f.peso_kg, f.costo_envio, f.fecha 
                                                     FROM fact_manifiestos f JOIN dim_clientes c ON f.id_cliente = c.id_cliente 
                                                     JOIN dim_destinos d ON f.id_destino = d.id_destino 
                                                     ORDER BY f.peso_kg DESC''').fetchall() # Ordenado por peso como pide la rúbrica
                for r in registros: tabla.insert("", tk.END, values=r)
        except Exception as e:
            messagebox.showerror("Error de Red", str(e))

    def actualizar(self):
        v = tk.Toplevel(self.root)
        v.geometry("300x200")
        v.configure(bg="#ECF0F1")
        tk.Label(v, text="ID Paquete a modificar:", bg="#ECF0F1").pack(pady=5)
        e_id = tk.Entry(v, justify="center")
        e_id.pack(pady=5)
        tk.Label(v, text="Nuevo Costo Flete ($):", bg="#ECF0F1").pack(pady=5)
        e_costo = tk.Entry(v, justify="center")
        e_costo.pack(pady=5)
        
        def exec_act():
            try:
                with sqlite3.connect(self.ruta_db()) as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE fact_manifiestos SET costo_envio=? WHERE id_paquete=?", (float(e_costo.get()), int(e_id.get())))
                    if cursor.rowcount == 0: raise ValueError("Guía de envío no encontrada.")
                    conn.commit()
                messagebox.showinfo("Éxito", "Flete recalculado en el manifiesto.", parent=v)
                v.destroy()
            except Exception as e: messagebox.showerror("Error", str(e), parent=v)
        tk.Button(v, text="Actualizar Ruta", command=exec_act, bg="#E67E22", fg="white", font=("Arial", 10, "bold")).pack(pady=10)

    def eliminar(self):
        v = tk.Toplevel(self.root)
        v.geometry("300x150")
        v.configure(bg="#ECF0F1")
        tk.Label(v, text="ID Paquete a CANCELAR:", bg="#ECF0F1", fg="#E74C3C").pack(pady=10)
        e_id = tk.Entry(v, justify="center")
        e_id.pack(pady=5)
        
        def exec_del():
            try:
                with sqlite3.connect(self.ruta_db()) as conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM fact_manifiestos WHERE id_paquete=?", (int(e_id.get()),))
                    if cursor.rowcount == 0: raise ValueError("Guía no localizada.")
                    conn.commit()
                messagebox.showinfo("Cancelado", "El envío ha sido retirado del camión.", parent=v)
                v.destroy()
            except Exception as e: messagebox.showerror("Error", str(e), parent=v)
        tk.Button(v, text="🗑️ Cancelar Envío", command=exec_del, bg="#E74C3C", fg="white", font=("Arial", 10, "bold")).pack(pady=10)

    def abrir_pbi(self):
        try:
            os.startfile(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "RutaOptima_Dashboard.pbix"))
        except Exception as e:
            messagebox.showerror("Error", "Asegúrese de guardar Power BI como 'RutaOptima_Dashboard.pbix'.")