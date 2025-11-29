import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from ui.styles import Styles

class HistoryFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.db = Database()
        self.setup_ui()
        self.load_sales()

    def setup_ui(self):
        # Header
        header = tk.Frame(self)
        header.pack(fill="x", pady=10)
        
        tk.Label(header, text="Historial de Ventas", font=Styles.SUBHEADER_FONT).pack(side="left")
        
        tk.Button(
            header, 
            text="🔄 Actualizar", 
            command=self.load_sales,
            bg=Styles.SECONDARY,
            fg=Styles.WHITE
        ).pack(side="right")

        # Table
        columns = ("id", "fecha", "total", "pago", "cambio")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree.heading("id", text="ID Venta")
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("total", text="Total")
        self.tree.heading("pago", text="Pago")
        self.tree.heading("cambio", text="Cambio")
        
        self.tree.column("id", width=50)
        self.tree.column("fecha", width=150)
        self.tree.column("total", width=80)
        self.tree.column("pago", width=80)
        self.tree.column("cambio", width=80)
        
        self.tree.pack(fill="both", expand=True, pady=10)
        
        self.tree.bind("<Double-1>", self.show_details)
        
        tk.Label(self, text="Doble clic en una venta para ver detalles", font=("Segoe UI", 10, "italic")).pack(pady=5)

    def load_sales(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        sales = self.db.get_sales()
        for s in sales:
            # s: (id, fecha, total, pago, cambio)
            self.tree.insert("", "end", values=(s[0], s[1], f"${s[2]:.2f}", f"${s[3]:.2f}", f"${s[4]:.2f}"))

    def show_details(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        
        item = self.tree.item(selected[0])
        venta_id = item['values'][0]
        
        details = self.db.get_sale_details(venta_id)
        
        modal = tk.Toplevel(self)
        modal.title(f"Detalles Venta #{venta_id}")
        modal.geometry("500x400")
        
        tk.Label(modal, text=f"Detalles de Venta #{venta_id}", font=Styles.BOLD_FONT).pack(pady=10)
        
        columns = ("producto", "cantidad", "precio", "subtotal")
        tree = ttk.Treeview(modal, columns=columns, show="headings")
        tree.heading("producto", text="Producto")
        tree.heading("cantidad", text="Cant")
        tree.heading("precio", text="Precio")
        tree.heading("subtotal", text="Subtotal")
        
        tree.column("producto", width=200)
        tree.column("cantidad", width=50)
        tree.column("precio", width=80)
        tree.column("subtotal", width=80)
        
        tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        for d in details:
            # d: (nombre, cantidad, precio, subtotal)
            tree.insert("", "end", values=(d[0], d[1], f"${d[2]:.2f}", f"${d[3]:.2f}"))
            
        tk.Button(modal, text="Cerrar", command=modal.destroy).pack(pady=10)
