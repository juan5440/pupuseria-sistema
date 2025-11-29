import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name="pupuseria.db"):
        self.db_name = db_name
        self.create_tables()
        self.seed_data()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def create_tables(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        # Productos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                precio REAL NOT NULL
            )
        ''')

        # Ventas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total REAL NOT NULL,
                pago REAL NOT NULL,
                cambio REAL NOT NULL
            )
        ''')

        # Detalle Venta
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS detalle_venta (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                venta_id INTEGER,
                producto_id INTEGER,
                cantidad INTEGER NOT NULL,
                precio_unitario REAL NOT NULL,
                FOREIGN KEY (venta_id) REFERENCES ventas(id) ON DELETE CASCADE,
                FOREIGN KEY (producto_id) REFERENCES productos(id)
            )
        ''')

        conn.commit()
        conn.close()

    def seed_data(self):
        """Insert initial data if products table is empty"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM productos")
        if cursor.fetchone()[0] == 0:
            initial_products = [
                ('Pupusa de Queso', 1.00),
                ('Pupusa Revuelta', 1.25),
                ('Pupusa de Frijol', 1.00),
                ('Pollo en Pan', 3.50),
                ('Pollo con Papas', 4.50),
                ('Agua', 0.75),
                ('Jugo', 1.00),
                ('Cerveza', 2.00)
            ]
            cursor.executemany("INSERT INTO productos (nombre, precio) VALUES (?, ?)", initial_products)
            conn.commit()
            print("Datos iniciales insertados.")
        
        conn.close()

    # --- Productos ---
    def get_products(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos")
        products = cursor.fetchall()
        conn.close()
        return products

    def add_product(self, nombre, precio):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO productos (nombre, precio) VALUES (?, ?)", (nombre, precio))
        conn.commit()
        conn.close()

    def update_product(self, id, nombre, precio):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE productos SET nombre = ?, precio = ? WHERE id = ?", (nombre, precio, id))
        conn.commit()
        conn.close()

    def delete_product(self, id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos WHERE id = ?", (id,))
        conn.commit()
        conn.close()

    # --- Ventas ---
    def create_sale(self, total, pago, cambio, items):
        """
        items: list of dicts {'id': product_id, 'cantidad': qty, 'precio': unit_price}
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Central America Time (UTC-6)
        from datetime import datetime, timedelta, timezone
        offset = timezone(timedelta(hours=-6))
        now = datetime.now(offset).strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            cursor.execute("INSERT INTO ventas (fecha, total, pago, cambio) VALUES (?, ?, ?, ?)", (now, total, pago, cambio))
            venta_id = cursor.lastrowid
            
            for item in items:
                cursor.execute('''
                    INSERT INTO detalle_venta (venta_id, producto_id, cantidad, precio_unitario)
                    VALUES (?, ?, ?, ?)
                ''', (venta_id, item['id'], item['cantidad'], item['precio']))
            
            conn.commit()
            return venta_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def get_sales(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ventas ORDER BY fecha DESC")
        sales = cursor.fetchall()
        conn.close()
        return sales

    def get_sale_details(self, venta_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.nombre, d.cantidad, d.precio_unitario, (d.cantidad * d.precio_unitario) as subtotal
            FROM detalle_venta d
            JOIN productos p ON d.producto_id = p.id
            WHERE d.venta_id = ?
        ''', (venta_id,))
        details = cursor.fetchall()
        conn.close()
        return details
