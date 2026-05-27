import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from Backend.database import LogisticaDB
from Frontend.app_logistica import AppLogistica

if __name__ == '__main__':
    LogisticaDB.inicializar()
    root = tk.Tk()
    app = AppLogistica(root)
    root.mainloop()