import unittest
import os
from database import Database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db_name = "test_pupuseria.db"
        self.db = Database(self.db_name)

    def tearDown(self):
        if os.path.exists(self.db_name):
            os.remove(self.db_name)

    def test_initial_products(self):
        products = self.db.get_products()
        self.assertGreater(len(products), 0)
        self.assertEqual(products[0][1], 'Pupusa de Queso')

    def test_add_product(self):
        self.db.add_product("Test Product", 9.99)
        products = self.db.get_products()
        found = False
        for p in products:
            if p[1] == "Test Product":
                found = True
                break
        self.assertTrue(found)

    def test_create_sale(self):
        items = [
            {'id': 1, 'cantidad': 2, 'precio': 1.00}, # 2 Pupusas de Queso
            {'id': 2, 'cantidad': 1, 'precio': 1.25}  # 1 Pupusa Revuelta
        ]
        total = 3.25
        pago = 5.00
        cambio = 1.75
        
        venta_id = self.db.create_sale(total, pago, cambio, items)
        self.assertIsNotNone(venta_id)
        
        sales = self.db.get_sales()
        self.assertEqual(sales[0][0], venta_id)
        self.assertEqual(sales[0][2], total)

if __name__ == '__main__':
    unittest.main()
