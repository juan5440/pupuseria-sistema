import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from ui.styles import Styles

class POSFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.db = Database()
        self.cart = []
        self.setup_ui()
        self.load_products()

    def setup_ui(self):
        # Layout: Left (Products), Right (Cart)
        self.columnconfigure(0, weight=1) # Products
        self.columnconfigure(1, weight=1) # Cart
        self.rowconfigure(0, weight=1)

        # --- Left Panel: Products ---
        left_panel = tk.Frame(self, padx=10, pady=10)
        left_panel.grid(row=0, column=0, sticky="nsew")
        
        tk.Label(left_panel, text="Menú", font=Styles.SUBHEADER_FONT).pack(anchor="w")
        
        # Product Grid (using a Frame with grid layout inside a Canvas for scrolling if needed, 
        # but for simplicity using a Treeview or Listbox first. 
        # Better: A scrollable frame with buttons)
        
        self.product_container = tk.Frame(left_panel)
        self.product_container.pack(fill="both", expand=True, pady=10)
        
        # --- Right Panel: Cart ---
        right_panel = tk.Frame(self, padx=10, pady=10, bg=Styles.LIGHT_BG)
        right_panel.grid(row=0, column=1, sticky="nsew")
        
        tk.Label(right_panel, text="Carrito de Compras", font=Styles.SUBHEADER_FONT, bg=Styles.LIGHT_BG).pack(anchor="w")
        
        # Cart Table
        columns = ("producto", "precio", "cantidad", "total")
        self.cart_tree = ttk.Treeview(right_panel, columns=columns, show="headings", height=15)
        self.cart_tree.heading("producto", text="Producto")
        self.cart_tree.heading("precio", text="Precio")
        self.cart_tree.heading("cantidad", text="Cant")
        self.cart_tree.heading("total", text="Total")
        
        self.cart_tree.column("producto", width=150)
        self.cart_tree.column("precio", width=60)
        self.cart_tree.column("cantidad", width=50)
        self.cart_tree.column("total", width=60)
        
        self.cart_tree.pack(fill="x", pady=10)
        
        # Totals & Actions
        totals_frame = tk.Frame(right_panel, bg=Styles.LIGHT_BG)
        totals_frame.pack(fill="x", pady=10)
        
        self.total_label = tk.Label(totals_frame, text="Total: $0.00", font=Styles.HEADER_FONT, bg=Styles.LIGHT_BG)
        self.total_label.pack(anchor="e")
        
        # Payment Input
        pay_frame = tk.Frame(right_panel, bg=Styles.LIGHT_BG)
        pay_frame.pack(fill="x", pady=5)
        
        tk.Label(pay_frame, text="Pago del cliente: $", bg=Styles.LIGHT_BG).pack(side="left")
        self.pay_entry = tk.Entry(pay_frame)
        self.pay_entry.pack(side="left", padx=5)
        self.pay_entry.bind("<KeyRelease>", self.calculate_change)
        
        self.change_label = tk.Label(pay_frame, text="Cambio: $0.00", font=Styles.BOLD_FONT, bg=Styles.LIGHT_BG, fg=Styles.DANGER)
        self.change_label.pack(side="left", padx=10)
        
        # Buttons
        btn_frame = tk.Frame(right_panel, bg=Styles.LIGHT_BG)
        btn_frame.pack(fill="x", pady=20)
        
        tk.Button(btn_frame, text="Generar Ticket", command=self.checkout, bg=Styles.PRIMARY, fg=Styles.WHITE, font=Styles.BOLD_FONT, height=2).pack(fill="x")
        tk.Button(btn_frame, text="Limpiar Carrito", command=self.clear_cart, bg=Styles.DANGER, fg=Styles.WHITE).pack(fill="x", pady=5)

    def load_products(self):
        # Clear existing buttons
        for widget in self.product_container.winfo_children():
            widget.destroy()
            
        products = self.db.get_products()
        
        # Create a grid of buttons
        row = 0
        col = 0
        max_cols = 3
        
        for p in products:
            id, name, price = p
            btn = tk.Button(
                self.product_container,
                text=f"{name}\n${price:.2f}",
                font=Styles.NORMAL_FONT,
                bg=Styles.WHITE,
                width=15,
                height=3,
                command=lambda p=p: self.add_to_cart(p)
            )
            btn.grid(row=row, column=col, padx=5, pady=5)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1

    def add_to_cart(self, product):
        id, name, price = product
        
        # Check if already in cart
        found = False
        for item in self.cart:
            if item['id'] == id:
                item['cantidad'] += 1
                item['total'] = item['cantidad'] * item['precio']
                found = True
                break
        
        if not found:
            self.cart.append({
                'id': id,
                'nombre': name,
                'precio': price,
                'cantidad': 1,
                'total': price
            })
            
        self.update_cart_ui()

    def update_cart_ui(self):
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
            
        total_sum = 0
        for item in self.cart:
            self.cart_tree.insert("", "end", values=(item['nombre'], f"${item['precio']:.2f}", item['cantidad'], f"${item['total']:.2f}"))
            total_sum += item['total']
            
        self.total_label.config(text=f"Total: ${total_sum:.2f}")
        self.calculate_change()

    def calculate_change(self, event=None):
        try:
            total = sum(item['total'] for item in self.cart)
            payment = float(self.pay_entry.get())
            change = payment - total
            self.change_label.config(text=f"Cambio: ${change:.2f}")
        except ValueError:
            self.change_label.config(text="Cambio: $0.00")

    def clear_cart(self):
        self.cart = []
        self.update_cart_ui()
        self.pay_entry.delete(0, tk.END)

    def checkout(self):
        if not self.cart:
            messagebox.showwarning("Error", "El carrito está vacío")
            return
            
        try:
            total = sum(item['total'] for item in self.cart)
            payment_str = self.pay_entry.get()
            if not payment_str:
                messagebox.showerror("Error", "Ingrese el monto de pago")
                return
                
            payment = float(payment_str)
            
            if payment < total:
                messagebox.showerror("Error", "El pago es insuficiente")
                return
                
            change = payment - total
            
            # Save to DB
            venta_id = self.db.create_sale(total, payment, change, self.cart)
            
            # Generate Ticket
            ticket_content = self.generate_ticket_text(venta_id, total, payment, change)
            self.show_ticket_modal(ticket_content)
            
            self.clear_cart()
            
        except ValueError:
            messagebox.showerror("Error", "Ingrese un monto de pago válido")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar venta: {e}")

    def generate_ticket_text(self, venta_id, total, payment, change):
        from datetime import datetime, timedelta, timezone
        offset = timezone(timedelta(hours=-6))
        now = datetime.now(offset).strftime("%d/%m/%Y %H:%M:%S")
        
        lines = [
            "--------------------------------",
            "   PUPUSERIA 'EL SABOR DE CASA'   ",
            "--------------------------------",
            f"Fecha: {now}",
            f"Ticket #: {venta_id}",
            "--------------------------------",
            f"{'Producto':<18} {'Cant':<4} {'Total':<6}",
            "--------------------------------"
        ]
        
        for item in self.cart:
            name = item['nombre'][:18] # Truncate if too long
            qty = item['cantidad']
            subtotal = item['total']
            lines.append(f"{name:<18} {qty:<4} ${subtotal:.2f}")
            
        lines.extend([
            "--------------------------------",
            f"Total:      ${total:.2f}",
            f"Pago:       ${payment:.2f}",
            f"Cambio:     ${change:.2f}",
            "--------------------------------",
            "      ¡Gracias por su compra!      ",
            "--------------------------------"
        ])
        
        return "\n".join(lines)

    def show_ticket_modal(self, ticket_content):
        modal = tk.Toplevel(self)
        modal.title("Ticket de Venta")
        modal.geometry("350x500")
        
        text_area = tk.Text(modal, font=("Courier New", 10), padx=10, pady=10)
        text_area.insert("1.0", ticket_content)
        text_area.config(state="disabled") # Read-only
        text_area.pack(fill="both", expand=True)
        
        btn_frame = tk.Frame(modal)
        btn_frame.pack(fill="x", pady=10)
        
        def print_ticket():
            import os
            filename = "ticket.txt"
            with open(filename, "w") as f:
                f.write(ticket_content)
            
            try:
                os.startfile(filename, "print")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo imprimir: {e}")
        
        tk.Button(btn_frame, text="🖨️ Imprimir", command=print_ticket, bg=Styles.PRIMARY, fg=Styles.WHITE).pack(side="left", padx=20, expand=True)
        tk.Button(btn_frame, text="Cerrar", command=modal.destroy).pack(side="right", padx=20, expand=True)
