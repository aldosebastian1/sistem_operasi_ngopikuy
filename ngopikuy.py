# =========================
# SISTEM MANAJEMEN COFFEE SHOP - NGOPIKUY
# Pemrograman Berbasis Object - UTS
# =========================
from datetime import datetime
import msvcrt


# =========================
# LOGIN SINGLE ADMIN (WINDOWS)
# =========================
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "12345"


def input_password(prompt="Masukkan password: "):
    """Input password dengan karakter ditampilkan sebagai asterisk"""
    print(prompt, end="", flush=True)
    password = ""

    while True:
        char = msvcrt.getch()

        if char == b"\r":
            print()
            break
        elif char == b"\x08":  # Backspace
            if password:
                password = password[:-1]
                print("\b \b", end="", flush=True)
        else: 
            password += char.decode("utf-8")
            print("*", end="", flush=True)

    return password


def login():
    """Login single admin (3 percobaan)"""
    percobaan_maksimal = 3
    percobaan = 0

    while percobaan < percobaan_maksimal:
        print("=" * 50)
        print("    SELAMAT DATANG DI NGOPIKUY - LOGIN PAGE")
        print("=" * 50)

        username = input("Username: ").strip()
        password = input_password("Password: ")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            print("\n" + "=" * 50)
            print("✓ Login berhasil!")
            print(f"Selamat datang, {username.upper()}")
            print("=" * 50 + "\n")
            return username

        percobaan += 1
        sisa = percobaan_maksimal - percobaan

        print("\n" + "=" * 50)
        print("✗ Login gagal!")
        print("Username atau password salah!")
        print("=" * 50 + "\n")

        if sisa > 0:
            print(f"Sisa percobaan: {sisa}\n")

    print("\n❌ Anda telah melebihi batas percobaan login!")
    print("Program akan ditutup.")
    return None


# =========================
# BASE CLASS TRANSAKSI
# =========================
class Transaksi:
    # Base class untuk semua jenis transaksi
    def __init__(self, id_transaksi, username="system"):
        self.id_transaksi = id_transaksi
        self.tanggal_transaksi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.username = username  # Tracking siapa melakukan transaksi
        self.daftar_item = []

    def tambah_item(self, item, jumlah):
        # Menambahkan item ke dalam transaksi
        self.daftar_item.append(item)


class Penjualan(Transaksi):
    # Class penjualan Subclass dari Transaksi merepresentasikan satu transaksi penjualan ke customer
    def __init__(self, id_transaksi, metode_bayar, username="system"):
        # Memanggil constructor Transaksi (inheritance)
        super().__init__(id_transaksi, username)
        self.total_harga = 0          # Menyimpan total harga penjualan
        self.metode_bayar = metode_bayar  # Menyimpan metode pembayaran
        # FASE 2: Status tracking pesanan
        self.status = StatusPesanan.DIBUAT
        self.waktu_dibuat = datetime.now()
        self.waktu_diseduh = None
        self.waktu_siap = None
        self.waktu_selesai = None

    def update_status(self, status_baru, username):
        """Update status pesanan (hanya barista/kasir yang bisa update)"""
        self.status = status_baru
        if status_baru == StatusPesanan.DISEDUH:
            self.waktu_diseduh = datetime.now()
        elif status_baru == StatusPesanan.SIAP:
            self.waktu_siap = datetime.now()
        elif status_baru == StatusPesanan.SELESAI or status_baru == StatusPesanan.BATAL:
            self.waktu_selesai = datetime.now()
        print(f"✓ Status pesanan {self.id_transaksi} diubah menjadi {status_baru} oleh {username}")

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
        # Menampilkan struk penjualan ke layar dengan info lengkap
        print("\n" + "="*50)
        print("NGOPIKUY COFFEE SHOP".center(50))
        print("="*50)
        print(f"ID Transaksi : {self.id_transaksi}")
        print(f"Tanggal      : {self.tanggal_transaksi}")
        print(f"Kasir        : {self.username}")
        print(f"Pembayaran   : {self.metode_bayar}")
        print("-" * 50)

        for item in self.daftar_item:
            subtotal = item['harga'] * item['jumlah']
            print(f"{item['nama_produk']:<25} x{item['jumlah']:<3} Rp {subtotal:>10,}")

        print("-" * 50)
        print(f"{'TOTAL':>40} : Rp {self.hitung_total():>10,}")
        print("="*50 + "\n")


class Pembelian(Transaksi):
    # Class Pembelian Subclass dari Transaksi Merepresentasikan transaksi pembelian bahan baku dari supplier

    def __init__(self, id_transaksi, kode_supplier, username="system"):
        # Memanggil constructor Transaksi (inheritance)
        super().__init__(id_transaksi, username)
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
# ENUM STATUS PESANAN (FASE 2)
# =========================
class StatusPesanan:
    DIBUAT = "DIBUAT"
    DISEDUH = "DISEDUH"
    SIAP = "SIAP"
    SELESAI = "SELESAI"
    BATAL = "BATAL"


# =========================
# AUDIT LOG STOK (FASE 2)
# =========================
class AuditLog:
    def __init__(self, username, aksi, bahan, jumlah, waktu=None):
        self.username = username
        self.aksi = aksi  # "TAMBAH" atau "PAKAI"
        self.bahan = bahan
        self.jumlah = jumlah
        self.waktu = waktu or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def __str__(self):
        return f"[{self.waktu}] {self.username} - {self.aksi} {self.jumlah} {self.bahan}"


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
        # FASE 2: Audit log untuk tracking stok
        self.audit_logs = []

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
        # Cek alias dengan case-insensitive lookup
        bahan_lower = bahan.lower()
        for alias_key, alias_value in self.alias.items():
            if alias_key.lower() == bahan_lower:
                return alias_value
        # Jika tidak ada di alias, cek stok dengan case-insensitive
        for stock_key in self.stock.keys():
            if stock_key.lower() == bahan_lower:
                return stock_key
        # Jika tidak ditemukan, kembalikan bahan original
        return bahan

    # =========================
    # CARI BAHAN
    # =========================
    def cari_bahan(self, nama):
        nama = self._normalize_bahan(nama)
        return self.stock.get(nama)

    # =========================
    # RESTOCK
    # =========================
    def add_stock(self, bahan, jumlah, username="system", unit=None):
        bahan = self._normalize_bahan(bahan)

        if jumlah <= 0:
            raise ValueError("Jumlah stok harus lebih dari 0")

        # Normalisasi satuan dan konversi bila perlu
        unit_use = None
        if unit is not None:
            u = unit.strip().lower()
            if u == "kg":
                # Konversi kg -> gram
                unit_use = "gram"
                jumlah = jumlah * 1000
            elif u in ["gram", "ml", "pcs"]:
                unit_use = u
            else:
                unit_use = unit.strip()  # satuan manual selain standar

        if bahan not in self.stock:
            # Tentukan satuan untuk bahan baru
            if unit_use is None:
                if "Powder" in bahan or "Bubuk" in bahan:
                    unit_use = "gram"
                elif "Syrup" in bahan or "Susu" in bahan or "Air" in bahan:
                    unit_use = "ml"
                else:
                    unit_use = "pcs"

            self.stock[bahan] = {"qty": 0, "unit": unit_use}
        else:
            # Validasi kesesuaian satuan terhadap bahan yang sudah ada
            existing_unit = self.stock[bahan]["unit"]
            if unit_use is not None and unit_use != existing_unit:
                raise ValueError(
                    f"Satuan tidak sesuai untuk bahan '{bahan}'. Gunakan satuan '{existing_unit}'."
                )

        self.stock[bahan]["qty"] += jumlah
        self.log_tambah.append(f"+{jumlah} {self.stock[bahan]['unit']} {bahan}")
        
        # FASE 2: Audit log
        audit = AuditLog(username, "TAMBAH", bahan, jumlah)
        self.audit_logs.append(audit)
        
        self._notify(f"Stok {bahan} telah diperbarui")

    # =========================
    # PAKAI STOK
    # =========================
    def use_stock(self, bahan, jumlah, username="system"):
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
        
        # FASE 2: Audit log
        audit = AuditLog(username, "PAKAI", bahan, jumlah)
        self.audit_logs.append(audit)

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
    # AUDIT LOG (FASE 2)
    # =========================
    def show_audit_logs(self, limit=20):
        """Tampilkan audit log stok (default 20 terakhir)"""
        print("\n" + "="*70)
        print("AUDIT LOG STOK - NGOPIKUY".center(70))
        print("="*70)
        
        if not self.audit_logs:
            print("Belum ada aktivitas stok yang tercatat")
            print("="*70)
            return
        
        logs_to_show = self.audit_logs[-limit:] if len(self.audit_logs) > limit else self.audit_logs
        
        for log in logs_to_show:
            print(log)
        
        print("="*70)
        print(f"Total log: {len(self.audit_logs)} | Ditampilkan: {len(logs_to_show)}")


# =========================
# ANTRIAN PESANAN (FASE 2)
# =========================
class AntrianPesanan:
    """Singleton untuk mengelola antrian pesanan"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AntrianPesanan, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized"):
            return
        self._initialized = True
        self.antrian = []  # List of Penjualan objects

    def tambah_pesanan(self, penjualan):
        """Tambah pesanan baru ke antrian"""
        self.antrian.append(penjualan)
        print(f"✓ Pesanan {penjualan.id_transaksi} ditambahkan ke antrian")

    def show_antrian(self):
        """Tampilkan antrian pesanan yang belum selesai"""
        print("\n" + "="*80)
        print("ANTRIAN PESANAN - NGOPIKUY".center(80))
        print("="*80)
        
        # Filter hanya pesanan yang belum selesai/batal
        active = [p for p in self.antrian if p.status not in [StatusPesanan.SELESAI, StatusPesanan.BATAL]]
        
        if not active:
            print("Tidak ada pesanan dalam antrian")
            print("="*80)
            return
        
        print(f"| {'No':<3} | {'ID Transaksi':<20} | {'Status':<10} | {'Kasir':<12} | {'Waktu Dibuat':<18} |")
        print("-"*80)
        
        for i, pesanan in enumerate(active, start=1):
            waktu = pesanan.waktu_dibuat.strftime("%Y-%m-%d %H:%M:%S")
            print(f"| {i:<3} | {pesanan.id_transaksi:<20} | {pesanan.status:<10} | {pesanan.username:<12} | {waktu:<18} |")
        
        print("="*80)
        print(f"Total antrian aktif: {len(active)}")

    def update_status_pesanan(self, id_transaksi, status_baru, username):
        """Update status pesanan berdasarkan ID"""
        for pesanan in self.antrian:
            if pesanan.id_transaksi == id_transaksi:
                pesanan.update_status(status_baru, username)
                return True
        print(f"❌ Pesanan {id_transaksi} tidak ditemukan")
        return False


# =========================
# DECORATOR
# =========================
def highlight_menu(func):
    def wrapper(*args, **kwargs):
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
    
    @staticmethod
    def laporan_metode_pembayaran(transaksi_manager):
        """Laporan rekap metode pembayaran (FASE 2)"""
        print("\n" + "="*60)
        print("LAPORAN METODE PEMBAYARAN - NGOPIKUY".center(60))
        print("="*60)
        
        if not transaksi_manager.riwayat_penjualan:
            print("Belum ada transaksi penjualan")
            print("=" * 60)
            return
        
        # Rekap per metode
        rekap = {}
        for trx in transaksi_manager.riwayat_penjualan:
            metode = trx.metode_bayar.upper()
            total = trx.hitung_total()
            
            if metode not in rekap:
                rekap[metode] = {"jumlah": 0, "total": 0}
            
            rekap[metode]["jumlah"] += 1
            rekap[metode]["total"] += total
        
        # Tampilkan rekap
        print(f"| {'Metode':<15} | {'Jumlah Trx':>12} | {'Total (Rp)':>15} |")
        print("-"*60)
        
        grand_total = 0
        for metode, data in sorted(rekap.items()):
            print(f"| {metode:<15} | {data['jumlah']:>12} | Rp {data['total']:>12,} |")
            grand_total += data["total"]
        
        print("-"*60)
        print(f"| {'TOTAL':<15} | {sum(d['jumlah'] for d in rekap.values()):>12} | Rp {grand_total:>12,} |")
        print("=" * 60)


# ===============================
# INISIALISASI (Singleton Inventory)
# ===============================
inventory = ManajemenPersediaan()
product_manager = ProductManager()
transaksi_manager = TransaksiManager()
laporan_manager = LaporanManager()
antrian_pesanan = AntrianPesanan()  # FASE 2
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

# Tambahan resep menggunakan bahan yang tersedia
cappuccino_recipe = {
    "Bubuk Kopi": {"qty": 18, "unit": "gram", "note": "Espresso"},
    "Susu Full Cream": {"qty": 120, "unit": "ml", "note": "Steamed"},
    "Air": {"qty": 30, "unit": "ml", "note": "Hot"},
    "Cup": {"qty": 1, "unit": "pcs", "note": "Packaging"}
}

caramel_macchiato_recipe = {
    "Bubuk Kopi": {"qty": 18, "unit": "gram", "note": "Espresso"},
    "Susu Full Cream": {"qty": 150, "unit": "ml", "note": "Steamed"},
    "Caramel Syrup": {"qty": 20, "unit": "ml", "note": "Syrup"},
    "Cup": {"qty": 1, "unit": "pcs", "note": "Packaging"}
}

mocha_recipe = {
    "Bubuk Kopi": {"qty": 18, "unit": "gram", "note": "Espresso"},
    "Coklat Bubuk": {"qty": 20, "unit": "gram", "note": "Mix"},
    "Susu Full Cream": {"qty": 140, "unit": "ml", "note": "Steamed"},
    "Cup": {"qty": 1, "unit": "pcs", "note": "Packaging"}
}

matcha_latte_recipe = {
    "Matcha Powder": {"qty": 25, "unit": "gram", "note": "Flavor"},
    "Susu Full Cream": {"qty": 150, "unit": "ml", "note": "Milk Base"},
    "Cup": {"qty": 1, "unit": "pcs", "note": "Packaging"}
}

kopi_gula_aren_recipe = {
    "Bubuk Kopi": {"qty": 18, "unit": "gram", "note": "Espresso"},
    "Susu Full Cream": {"qty": 140, "unit": "ml", "note": "Milk Base"},
    "Gula Aren": {"qty": 20, "unit": "gram", "note": "Sweetener"},
    "Cup": {"qty": 1, "unit": "pcs", "note": "Packaging"}
}

hot_chocolate_recipe = {
    "Coklat Bubuk": {"qty": 30, "unit": "gram", "note": "Mix"},
    "Susu Full Cream": {"qty": 180, "unit": "ml", "note": "Hot"},
    "Cup": {"qty": 1, "unit": "pcs", "note": "Packaging"}
}

oat_latte_recipe = {
    "Bubuk Kopi": {"qty": 18, "unit": "gram", "note": "Espresso"},
    "Susu Oat": {"qty": 150, "unit": "ml", "note": "Milk Base"},
    "Air": {"qty": 30, "unit": "ml", "note": "Hot"},
    "Cup": {"qty": 1, "unit": "pcs", "note": "Packaging"}
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

# Tambahkan produk baru
product_manager.add_product(ProductFactory.create_product(
    "Cappuccino", "coffee", 22000, cappuccino_recipe
))
product_manager.add_product(ProductFactory.create_product(
    "Caramel Macchiato", "coffee", 25000, caramel_macchiato_recipe
))
product_manager.add_product(ProductFactory.create_product(
    "Mocha", "coffee", 24000, mocha_recipe
))
product_manager.add_product(ProductFactory.create_product(
    "Matcha Latte", "non-coffee", 24000, matcha_latte_recipe
))
product_manager.add_product(ProductFactory.create_product(
    "Kopi Susu Gula Aren", "coffee", 23000, kopi_gula_aren_recipe
))
product_manager.add_product(ProductFactory.create_product(
    "Hot Chocolate", "non-coffee", 22000, hot_chocolate_recipe
))
product_manager.add_product(ProductFactory.create_product(
    "Oat Latte", "coffee", 23000, oat_latte_recipe
))

# ===============================
# MENU UTAMA (SINGLE ADMIN)
# ===============================
def tampilkan_menu():
    print("\n" + "="*70)
    print("SISTEM MANAJEMEN NGOPIKUY".center(70))
    print("="*70)
    print("1. Lihat Daftar Produk")
    print("2. Lihat Stok Bahan")
    print("3. Cari Bahan")
    print("4. Tambah / Restock Bahan")
    print("5. Tambah Produk Baru")
    print("6. Jual Menu (Penjualan)")
    print("7. Beli Bahan dari Supplier (Pembelian)")
    print("8. Lihat Antrian Pesanan")
    print("9. Update Status Pesanan")
    print("10. Laporan & Analisis")
    print("11. Audit Log Stok")
    print("12. Hapus Produk")
    print("13. Keluar")
    print("="*70)


# ===============================
# SUPPLIER CATALOG & TABLE VIEW
# ===============================
# Daftar supplier beserta bahan yang disediakan
SUPPLIERS = {
    "SUP-COF": {"nama": "Sumatra Coffee Co.", "menyediakan": ["Bubuk Kopi", "Cup"]},
    "SUP-DAI": {"nama": "Fresh Dairy", "menyediakan": ["Susu Full Cream", "Susu Oat"]},
    "SUP-SYR": {"nama": "Syrup House", "menyediakan": ["Caramel Syrup", "Gula Aren"]},
    "SUP-POW": {"nama": "Powder Mate", "menyediakan": ["Matcha Powder", "Taro Powder", "Coklat Bubuk"]},
    "SUP-BAK": {"nama": "Bakery Supply", "menyediakan": ["Tepung Terigu", "Mentega"]},
    "SUP-PKG": {"nama": "Pack&Go", "menyediakan": ["Cup", "Sedotan Hitam"]},
    "SUP-WAT": {"nama": "Aqua Pure", "menyediakan": ["Air"]},
}

def show_suppliers_table():
    print("\n" + "="*80)
    print("DAFTAR SUPPLIER - NGOPIKUY".center(80))
    print("="*80)
    print(f"| {'Kode':<10} | {'Nama Supplier':<22} | {'Menyediakan':<40} |")
    print("-"*80)
    for kode in sorted(SUPPLIERS.keys()):
        data = SUPPLIERS[kode]
        menyediakan = ", ".join(data["menyediakan"])[:40]
        print(f"| {kode:<10} | {data['nama']:<22} | {menyediakan:<40} |")
    print("="*80)


# ===============================
# HELPER: GENERATE ID TRANSAKSI
# ===============================
def generate_id_penjualan(counter):
    """Generate ID penjualan format: NGO-SAL-YYYYMM-####"""
    bulan = datetime.now().strftime("%Y%m")
    nomor = str(counter + 1).zfill(4)
    return f"NGO-SAL-{bulan}-{nomor}"


def generate_id_pembelian(counter):
    """Generate ID pembelian format: NGO-BUY-YYYYMM-####"""
    bulan = datetime.now().strftime("%Y%m")
    nomor = str(counter + 1).zfill(4)
    return f"NGO-BUY-{bulan}-{nomor}"


# ===============================
    print("1. Tambah Stok Bahan")
    print("2. Lihat Stok Bahan")
    print("3. Tambah Produk")
    print("4. Lihat Daftar Produk")
    print("5. Cari Bahan")
    print("6. Transaksi Penjualan Produk")
    print("7. Transaksi Pembelian Bahan (Supplier)")
    print("8. Hapus Produk")
    print("9. Laporan & Analisis")
    print("10. Keluar")
    print("="*70)


# ================================
# FUNGSI UTAMA
# ================================
def main():
    """Fungsi utama untuk menjalankan sistem"""
    global riwayat_transaksi

    username = login()
    if username is None:
        return

    print(f"\n Selamat datang di Sistem Operasi Ngopikuy!")

    # Header awal (langsung lanjut ke menu tanpa daftar produk/stok)
    print("\n" + "="*70)
    print("SISTEM MANAJEMEN COFFEE SHOP".center(70))
    print("NGOPIKUY".center(70))
    print("="*70)
    # Tampilkan tabel daftar produk (tanpa judul custom tambahan)
    product_manager.show_products()
    
    while True:
        tampilkan_menu()
        pilihan = input("\nPilih menu: ").strip()

        # ===============================
        # 1. LIHAT DAFTAR PRODUK
        # ===============================
        if pilihan == "1":
            product_manager.show_products()
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
        # 2. LIHAT STOK BAHAN
        # ===============================
        elif pilihan == "2":
            inventory.show_stock_table()

        # ===============================
        # 3. CARI BAHAN
        # ===============================
        elif pilihan == "3":
            print("\n" + "="*60)
            print("CARI BAHAN - NGOPIKUY".center(60))
            print("="*60)
            nama = input("Nama bahan: ").strip().lower()
            if not nama:
                print("❌ Nama bahan tidak boleh kosong!")
                continue
            
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
        # 4. RESTOCK BAHAN
        # ===============================
        elif pilihan == "4":
            print("\n" + "="*60)
            print("RESTOCK BAHAN - NGOPIKUY".center(60))
            print("="*60)
            try:
                bahan = input("Nama bahan: ").strip()
                if not bahan:
                    print("❌ Nama bahan tidak boleh kosong!")
                    continue
                
                jumlah_str = input("Jumlah: ").strip()
                try:
                    jumlah = int(jumlah_str)
                except ValueError:
                    print("❌ Input jumlah tidak valid. Masukkan angka bulat, contoh: 10.")
                    continue
                if jumlah <= 0:
                    print("❌ Jumlah harus lebih dari 0!")
                    continue
                
                # Input satuan: pilih dari opsi yang tersedia (tanpa input manual)
                print("\nPilih Satuan:")
                print("1. gram")
                print("2. kg")
                print("3. ml")
                print("4. pcs")
                satuan_input = input("Satuan (1-4): ").strip().lower()
                mapping = {"1": "gram", "2": "kg", "3": "ml", "4": "pcs"}
                if satuan_input not in mapping:
                    print("❌ Pilihan satuan tidak valid. Pilih 1-gram, 2-kg, 3-ml, atau 4-pcs.")
                    continue
                satuan = mapping[satuan_input]
                
                # Hitung kuantitas aktual jika satuan kg (konversi ke gram untuk penyimpanan)
                actual_qty = jumlah * 1000 if satuan.lower() == "kg" else jumlah
                actual_unit = "gram" if satuan.lower() == "kg" else satuan
                
                inventory.add_stock(bahan, jumlah, username, unit=satuan)
                print(f"✓ Berhasil menambah {actual_qty} {actual_unit} {bahan}")
                inventory.show_stock_table()
            except ValueError as e:
                print(f"❌ {e}")

        # ===============================
        # 5. TAMBAH PRODUK
        # ===============================
        elif pilihan == "5":
            print("\n" + "="*60)
            print("TAMBAH PRODUK BARU - NGOPIKUY".center(60))
            print("="*60)
            nama = input("Nama produk: ").strip()
            if not nama:
                print("❌ Nama produk tidak boleh kosong!")
                continue

            print("\nPilih Kategori:")
            print("1. Coffee")
            print("2. Non-Coffee")
            print("3. Pastry")

            pil = input("Pilihan (1-3): ").strip().lower()
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
                if harga <= 0:
                    print("❌ Harga harus lebih dari 0!")
                    continue
            except ValueError:
                print("❌ Harga harus berupa angka!")
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

            if not recipe:
                print("❌ Minimal harus ada 1 resep!")
                continue
            
            product_manager.add_product(
                ProductFactory.create_product(nama, kategori, harga, recipe)
            )
            print(f"✓ Produk '{nama}' berhasil ditambahkan")

        # ===============================
        # 8. LIHAT ANTRIAN PESANAN
        # ===============================
        elif pilihan == "8":
            antrian_pesanan.show_antrian()
            input("\nTekan Enter untuk kembali...")

        # ===============================
        # 9. UPDATE STATUS PESANAN
        # ===============================
        elif pilihan == "9":
            print("\n" + "="*60)
            print("UPDATE STATUS PESANAN - NGOPIKUY".center(60))
            print("="*60)
            
            # Tampilkan antrian dulu
            antrian_pesanan.show_antrian()
            
            id_transaksi = input("\nMasukkan ID Transaksi: ").strip()
            
            print("\nPilih Status Baru:")
            print(f"1. {StatusPesanan.DISEDUH}")
            print(f"2. {StatusPesanan.SIAP}")
            print(f"3. {StatusPesanan.SELESAI}")
            print(f"4. {StatusPesanan.BATAL}")
            
            status_pilihan = input("Pilih (1-4): ").strip().lower()
            
            status_map = {
                "1": StatusPesanan.DISEDUH,
                "2": StatusPesanan.SIAP,
                "3": StatusPesanan.SELESAI,
                "4": StatusPesanan.BATAL
            }
            
            if status_pilihan in status_map:
                status_baru = status_map[status_pilihan]
                antrian_pesanan.update_status_pesanan(id_transaksi, status_baru, username)
            else:
                print("❌ Pilihan tidak valid")
            
            input("\nTekan Enter untuk kembali...")

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
            nama = input("Nama bahan: ").strip().lower()
            if not nama:
                print("❌ Nama bahan tidak boleh kosong!")
                continue
            
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
        # 6. JUAL MENU (PENJUALAN)
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

                # Buat transaksi penjualan dengan ID format baru dan username
                metode_bayar = input("\nMetode Pembayaran (Tunai/Debit/QRIS): ").strip().lower()
                metode_valid = ["tunai", "debit", "qris"]
                if metode_bayar not in metode_valid:
                    print("❌ Metode pembayaran hanya: Tunai, Debit, atau QRIS")
                    continue
                
                id_penjualan = generate_id_penjualan(len(riwayat_transaksi))
                transaksi = Penjualan(id_penjualan, metode_bayar, username)
                
                # Cek & kurangi stok untuk setiap pesanan
                try:
                    for _ in range(jumlah_order):
                        for bahan, data in product.recipe.items():
                            inventory.use_stock(bahan, data["qty"], username)  # Pass username untuk audit
                        transaksi.tambah_produk(product, 1)
                    
                    # Cetak struk dengan user info
                    transaksi.cetak_struk()
                    
                    # Simpan ke riwayat
                    riwayat_transaksi.append(transaksi)
                    transaksi_manager.tambah_penjualan(transaksi)
                    
                    # FASE 2: Tambahkan ke antrian pesanan
                    antrian_pesanan.tambah_pesanan(transaksi)
                    
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
            # Tampilkan daftar supplier untuk mempermudah pemilihan
            show_suppliers_table()
            # Input supplier: gunakan kode (disarankan) atau ketik nama manual
            kode_supplier = input("Masukkan Kode Supplier (mis. SUP-COF) atau Nama: ").strip()
            if not kode_supplier:
                print("❌ Kode supplier harus diisi!")
                continue
            # Jika kode valid, tampilkan label lengkap "KODE - Nama"
            supplier_label = kode_supplier
            if kode_supplier in SUPPLIERS:
                supplier_label = f"{kode_supplier} - {SUPPLIERS[kode_supplier]['nama']}"
            
            # Buat transaksi pembelian dengan ID format baru dan username
            id_pembelian = generate_id_pembelian(len(transaksi_manager.riwayat_pembelian))
            transaksi_beli = Pembelian(id_pembelian, supplier_label, username)
            
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
                    
                    # Tambahkan ke inventory dengan username tracking
                    try:
                        inventory.add_stock(nama_bahan, jumlah, username)
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
                print(f"User         : {transaksi_beli.username}")
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
        # 10. LAPORAN & ANALISIS
        # ===============================
        elif pilihan == "10":
            # Loop submenu laporan & analisis
            while True:
                print("\n" + "="*60)
                print("LAPORAN & ANALISIS - NGOPIKUY".center(60))
                print("="*60)
                print("1. Laporan Penjualan Harian")
                print("2. Laporan Pembelian")
                print("3. Laporan Stok Menipis")
                print("4. Laporan Metode Pembayaran")
                print("5. Riwayat Transaksi Penjualan")
                print("6. Riwayat Transaksi Pembelian")
                print("7. Kembali ke Menu Utama")
                
                sub_pilihan = input("\nPilih (1-7): ").strip().lower()
                
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
                    # FASE 2: Laporan metode pembayaran
                    laporan_manager.laporan_metode_pembayaran(transaksi_manager)
                elif sub_pilihan == "5":
                    transaksi_manager.tampilkan_riwayat_penjualan()
                elif sub_pilihan == "6":
                    transaksi_manager.tampilkan_riwayat_pembelian()
                elif sub_pilihan == "7":
                    break  # Keluar dari loop submenu, kembali ke menu utama
                else:
                    print("❌ Pilihan tidak valid")
                
                input("\nTekan Enter untuk kembali...")

        # ===============================
        # 11. AUDIT LOG STOK (FASE 2)
        # ===============================
        elif pilihan == "11":
            inventory.show_audit_logs(limit=30)
            input("\nTekan Enter untuk kembali...")

        # ===============================
        # 12. HAPUS PRODUK
        # ===============================
        elif pilihan == "12":
            print("\n" + "="*60)
            print("HAPUS PRODUK - NGOPIKUY".center(60))
            print("="*60)
            product_manager.show_products()
            nama = input("\nNama produk yang ingin dihapus: ").strip().lower()
            if not nama:
                print("❌ Nama produk tidak boleh kosong!")
                continue
            
            try:
                product_manager.hapus_produk(nama)
                print(f"✓ Produk '{nama}' berhasil dihapus")
            except ValueError as e:
                print(f"❌ {e}")

        # ===============================
        # 13. KELUAR
        # ===============================
        elif pilihan == "13":
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
