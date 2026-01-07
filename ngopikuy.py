# =========================
# SISTEM MANAJEMEN COFFEE SHOP - NGOPIKUY
# Pemrograman Berbasis Object - UTS
# =========================
from datetime import datetime


# =========================
# BASE CLASS TRANSAKSI
# =========================
class Transaksi:
    # Base class untuk semua jenis transaksi
    def __init__(self, id_transaksi):
        self.id_transaksi = id_transaksi
        self.tanggal_transaksi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.daftar_item = []

    def tambah_item(self, item, jumlah):
        # Menambahkan item ke dalam transaksi
        self.daftar_item.append(item)


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
            "nama_produk": produk.name,
            "harga": produk.price,
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
        print("\n" + "="*40)
        print("NGOPIKUY COFFEE SHOP".center(40))
        print("="*40)
        print(f"ID Transaksi : {self.id_transaksi}")
        print(f"Tanggal      : {self.tanggal_transaksi}")
        print("-" * 40)

        for item in self.daftar_item:
            print(f"{item['nama_produk']} x{item['jumlah']} "
                  f"= Rp {item['harga'] * item['jumlah']:,}")

        print("-" * 40)
        print(f"Total Harga  : Rp {self.hitung_total():,}")
        print(f"Metode Bayar : {self.metode_bayar}")
        print("="*40 + "\n")


class Pembelian(Transaksi):
    # Class Pembelian Subclass dari Transaksi Merepresentasikan transaksi pembelian bahan baku dari supplier

    def __init__(self, id_transaksi, kode_supplier):
        # Memanggil constructor Transaksi (inheritance)
        super().__init__(id_transaksi)
        self.total_beli = 0           # Menyimpan total pembelian
        self.kode_supplier = kode_supplier  # Menyimpan kode supplier

    def tambah_bahan(self, bahan_baku, jumlah, harga_satuan):
        # Menambahkan bahan baku yang dibeli ke dalam transaksi
        self.tambah_item({
            "nama_bahan": bahan_baku,
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
            "Taro Powder": {"qty": 2000, "unit": "gram"},
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
    # CARI BAHAN
    # =========================
    def cari_bahan(self, nama):
        nama = self._normalize_bahan(nama)
        return self.stock.get(nama)

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
        self._notify(f"Stok {bahan} telah diperbarui")

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
            self._notify(f"⚠ Stok {bahan} {status}!")

    # =========================
    # STATUS (STRATEGY)
    # =========================
    def get_status(self, jumlah):
        return self.status_strategy.get_status(jumlah)

    # =========================
    # TABEL STOK (FIXED & RAPI)
    # =========================
    def show_stock_table(self):
        print("\n" + "="*70)
        print("STOK BAHAN - NGOPIKUY".center(70))
        print("="*70)
        print(f"| {'No':<3} | {'Nama Bahan':<20} | {'Jumlah':>10} | {'Satuan':^8} | {'Status':^8} |")
        print("-"*70)

        for i, (bahan, data) in enumerate(self.stock.items(), start=1):
            jumlah = data["qty"]
            satuan = data["unit"]
            status = self.get_status(jumlah)

            print(
                f"| {i:<3} | {bahan:<20} | "
                f"{jumlah:>10} | {satuan:^8} | {status:^8} |"
            )

        print("="*70)


# =========================
# DECORATOR
# =========================
def highlight_menu(func):
    def wrapper(*args, **kwargs):
        print("\n━━━ MENU PILIHAN ━━━")
        return func(*args, **kwargs)
    return wrapper


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
        print("\n" + "="*75)
        print("DETAIL RESEP MENU - NGOPIKUY".center(75))
        print("="*75)
        print(f"Menu     : {self.name}")
        print(f"Kategori : {self.kategori}")
        print(f"Harga    : Rp {self.price:,}")
        print("-"*75)
        print(f"| {'No':<3} | {'Nama Bahan':<20} | {'Jumlah':>8} | {'Satuan':^8} | {'Keterangan':<15} |")
        print("-"*75)

        for i, (bahan, data) in enumerate(self.recipe.items(), start=1):
            print(
                f"| {i:<3} | {bahan:<20} | "
                f"{data['qty']:>8} | {data['unit']:^8} | "
                f"{data.get('note', '-'):<15} |"
            )

        print("="*75)


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
        print("\n" + "="*65)
        print("DAFTAR PRODUK - NGOPIKUY".center(65))
        print("="*65)
        print(f"| {'No':<3} | {'Nama Produk':<20} | {'Harga':>12} | {'Kategori':<18} |")
        print("-"*65)

        if not self.products:
            print(f"| {'--':<3} | {'BELUM ADA PRODUK':<20} | {' ':>12} | {' ':<18} |")
        else:
            for i, product in enumerate(self.products, start=1):
                print(
                    f"| {i:<3} | {product.name:<20} | "
                    f"Rp {product.price:>9,} | {product.get_label():<18} |"
                )

        print("="*65)

    # ambil produk berdasarkan pilihan user
    def get_product_by_index(self, index):
        if 0 <= index < len(self.products):
            return self.products[index]
        return None


# =========================
# TRANSACTION MANAGER
# =========================
class TransaksiManager:
    """Class untuk mengelola riwayat transaksi"""
    
    def __init__(self):
        self.riwayat_penjualan = []
        self.riwayat_pembelian = []
    
    def tambah_penjualan(self, transaksi):
        """Menambahkan transaksi penjualan ke riwayat"""
        self.riwayat_penjualan.append(transaksi)
    
    def tambah_pembelian(self, transaksi):
        """Menambahkan transaksi pembelian ke riwayat"""
        self.riwayat_pembelian.append(transaksi)
    
    def tampilkan_riwayat_penjualan(self):
        """Menampilkan semua riwayat penjualan"""
        print("\n" + "="*60)
        print("RIWAYAT PENJUALAN - NGOPIKUY".center(60))
        print("="*60)
        if not self.riwayat_penjualan:
            print("Belum ada transaksi penjualan")
        else:
            for i, trx in enumerate(self.riwayat_penjualan, 1):
                print(f"\n--- Penjualan #{i} ---")
                trx.cetak_struk()
    
    def tampilkan_riwayat_pembelian(self):
        """Menampilkan semua riwayat pembelian"""
        print("\n" + "="*60)
        print("RIWAYAT PEMBELIAN - NGOPIKUY".center(60))
        print("="*60)
        if not self.riwayat_pembelian:
            print("Belum ada transaksi pembelian")
        else:
            for i, trx in enumerate(self.riwayat_pembelian, 1):
                print(f"\n--- Pembelian #{i} ---")
                print(f"ID Transaksi: {trx.id_transaksi}")
                print(f"Tanggal: {trx.tanggal_transaksi}")
                print(f"Supplier: {trx.kode_supplier}")
                print(f"Total: Rp {trx.konfirmasi_pembelian():,}")
                print("-" * 40)


# =========================
# LAPORAN DAN ANALISIS
# =========================
class LaporanManager:
    """Class untuk mengelola laporan dan analisis"""
    
    @staticmethod
    def laporan_penjualan_harian(transaksi_manager):
        """Membuat laporan penjualan harian"""
        print("\n" + "="*60)
        print("LAPORAN PENJUALAN HARIAN - NGOPIKUY".center(60))
        print("="*60)
        total_pendapatan = 0
        total_transaksi = len(transaksi_manager.riwayat_penjualan)
        
        if total_transaksi == 0:
            print("Belum ada transaksi penjualan hari ini")
            return
        
        for trx in transaksi_manager.riwayat_penjualan:
            total_pendapatan += trx.hitung_total()
        
        print(f"Total Transaksi      : {total_transaksi}")
        print(f"Total Pendapatan     : Rp {total_pendapatan:,}")
        print(f"Rata-rata/Transaksi  : Rp {total_pendapatan//total_transaksi:,}")
        print("=" * 60)
    
    @staticmethod
    def laporan_stok_menipis(inventory):
        """Menampilkan bahan yang stoknya menipis"""
        print("\n" + "="*60)
        print("LAPORAN STOK MENIPIS - NGOPIKUY".center(60))
        print("="*60)
        ada_menipis = False
        
        for bahan, data in inventory.stock.items():
            status = inventory.get_status(data["qty"])
            if status in ["MENIPIS", "HABIS"]:
                print(f"⚠ {bahan:<20} : {data['qty']:>6} {data['unit']:<6} [{status}]")
                ada_menipis = True
        
        if not ada_menipis:
            print("✓ Semua stok dalam kondisi aman")
        print("=" * 60)


# ===============================
# INISIALISASI (Singleton Inventory)
# ===============================
inventory = ManajemenPersediaan()
product_manager = ProductManager()
transaksi_manager = TransaksiManager()
laporan_manager = LaporanManager()
riwayat_transaksi = []

# Setup observer untuk notifikasi stok
notif_stok = NotifikasiStok()
inventory.tambah_observer(notif_stok)


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

# Pakai FACTORY untuk membuat produk
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
print("\n" + "="*70)
print("SISTEM MANAJEMEN COFFEE SHOP".center(70))
print("NGOPIKUY".center(70))
print("="*70)
print("\n📦 STOK AWAL BAHAN")
inventory.show_stock_table()


# ===============================
# MENU UTAMA
# ===============================
def tampilkan_menu():
    print("\n" + "="*70)
    print("SISTEM MANAJEMEN NGOPIKUY".center(70))
    print("="*70)
    print("1. Tambah / Restock Bahan")
    print("2. Lihat Stok Bahan")
    print("3. Tambah Produk")
    print("4. Lihat Daftar Produk")
    print("5. Cari Bahan")
    print("6. Jual Menu (Penjualan)")
    print("7. Beli Bahan dari Supplier (Pembelian)")
    print("8. Hapus Produk")
    print("9. Laporan & Analisis")
    print("10. Keluar")
    print("="*70)


# ===============================
# FUNGSI UTAMA
# ===============================
def main():
    """Fungsi utama untuk menjalankan sistem"""
    global riwayat_transaksi
    
    print("\n☕ Selamat datang di Sistem Operasi Ngopikuy!")
    input("\nTekan Enter untuk melanjutkan...")
    
    while True:
        tampilkan_menu()
        pilihan = input("\nPilih menu (1-10): ").strip()

        # ===============================
        # 1. RESTOCK
        # ===============================
        if pilihan == "1":
            print("\n" + "="*60)
            print("RESTOCK BAHAN - NGOPIKUY".center(60))
            print("="*60)
            try:
                bahan = input("Nama bahan: ")
                jumlah = int(input("Jumlah: "))
                inventory.add_stock(bahan, jumlah)
                print(f"✓ Berhasil menambah {jumlah} {bahan}")
                inventory.show_stock_table()
            except ValueError:
                print("❌ ERROR: Jumlah Harus Berupa Angka!")

        # ===============================
        # 2. LIHAT STOK
        # ===============================
        elif pilihan == "2":
            inventory.show_stock_table()

        # ===============================
        # 3. TAMBAH PRODUK
        # ===============================
        elif pilihan == "3":
            print("\n" + "="*60)
            print("TAMBAH PRODUK BARU - NGOPIKUY".center(60))
            print("="*60)
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
                print("❌ Kategori tidak valid!")
                continue

            try:
                harga = int(input("Harga: "))
            except ValueError:
                print("❌ Harga harus angka!")
                continue

            recipe = {}
            print("\nTambah Resep (CONTOH: Bubuk Kopi = 10 gram Espresso)")
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
                    print("❌ Format salah! Gunakan: Bahan = jumlah satuan keterangan")

            product_manager.add_product(
                ProductFactory.create_product(nama, kategori, harga, recipe)
            )
            print(f"✓ Produk '{nama}' berhasil ditambahkan")

        # ===============================
        # 4. LIHAT PRODUK
        # ===============================
        elif pilihan == "4":
            product_manager.show_products()

        # ===============================
        # 5. CARI BAHAN
        # ===============================
        elif pilihan == "5":
            print("\n" + "="*60)
            print("CARI BAHAN - NGOPIKUY".center(60))
            print("="*60)
            nama = input("Nama bahan: ")
            hasil = inventory.cari_bahan(nama)
            if hasil:
                status = inventory.get_status(hasil['qty'])
                print(f"\n✓ Bahan ditemukan!")
                print(f"  Nama   : {nama}")
                print(f"  Stok   : {hasil['qty']} {hasil['unit']}")
                print(f"  Status : {status}")
            else:
                print(f"❌ Bahan '{nama}' tidak ditemukan")

        # ===============================
        # 6. JUAL MENU
        # ===============================
        elif pilihan == "6":
            print("\n" + "="*60)
            print("TRANSAKSI PENJUALAN - NGOPIKUY".center(60))
            print("="*60)
            product_manager.show_products()
            
            try:
                pilih = int(input("\nPilih nomor menu: ")) - 1
                product = product_manager.get_product_by_index(pilih)

                if not product:
                    print("❌ Menu tidak valid")
                    continue

                jumlah_order = int(input("Jumlah pesanan: "))
                if jumlah_order <= 0:
                    print("❌ Jumlah harus lebih dari 0")
                    continue

                # Tampilkan detail resep
                product.show_recipe_table()

                # Buat transaksi penjualan
                metode_bayar = input("\nMetode Pembayaran (Tunai/Debit/QRIS): ")
                transaksi = Penjualan(f"TRX-{len(riwayat_transaksi)+1:04d}", metode_bayar)
                
                # Cek & kurangi stok untuk setiap pesanan
                try:
                    for _ in range(jumlah_order):
                        for bahan, data in product.recipe.items():
                            inventory.use_stock(bahan, data["qty"])
                        transaksi.tambah_produk(product, 1)
                    
                    # Cetak struk
                    transaksi.cetak_struk()
                    
                    # Simpan ke riwayat
                    riwayat_transaksi.append(transaksi)
                    transaksi_manager.tambah_penjualan(transaksi)
                    
                    print(f"✓ {product.name} x{jumlah_order} BERHASIL DIJUAL | Total: Rp {transaksi.hitung_total():,}")
                    
                except StokTidakCukupError as e:
                    print("\n❌ GAGAL MENJUAL PRODUK")
                    print(f"Alasan: {e}")
                    continue

            except StokTidakCukupError as e:
                print("\n❌ GAGAL MENJUAL PRODUK")
                print(f"Alasan: {e}")

            except ValueError:
                print("❌ Input tidak valid")

        # ===============================
        # 7. BELI BAHAN DARI SUPPLIER (PEMBELIAN)
        # ===============================
        elif pilihan == "7":
            print("\n" + "="*60)
            print("TRANSAKSI PEMBELIAN - NGOPIKUY".center(60))
            print("="*60)
            
            # Input supplier
            kode_supplier = input("Kode/Nama Supplier: ").strip()
            if not kode_supplier:
                print("❌ Kode supplier harus diisi!")
                continue
            
            # Buat transaksi pembelian
            id_pembelian = f"BUY-{len(transaksi_manager.riwayat_pembelian)+1:04d}"
            transaksi_beli = Pembelian(id_pembelian, kode_supplier)
            
            print("\nMasukkan bahan yang dibeli (ketik 'selesai' untuk mengakhiri)")
            
            while True:
                print("\n" + "-"*60)
                nama_bahan = input("Nama bahan (atau 'selesai'): ").strip()
                
                if nama_bahan.lower() == 'selesai':
                    break
                
                try:
                    jumlah = int(input("Jumlah: "))
                    if jumlah <= 0:
                        print("❌ Jumlah harus lebih dari 0")
                        continue
                    
                    harga_satuan = int(input("Harga per satuan: Rp "))
                    if harga_satuan <= 0:
                        print("❌ Harga harus lebih dari 0")
                        continue
                    
                    # Tambahkan bahan ke transaksi
                    transaksi_beli.tambah_bahan(nama_bahan, jumlah, harga_satuan)
                    
                    # Tambahkan ke inventory
                    try:
                        inventory.add_stock(nama_bahan, jumlah)
                        subtotal = jumlah * harga_satuan
                        print(f"✓ {nama_bahan} x {jumlah} = Rp {subtotal:,} ditambahkan")
                    except ValueError as e:
                        print(f"⚠ Warning: {e}")
                        
                except ValueError:
                    print("❌ ERROR: Input Harus Berupa Angka!")
            
            # Konfirmasi dan cetak struk pembelian
            if transaksi_beli.daftar_item:
                print("\n" + "="*60)
                print("STRUK PEMBELIAN - NGOPIKUY".center(60))
                print("="*60)
                print(f"ID Transaksi : {transaksi_beli.id_transaksi}")
                print(f"Tanggal      : {transaksi_beli.tanggal_transaksi}")
                print(f"Supplier     : {transaksi_beli.kode_supplier}")
                print("-"*60)
                
                for item in transaksi_beli.daftar_item:
                    subtotal = item['jumlah'] * item['harga_satuan']
                    print(f"{item['nama_bahan']:<25} x{item['jumlah']:<5} @ Rp {item['harga_satuan']:>8,} = Rp {subtotal:>10,}")
                
                print("-"*60)
                total = transaksi_beli.konfirmasi_pembelian()
                print(f"{'TOTAL PEMBELIAN':>50} : Rp {total:>10,}")
                print("="*60)
                
                # Simpan ke riwayat
                transaksi_manager.tambah_pembelian(transaksi_beli)
                print("\n✓ Transaksi pembelian berhasil disimpan!")
            else:
                print("\n❌ Tidak ada bahan yang dibeli")

        # ===============================
        # 8. HAPUS PRODUK
        # ===============================
        elif pilihan == "8":
            print("\n" + "="*60)
            print("HAPUS PRODUK - NGOPIKUY".center(60))
            print("="*60)
            product_manager.show_products()
            nama = input("\nNama produk yang ingin dihapus: ")
            try:
                product_manager.hapus_produk(nama)
                print(f"✓ Produk '{nama}' berhasil dihapus")
            except ValueError as e:
                print(f"❌ {e}")

        # ===============================
        # 9. LAPORAN & ANALISIS
        # ===============================
        elif pilihan == "9":
            print("\n" + "="*60)
            print("LAPORAN & ANALISIS - NGOPIKUY".center(60))
            print("="*60)
            print("1. Laporan Penjualan Harian")
            print("2. Laporan Pembelian")
            print("3. Laporan Stok Menipis")
            print("4. Riwayat Transaksi Penjualan")
            print("5. Riwayat Transaksi Pembelian")
            print("6. Kembali")
            
            sub_pilihan = input("\nPilih (1-6): ")
            
            if sub_pilihan == "1":
                laporan_manager.laporan_penjualan_harian(transaksi_manager)
            elif sub_pilihan == "2":
                # Laporan pembelian
                print("\n" + "="*60)
                print("LAPORAN PEMBELIAN - NGOPIKUY".center(60))
                print("="*60)
                total_pembelian = 0
                jumlah_transaksi = len(transaksi_manager.riwayat_pembelian)
                
                if jumlah_transaksi == 0:
                    print("Belum ada transaksi pembelian")
                else:
                    for trx in transaksi_manager.riwayat_pembelian:
                        total_pembelian += trx.konfirmasi_pembelian()
                    
                    print(f"Total Transaksi Pembelian : {jumlah_transaksi}")
                    print(f"Total Pengeluaran         : Rp {total_pembelian:,}")
                    print(f"Rata-rata/Transaksi       : Rp {total_pembelian//jumlah_transaksi:,}")
                print("=" * 60)
            elif sub_pilihan == "3":
                laporan_manager.laporan_stok_menipis(inventory)
            elif sub_pilihan == "4":
                transaksi_manager.tampilkan_riwayat_penjualan()
            elif sub_pilihan == "5":
                transaksi_manager.tampilkan_riwayat_pembelian()
            elif sub_pilihan == "6":
                continue
            else:
                print("❌ Pilihan tidak valid")
            
            input("\nTekan Enter untuk kembali...")

        # ===============================
        # 10. KELUAR
        # ===============================
        elif pilihan == "10":
            print("\n" + "="*70)
            print("Terima kasih telah menggunakan sistem!".center(70))
            print("SISTEM OPERASI NGOPIKUY - © 2026".center(70))
            print("="*70)
            break

        else:
            print("❌ Menu tidak valid!")


# ===============================
# JALANKAN PROGRAM
# ===============================
if __name__ == "__main__":
    main()
