import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from ui.styles import Styles

class MenuFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.db = Database()
        self.setup_ui()
        self.load_products()

    def setup_ui(self):
        # Header
        header = tk.Frame(self)
        header.pack(fill="x", pady=10)
        
        tk.Label(header, text="Gestión de Menú", font=Styles.SUBHEADER_FONT).pack(side="left")
        
        tk.Button(
            header, 
            text="➕ Agregar Producto", 
            command=self.open_add_modal,
            bg=Styles.SECONDARY,
            fg=Styles.WHITE,
            font=Styles.BOLD_FONT
        ).pack(side="right")

        # Table
        columns = ("id", "nombre", "precio")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("precio", text="Precio")
        
        self.tree.column("id", width=50)
        self.tree.column("nombre", width=300)
        self.tree.column("precio", width=100)
        
        self.tree.pack(fill="both", expand=True, pady=10)
        
        # Actions
        actions = tk.Frame(self)
        actions.pack(fill="x", pady=10)
        
        tk.Button(actions, text="Editar", command=self.edit_selected, bg=Styles.WARNING, fg=Styles.WHITE).pack(side="left", padx=5)
        tk.Button(actions, text="Eliminar", command=self.delete_selected, bg=Styles.DANGER, fg=Styles.WHITE).pack(side="left", padx=5)

    def load_products(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        products = self.db.get_products()
        for p in products:
            self.tree.insert("", "end", values=p)

    def open_add_modal(self):
        self.open_modal("Agregar Producto")

    def edit_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un producto para editar")
            return
        
        item = self.tree.item(selected[0])
        self.open_modal("Editar Producto", item['values'])

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un producto para eliminar")
            return
        
        if messagebox.askyesno("Confirmar", "¿Eliminar este producto?"):
            item = self.tree.item(selected[0])
            self.db.delete_product(item['values'][0])
            self.load_products()

    def open_modal(self, title, product_data=None):
        modal = tk.Toplevel(self)
        modal.title(title)
        modal.geometry("400x300")
        
        tk.Label(modal, text="Nombre:").pack(pady=5)
        name_entry = tk.Entry(modal)
        name_entry.pack(pady=5)
        
        tk.Label(modal, text="Precio:").pack(pady=5)
        price_entry = tk.Entry(modal)
        price_entry.pack(pady=5)
        
        if product_data:
            name_entry.insert(0, product_data[1])
            price_entry.insert(0, product_data[2])
            
        def save():
            name = name_entry.get()
            price = price_entry.get()
            
            if not name or not price:
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            
            try:
                price = float(price)
            except ValueError:
                messagebox.showerror("Error", "El precio debe ser un número")
                return
            
            if product_data:
                self.db.update_product(product_data[0], name, price)
            else:
                self.db.add_product(name, price)
            
            self.load_products()
            modal.destroy()
            
        tk.Button(modal, text="Guardar", command=save, bg=Styles.SECONDARY, fg=Styles.WHITE).pack(pady=20)
