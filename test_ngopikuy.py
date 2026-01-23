import unittest
import importlib.util
import sys
import os

# Load ngopikuy.py as a module without changing its code
spec = importlib.util.spec_from_file_location("ngopikuy", os.path.join(os.path.dirname(__file__), "ngopikuy.py"))
ngopikuy = importlib.util.module_from_spec(spec)
sys.modules["ngopikuy"] = ngopikuy
spec.loader.exec_module(ngopikuy)

class TestManajemenPersediaan(unittest.TestCase):
    def setUp(self):
        self.inventory = ngopikuy.ManajemenPersediaan()
        # Reset stock for test isolation
        self.inventory.stock = {
            "Bubuk Kopi": {"qty": 100, "unit": "gram"},
            "Air": {"qty": 200, "unit": "ml"},
        }

    def test_add_stock(self):
        self.inventory.add_stock("Bubuk Kopi", 50)
        self.assertEqual(self.inventory.stock["Bubuk Kopi"]["qty"], 150)

    def test_use_stock_success(self):
        self.inventory.use_stock("Bubuk Kopi", 20)
        self.assertEqual(self.inventory.stock["Bubuk Kopi"]["qty"], 80)

    def test_use_stock_insufficient(self):
        with self.assertRaises(ngopikuy.StokTidakCukupError):
            self.inventory.use_stock("Bubuk Kopi", 200)

    def test_add_new_stock_item(self):
        self.inventory.add_stock("Susu Full Cream", 50, unit="ml")
        self.assertIn("Susu Full Cream", self.inventory.stock)
        self.assertEqual(self.inventory.stock["Susu Full Cream"]["qty"], 50)

class TestProductManager(unittest.TestCase):
    def setUp(self):
        self.pm = ngopikuy.ProductManager()
        self.product = ngopikuy.ProductFactory.create_product(
            "Latte", "coffee", 22000, {"Bubuk Kopi": {"qty": 18, "unit": "gram"}}
        )
        self.pm.add_product(self.product)

    def test_add_product(self):
        self.assertEqual(len(self.pm.products), 1)

    def test_get_product_by_index(self):
        prod = self.pm.get_product_by_index(0)
        self.assertEqual(prod.name, "Latte")

    def test_hapus_produk(self):
        self.pm.hapus_produk("Latte")
        self.assertEqual(len(self.pm.products), 0)

class TestTransaksiManager(unittest.TestCase):
    def setUp(self):
        self.tm = ngopikuy.TransaksiManager()
        self.penjualan = ngopikuy.Penjualan("TRX-001", "cash", username="admin")
        self.pembelian = ngopikuy.Pembelian("TRX-002", "SUP-COF", username="admin")

    def test_tambah_penjualan(self):
        self.tm.tambah_penjualan(self.penjualan)
        self.assertEqual(len(self.tm.riwayat_penjualan), 1)

    def test_tambah_pembelian(self):
        self.tm.tambah_pembelian(self.pembelian)
        self.assertEqual(len(self.tm.riwayat_pembelian), 1)

if __name__ == "__main__":
    unittest.main()
