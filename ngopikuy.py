# =========================
# DECORATOR
# =========================
def highlight_menu(func):
    def wrapper(*args, **kwargs):
        print("\n MENU PILIHAN ")
        return func(*args, **kwargs)
    return wrapper

# =========================
# CLASS PENJUALAN
# =========================
class Penjualan(Transaksi):
    # Class penjualan Subclass dari Transaksi merepresentasikan satu transaksi penjualan ke customer

    def __init__(self, id_transaksi, metode_bayar):
        # Memanggil constructor Transaksi (inheritance)
        super().__init__(id_transaksi)
        self.total_harga = 0          # Menyimpan total harga penjualan
        self.metode_bayar = metode_bayar  # Menyimpan metode pembayaran

    def tambah_produk(self, produk, jumlah):
        # Menambahkan produk yang dijual ke dalam transaksi
        self.tambah_item({
            "nama_produk": produk.nama_produk,
            "harga": produk.harga,
            "jumlah": jumlah
        }, jumlah)

    def hitung_total(self):
        # Menghitung total harga dari seluruh produk yang dijual
        self.total_harga = 0
        for item in self.daftar_item:
            self.total_harga += item["harga"] * item["jumlah"]
        return self.total_harga

    def cetak_struk(self):
        # Menampilkan struk penjualan ke layar
        print("\n===== STRUK PENJUALAN =====")
        print(f"ID Transaksi : {self.id_transaksi}")
        print(f"Tanggal      : {self.tanggal_transaksi}")
        print("---------------------------")

        for item in self.daftar_item:
            print(f"{item['nama_produk']} x{item['jumlah']} "
                  f"= Rp {item['harga'] * item['jumlah']}")

        print("---------------------------")
        print(f"Total Harga  : Rp {self.hitung_total()}")
        print(f"Metode Bayar : {self.metode_bayar}")
        print("===========================\n")

# =========================
# CLASS PEMBELIAN
# =========================        
class Pembelian(Transaksi):
    # Class Pembelian Subclass dari Transaksi Merepresentasikan transaksi pembelian bahan baku dari supplier

    def __init__(self, id_transaksi, kode_supplier):
        # Memanggil constructor Transaksi(inheritance)
        super().__init__(id_transaksi)
        self.total_beli = 0           # Menyimpan total pembelian
        self.kode_supplier = kode_supplier  # Menyimpan kode supplier

    def tambah_bahan(self, bahan_baku, jumlah, harga_satuan):
        # Menambahkan bahan baku yang dibeli ke dalam transaksi
        self.tambah_item({
            "nama_bahan": bahan_baku.nama_bahan,
            "jumlah": jumlah,
            "harga_satuan": harga_satuan
        }, jumlah)

    def konfirmasi_pembelian(self):
        # Menghitung total biaya pembelian bahan baku
        self.total_beli = 0
        for item in self.daftar_item:
            self.total_beli += item["jumlah"] * item["harga_satuan"]
        return self.total_beli

# =========================
# BASE PRODUCT (INHERITANCE)
# =========================
class Product:
    def __init__(self, name, kategori, price, recipe):
        self.name = name
        self.kategori = kategori
        self.price = price
        # recipe = {bahan: {qty, unit, note}}
        self.recipe = recipe

    def get_recipe(self):
        return self.recipe

    # POLYMORPHISM (bisa dioverride)
    def get_label(self):
        return self.kategori

    def show_recipe_table(self):
        print("\n======================= DETAIL RESEP MENU =======================")
        print(f"Menu     : {self.name}")
        print(f"Kategori : {self.kategori}")
        print(f"Harga    : Rp{self.price}")
        print("-----------------------------------------------------------------")
        print("| No | Nama Bahan        | Jumlah | Satuan | Keterangan |")
        print("-----------------------------------------------------------------")

        for i, (bahan, data) in enumerate(self.recipe.items(), start=1):
            print(
                f"| {i:<2} | {bahan:<18} | "
                f"{data['qty']:<6} | {data['unit']:<6} | "
                f"{data.get('note', '-'):<10} |"
            )

        print("=================================================================")


# =========================
# SUBCLASS (POLYMORPHISM)
# =========================
class CoffeeProduct(Product):
    def get_label(self):
        return "Coffee"


class NonCoffeeProduct(Product):
    def get_label(self):
        return "Non-Coffee"


class PastryProduct(Product):
    def get_label(self):
        return "Pastry"


# =========================
# FACTORY
# =========================
class ProductFactory:
    @staticmethod
    def create_product(name, kategori, price, recipe):
        kategori = kategori.lower()
        if kategori == "coffee":
            return CoffeeProduct(name, kategori, price, recipe)
        elif kategori == "non-coffee":
            return NonCoffeeProduct(name, kategori, price, recipe)
        elif kategori == "pastry":
            return PastryProduct(name, kategori, price, recipe)
        else:
            return Product(name, kategori, price, recipe)


# =========================
# PRODUCT MANAGER
# =========================
class ProductManager:
    def __init__(self):
        self.products = []

    # ITERATOR
    def __iter__(self):
        return iter(self.products)

    def add_product(self, product):
        self.products.append(product)

    def hapus_produk(self, nama):
        for product in self.products:
            if product.name.lower() == nama.lower():
                self.products.remove(product)
                return
        raise ValueError("Produk tidak ditemukan")

    @highlight_menu
    def show_products(self):
        print("\n================ DAFTAR PRODUK =================")
        print("| No | Nama Produk     | Harga    | Kategori        |")
        print("--------------------------------------------------")

        if not self.products:
            print("| -- | BELUM ADA PRODUK                         |")
        else:
            for i, product in enumerate(self.products, start=1):
                print(
                    f"| {i:<2} | {product.name:<15} | "
                    f"Rp{product.price:<7} | {product.get_label():<14} |"
                )

        print("================================================")

    # ambil produk berdasarkan pilihan user
    def get_product_by_index(self, index):
        if 0 <= index < len(self.products):
            return self.products[index]
        return None

# =========================
# EXCEPTION
# =========================
class StokTidakCukupError(Exception):
    pass


# =========================
# OBSERVER
# =========================
class Observer:
    def update(self, message):
        pass


class NotifikasiStok(Observer):
    def update(self, message):
        print(f"[NOTIFIKASI] {message}")


# =========================
# STRATEGY STATUS STOK
# =========================
class StatusStrategy:
    def get_status(self, jumlah):
        pass


class DefaultStatusStrategy(StatusStrategy):
    def get_status(self, jumlah):
        if jumlah <= 0:
            return "HABIS"
        elif jumlah <= 10:
            return "MENIPIS"
        return "AMAN"


# =========================
# INVENTORY (SINGLETON)
# =========================
class ManajemenPersediaan:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ManajemenPersediaan, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized"):
            return
        self._initialized = True

        # =========================
        # STOK AWAL BAHAN
        # =========================
        self.stock = {
            "Bubuk Kopi": {"qty": 10000, "unit": "gram"},
            "Air": {"qty": 200000, "unit": "ml"},
            "Susu Full Cream": {"qty": 100000, "unit": "ml"},
            "Susu Oat": {"qty": 30000, "unit": "ml"},
            "Gula Aren": {"qty": 5000, "unit": "gram"},
            "Caramel Syrup": {"qty": 5000, "unit": "ml"},
            "Coklat Bubuk": {"qty": 3000, "unit": "gram"},
            "Matcha Powder": {"qty": 2000, "unit": "gram"},
            "Tepung Terigu": {"qty": 10000, "unit": "gram"},
            "Mentega": {"qty": 5000, "unit": "gram"},
            "Cup": {"qty": 500, "unit": "pcs"},
            "Sedotan Hitam": {"qty": 500, "unit": "pcs"}
        }

        # =========================
        # ALIAS
        # =========================
        self.alias = {
            "Susu": "Susu Full Cream",
            "Kopi": "Bubuk Kopi",
            "Cup Plastik": "Cup",
            "Sedotan": "Sedotan Hitam"
        }

        # =========================
        # LOG & OBSERVER
        # =========================
        self.log_tambah = []
        self.observers = []

        # =========================
        # STRATEGY
        # =========================
        self.status_strategy = DefaultStatusStrategy()

    # =========================
    # ITERATOR
    # =========================
    def __iter__(self):
        return iter(self.stock.items())

    # =========================
    # OBSERVER METHOD
    # =========================
    def tambah_observer(self, observer: Observer):
        self.observers.append(observer)

    def _notify(self, message):
        for obs in self.observers:
            obs.update(message)

    # =========================
    # NORMALISASI NAMA
    # =========================
    def _normalize_bahan(self, bahan):
        bahan = bahan.strip()
        return self.alias.get(bahan, bahan)

    # =========================
    # RESTOCK
    # =========================
    def add_stock(self, bahan, jumlah):
        bahan = self._normalize_bahan(bahan)

        if jumlah <= 0:
            raise ValueError("Jumlah stok harus lebih dari 0")

        if bahan not in self.stock:
            if "Powder" in bahan or "Bubuk" in bahan:
                unit = "gram"
            elif "Syrup" in bahan or "Susu" in bahan or "Air" in bahan:
                unit = "ml"
            else:
                unit = "pcs"

            self.stock[bahan] = {"qty": 0, "unit": unit}

        self.stock[bahan]["qty"] += jumlah
        self.log_tambah.append(f"+{jumlah} {self.stock[bahan]['unit']} {bahan}")
        self._notify("Stok bahan telah diperbarui")

    # =========================
    # PAKAI STOK
    # =========================
    def use_stock(self, bahan, jumlah):
        bahan = self._normalize_bahan(bahan)

        if bahan not in self.stock:
            raise StokTidakCukupError(f"Bahan '{bahan}' tidak tersedia")

        if jumlah <= 0:
            raise ValueError("Jumlah pemakaian harus lebih dari 0")

        if self.stock[bahan]["qty"] < jumlah:
            raise StokTidakCukupError(
                f"Stok {bahan} tidak cukup (tersedia {self.stock[bahan]['qty']})"
            )

        self.stock[bahan]["qty"] -= jumlah

        status = self.get_status(self.stock[bahan]["qty"])
        if status in ["MENIPIS", "HABIS"]:
            self._notify(f"Stok {bahan} {status}")

    # =========================
    # STATUS (STRATEGY)
    # =========================
    def get_status(self, jumlah):
        return self.status_strategy.get_status(jumlah)

    # =========================
    # TABEL STOK (FIXED & RAPI)
    # =========================
    def show_stock_table(self):
        print("\n===================== STOK BAHAN =====================")
        print("| No | Nama Bahan           | Jumlah      | Satuan | Status  |")
        print("-------------------------------------------------------")

        for i, (bahan, data) in enumerate(self.stock.items(), start=1):
            jumlah = data["qty"]
            satuan = data["unit"]
            status = self.get_status(jumlah)

            print(
                f"| {i:<2} | {bahan:<20} | "
                f"{jumlah:>11} | {satuan:^6} | {status:^7} |"
            )

        print("======================================================")


# =========================
# EXCEPTION
# =========================
class StokTidakCukupError(Exception):
    pass


# =========================
# OBSERVER
# =========================
class Observer:
    def update(self, message):
        pass


class NotifikasiStok(Observer):
    def update(self, message):
        print(f"[NOTIFIKASI] {message}")


# =========================
# STRATEGY STATUS STOK
# =========================
class StatusStrategy:
    def get_status(self, jumlah):
        pass


class DefaultStatusStrategy(StatusStrategy):
    def get_status(self, jumlah):
        if jumlah <= 0:
            return "HABIS"
        elif jumlah <= 10:
            return "MENIPIS"
        return "AMAN"


# =========================
# INVENTORY (SINGLETON)
# =========================
class ManajemenPersediaan:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ManajemenPersediaan, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized"):
            return
        self._initialized = True

        # =========================
        # STOK AWAL BAHAN
        # =========================
        self.stock = {
            "Bubuk Kopi": {"qty": 10000, "unit": "gram"},
            "Air": {"qty": 200000, "unit": "ml"},
            "Susu Full Cream": {"qty": 100000, "unit": "ml"},
            "Susu Oat": {"qty": 30000, "unit": "ml"},
            "Gula Aren": {"qty": 5000, "unit": "gram"},
            "Caramel Syrup": {"qty": 5000, "unit": "ml"},
            "Coklat Bubuk": {"qty": 3000, "unit": "gram"},
            "Matcha Powder": {"qty": 2000, "unit": "gram"},
            "Tepung Terigu": {"qty": 10000, "unit": "gram"},
            "Mentega": {"qty": 5000, "unit": "gram"},
            "Cup": {"qty": 500, "unit": "pcs"},
            "Sedotan Hitam": {"qty": 500, "unit": "pcs"}
        }

        # =========================
        # ALIAS
        # =========================
        self.alias = {
            "Susu": "Susu Full Cream",
            "Kopi": "Bubuk Kopi",
            "Cup Plastik": "Cup",
            "Sedotan": "Sedotan Hitam"
        }

        # =========================
        # LOG & OBSERVER
        # =========================
        self.log_tambah = []
        self.observers = []

        # =========================
        # STRATEGY
        # =========================
        self.status_strategy = DefaultStatusStrategy()

    # =========================
    # ITERATOR
    # =========================
    def __iter__(self):
        return iter(self.stock.items())

    # =========================
    # OBSERVER METHOD
    # =========================
    def tambah_observer(self, observer: Observer):
        self.observers.append(observer)

    def _notify(self, message):
        for obs in self.observers:
            obs.update(message)

    # =========================
    # NORMALISASI NAMA
    # =========================
    def _normalize_bahan(self, bahan):
        bahan = bahan.strip()
        return self.alias.get(bahan, bahan)

    # =========================
    # RESTOCK
    # =========================
    def add_stock(self, bahan, jumlah):
        bahan = self._normalize_bahan(bahan)

        if jumlah <= 0:
            raise ValueError("Jumlah stok harus lebih dari 0")

        if bahan not in self.stock:
            if "Powder" in bahan or "Bubuk" in bahan:
                unit = "gram"
            elif "Syrup" in bahan or "Susu" in bahan or "Air" in bahan:
                unit = "ml"
            else:
                unit = "pcs"

            self.stock[bahan] = {"qty": 0, "unit": unit}

        self.stock[bahan]["qty"] += jumlah
        self.log_tambah.append(f"+{jumlah} {self.stock[bahan]['unit']} {bahan}")
        self._notify("Stok bahan telah diperbarui")

    # =========================
    # PAKAI STOK
    # =========================
    def use_stock(self, bahan, jumlah):
        bahan = self._normalize_bahan(bahan)

        if bahan not in self.stock:
            raise StokTidakCukupError(f"Bahan '{bahan}' tidak tersedia")

        if jumlah <= 0:
            raise ValueError("Jumlah pemakaian harus lebih dari 0")

        if self.stock[bahan]["qty"] < jumlah:
            raise StokTidakCukupError(
                f"Stok {bahan} tidak cukup (tersedia {self.stock[bahan]['qty']})"
            )

        self.stock[bahan]["qty"] -= jumlah

        status = self.get_status(self.stock[bahan]["qty"])
        if status in ["MENIPIS", "HABIS"]:
            self._notify(f"Stok {bahan} {status}")

    # =========================
    # STATUS (STRATEGY)
    # =========================
    def get_status(self, jumlah):
        return self.status_strategy.get_status(jumlah)

    # =========================
    # TABEL STOK (FIXED & RAPI)
    # =========================
    def show_stock_table(self):
        print("\n===================== STOK BAHAN =====================")
        print("| No | Nama Bahan           | Jumlah      | Satuan | Status  |")
        print("-------------------------------------------------------")

        for i, (bahan, data) in enumerate(self.stock.items(), start=1):
            jumlah = data["qty"]
            satuan = data["unit"]
            status = self.get_status(jumlah)

            print(
                f"| {i:<2} | {bahan:<20} | "
                f"{jumlah:>11} | {satuan:^6} | {status:^7} |"
            )

        print("======================================================")


from inventory import ManajemenPersediaan, StokTidakCukupError
from product import ProductManager, ProductFactory


# ===============================
# INISIALISASI (Singleton Inventory)
# ===============================
inventory = ManajemenPersediaan()
product_manager = ProductManager()


# ===============================
# CONTOH PRODUK & RESEP (AUTO)
# ===============================
latte_recipe = {
    "Bubuk Kopi": {"qty": 18, "unit": "gram", "note": "Espresso"},
    "Susu Full Cream": {"qty": 150, "unit": "ml", "note": "Steamed"},
    "Air": {"qty": 30, "unit": "ml", "note": "Hot"},
    "Cup": {"qty": 1, "unit": "pcs", "note": "Packaging"}
}

americano_recipe = {
    "Bubuk Kopi": {"qty": 18, "unit": "gram", "note": "Espresso"},
    "Air": {"qty": 180, "unit": "ml", "note": "Hot Water"},
    "Cup": {"qty": 1, "unit": "pcs", "note": "Packaging"}
}

taro_latte_recipe = {
    "Taro Powder": {"qty": 25, "unit": "gram", "note": "Flavor"},
    "Susu Full Cream": {"qty": 150, "unit": "ml", "note": "Milk Base"},
    "Cup": {"qty": 1, "unit": "pcs", "note": "Packaging"}
}

croissant_recipe = {
    "Tepung Terigu": {"qty": 120, "unit": "gram", "note": "Dough"},
    "Mentega": {"qty": 30, "unit": "gram", "note": "Butter"}
}

# pakai FACTORY
product_manager.add_product(ProductFactory.create_product(
    "Latte", "coffee", 22000, latte_recipe
))
product_manager.add_product(ProductFactory.create_product(
    "Americano", "coffee", 20000, americano_recipe
))
product_manager.add_product(ProductFactory.create_product(
    "Taro Latte", "non-coffee", 23000, taro_latte_recipe
))
product_manager.add_product(ProductFactory.create_product(
    "Croissant", "pastry", 15000, croissant_recipe
))


# ===============================
# TAMPILKAN STOK AWAL
# ===============================
print("\nSTOK AWAL BAHAN")
inventory.show_stock_table()


# ===============================
# MENU UTAMA
# ===============================
def tampilkan_menu():
    print("\n=== SISTEM COFFEE SHOP ===")
    print("1. Tambah / Restock Bahan")
    print("2. Lihat Stok Bahan")
    print("3. Tambah Produk")
    print("4. Lihat Daftar Produk")
    print("5. Cari Bahan")
    print("6. Jual Menu")
    print("7. Hapus Produk")
    print("8. Keluar")


# ===============================
# LOOP PROGRAM
# ===============================
while True:
    tampilkan_menu()
    pilihan = input("Pilih menu (1-8): ")
    
    # ===============================
    # 1. RESTOCK
    # ===============================
    if pilihan == "1":
        try:
            bahan = input("Nama bahan: ")
            jumlah = int(input("Jumlah: "))
            inventory.add_stock(bahan, jumlah)
            inventory.show_stock_table()
        except ValueError as e:
            print("Error:", e)

    # ===============================
    # 2. LIHAT STOK
    # ===============================
    elif pilihan == "2":
        inventory.show_stock_table()

    # ===============================
    # 3. TAMBAH PRODUK
    # ===============================
    elif pilihan == "3":
        nama = input("Nama produk: ")

        print("\nPilih Kategori:")
        print("1. Coffee")
        print("2. Non-Coffee")
        print("3. Pastry")

        pil = input("Pilihan (1-3): ")
        if pil == "1":
            kategori = "coffee"
        elif pil == "2":
            kategori = "non-coffee"
        elif pil == "3":
            kategori = "pastry"
        else:
            print("Kategori tidak valid!")
            continue

        try:
            harga = int(input("Harga: "))
        except ValueError:
            print("Harga harus angka!")
            continue

        recipe = {}
        print("\nTambah Resep (contoh: Bubuk Kopi = 10 gram Espresso)")
        print("Ketik 'stop' jika selesai")

        while True:
            data = input("> ").strip()
            if data.lower() == "stop":
                break

            try:
                bahan, detail = data.split("=")
                parts = detail.strip().split()

                recipe[bahan.strip()] = {
                    "qty": int(parts[0]),
                    "unit": parts[1],
                    "note": parts[2] if len(parts) > 2 else "-"
                }
            except:
                print("Format salah!")

        product_manager.add_product(
            ProductFactory.create_product(nama, kategori, harga, recipe)
        )
        print("Produk berhasil ditambahkan")

    # ===============================
    # 4. LIHAT PRODUK
    # ===============================
    elif pilihan == "4":
        product_manager.show_products()

    # ===============================
    # 5. CARI BAHAN
    # ===============================
    elif pilihan == "5":
        nama = input("Nama bahan: ")
        hasil = inventory.cari_bahan(nama)
        if hasil:
            print(f"Stok {nama}: {hasil['qty']} {hasil['unit']}")
        else:
            print("Bahan tidak ditemukan")

    # ===============================
    # 6. JUAL MENU
    # ===============================
    elif pilihan == "6":
        product_manager.show_products()
        try:
            pilih = int(input("Pilih nomor menu: ")) - 1
            product = product_manager.get_product_by_index(pilih)

            if not product:
                print("Menu tidak valid")
                continue

            product.show_recipe_table()

            # cek & kurangi stok
            for bahan, data in product.recipe.items():
                inventory.use_stock(bahan, data["qty"])

            print("\n Stok bahan telah diperbarui")
            print(f"{product.name} BERHASIL DIJUAL | Rp{product.price}")

        except StokTidakCukupError as e:
            print("\n GAGAL MENJUAL PRODUK")
            print("Alasan:", e)

        except ValueError:
            print("Input tidak valid")

    # ===============================
    # 7. HAPUS PRODUK
    # ===============================
    elif pilihan == "7":
        nama = input("Nama produk yang ingin dihapus: ")
        try:
            product_manager.hapus_produk(nama)
            print(f"Produk '{nama}' berhasil dihapus")
        except ValueError as e:
            print(e)

    # ===============================
    # 8. KELUAR
    # ===============================
    elif pilihan == "8":
        print("Program selesai. Terima kasih")
        break

    else:
        print("Menu tidak valid!")
