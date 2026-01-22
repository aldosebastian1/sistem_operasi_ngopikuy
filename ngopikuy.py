# =========================
# SISTEM MANAJEMEN COFFEE SHOP - NGOPIKUY
# Pemrograman Berbasis Object - UTS
# =========================
from datetime import datetime
import msvcrt


# =========================
# KONSTANTA SISTEM
# =========================
PPN_RATE = 0.11  # PPN 11% sesuai aturan Indonesia


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

    def tambah_item(self, item):
        # Menambahkan item ke dalam transaksi
        self.daftar_item.append(item)


class Penjualan(Transaksi):
    # Class penjualan Subclass dari Transaksi merepresentasikan satu transaksi penjualan ke customer
    def __init__(self, id_transaksi, metode_bayar, username="system"):
        # Memanggil constructor Transaksi (inheritance)
        super().__init__(id_transaksi, username)
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
        elif status_baru == StatusPesanan.DIAMBIL or status_baru == StatusPesanan.BATAL:
            self.waktu_selesai = datetime.now()
        print(f"✓ Status pesanan {self.id_transaksi} diubah menjadi {status_baru} oleh {username}")

    def tambah_produk(self, produk, jumlah):
        # Menambahkan produk yang dijual ke dalam transaksi
        self.tambah_item({
            "nama_produk": produk.name,
            "harga": produk.price,
            "jumlah": jumlah
        })
    
    def hitung_subtotal(self):
        """Menghitung subtotal sebelum PPN"""
        subtotal = 0
        for item in self.daftar_item:
            subtotal += item["harga"] * item["jumlah"]
        return subtotal
    
    def hitung_ppn(self):
        """Menghitung nilai PPN 11%"""
        return int(self.hitung_subtotal() * PPN_RATE)
    
    def hitung_total_dengan_ppn(self):
        """Menghitung total akhir termasuk PPN"""
        return self.hitung_subtotal() + self.hitung_ppn()

    def cetak_struk(self):
        # Menampilkan struk penjualan ke layar dengan info lengkap
        metode_display = self.metode_bayar.capitalize()
        
        print("\n" + "="*54)
        print("NGOPIKUY COFFEE SHOP".center(54))
        print("="*54)
        print(f"ID Transaksi : {self.id_transaksi}")
        print(f"Tanggal      : {self.tanggal_transaksi}")
        print(f"Kasir        : {self.username}")
        print(f"Pembayaran   : {metode_display}")
        print("-" * 54)

        for item in self.daftar_item:
            subtotal = item['harga'] * item['jumlah']
            print(f"{item['nama_produk']:<25} x{item['jumlah']:<2}  Rp {subtotal:>12,}")

        print("-" * 54)
        
        # Breakdown: Subtotal, PPN, Total
        subtotal = self.hitung_subtotal()
        ppn = self.hitung_ppn()
        total = self.hitung_total_dengan_ppn()
        
        print(f"{'Subtotal':<32}  Rp {subtotal:>12,}")
        print(f"{'PPN 11%':<32}  Rp {ppn:>12,}")
        print("-" * 54)
        print(f"{'TOTAL BAYAR':<32}  Rp {total:>12,}")
        print("="*54)
        print("Terima Kasih atas Kunjungan Anda!".center(54))
        print("="*54 + "\n")


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
        })

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
    DIAMBIL = "DIAMBIL"
    BATAL = "BATAL"


# =========================
# AUDIT LOG STOK (FASE 2)
# =========================
class AuditLog:
    def __init__(self, username, aksi, bahan, jumlah, unit, waktu=None):
        self.username = username
        self.aksi = aksi  # "TAMBAH" atau "PAKAI"
        self.bahan = bahan
        self.jumlah = jumlah
        self.unit = unit
        self.waktu = waktu or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        # Tampilkan konversi ramah untuk gram >= 1000
        if self.unit == "gram" and self.jumlah >= 1000:
            kg = self.jumlah / 1000
            return f"[{self.waktu}] {self.username} - {self.aksi} {self.jumlah} gram ({kg:.2f} kg) {self.bahan}"
        return f"[{self.waktu}] {self.username} - {self.aksi} {self.jumlah} {self.unit} {self.bahan}"


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
        audit = AuditLog(username, "TAMBAH", bahan, jumlah, self.stock[bahan]["unit"])
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
        audit = AuditLog(username, "PAKAI", bahan, jumlah, self.stock[bahan]["unit"])
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
        print("\n" + "="*80)
        print("STOK BAHAN - NGOPIKUY".center(80))
        print("="*80)
        print(f"| {'No':<4} | {'Nama Bahan':<30} | {'Jumlah':>10} | {'Satuan':^10} | {'Status':^10} |")
        print("-"*80)

        for i, (bahan, data) in enumerate(self.stock.items(), start=1):
            jumlah = data["qty"]
            satuan = data["unit"]
            status = self.get_status(jumlah)

            print(
                f"| {i:<4} | {bahan:<30} | "
                f"{jumlah:>10} | {satuan:^10} | {status:^10} |"
            )

        print("="*80)

    def show_stock_table_compact(self, title="DAFTAR BAHAN TERSEDIA"):
        """Tampilkan tabel stok dalam format ringkas untuk tambah resep"""
        print("\n" + "="*75)
        print(title.center(75))
        print("="*75)
        print(f"| {'No':<3} | {'Nama Bahan':<32} | {'Satuan':^8} | {'Status':^8} |")
        print("-"*75)

        for i, (bahan, data) in enumerate(self.stock.items(), start=1):
            satuan = data["unit"]
            jumlah = data["qty"]
            status = self.get_status(jumlah)
            print(f"| {i:<3} | {bahan:<32} | {satuan:^8} | {status:^8} |")

        print("="*75)

    def show_recipe_helper_table(self):
        """Tabel panduan bahan, satuan, dan keterangan untuk tambah resep."""
        unit_note = {
            "gram": "Bubuk/padat (kopi, powder, gula)",
            "ml": "Cair/sirup/susu (shot, milk, water)",
            "pcs": "Kemasan/aksesori (cup, sedotan)",
        }

        # Keterangan lebih kontekstual per bahan (fallback ke unit_note jika tidak ada)
        item_note = {
            "Bubuk Kopi": "Espresso",
            "Air": "Hot",
            "Susu Full Cream": "Steamed",
            "Susu Oat": "Milk Base",
            "Gula Aren": "Sweetener",
            "Caramel Syrup": "Syrup",
            "Coklat Bubuk": "Mix",
            "Matcha Powder": "Flavor",
            "Taro Powder": "Flavor",
            "Tepung Terigu": "Dough",
            "Mentega": "Butter",
            "Cup": "Packaging",
            "Sedotan Hitam": "Packaging",
        }

        width = 78
        print("\n" + "="*width)
        print("PANDUAN BAHAN RESEP".center(width))
        print("="*width)
        print(f"| {'No':<3} | {'Nama Bahan':<28} | {'Satuan':^8} | {'Keterangan':<30} |")
        print("-"*width)

        for i, (bahan, data) in enumerate(self.stock.items(), start=1):
            satuan = data["unit"]
            note = item_note.get(bahan, unit_note.get(satuan, "-"))
            print(f"| {i:<3} | {bahan:<28} | {satuan:^8} | {note:<30} |")

        print("="*width)

    # =========================
    # AUDIT LOG (FASE 2)
    # =========================
    def show_audit_logs(self, limit=20):
        """Tampilkan audit log stok (default 20 terbaru) dalam format ringkas."""
        width = 100
        print("\n" + "="*width)
        print("AUDIT LOG STOK - NGOPIKUY".center(width))
        print("="*width)

        if not self.audit_logs:
            print("Belum ada aktivitas stok yang tercatat")
            print("="*width)
            return

        logs_to_show = self.audit_logs[-limit:] if len(self.audit_logs) > limit else self.audit_logs
        # Tampilkan terbaru dulu
        logs_to_show = list(reversed(logs_to_show))

        print(f"| {'No':<3} | {'Waktu':<19} | {'User':<12} | {'Aksi':<6} | {'Bahan':<28} | {'Jumlah':<15} |")
        print("-"*width)
        for i, log in enumerate(logs_to_show, start=1):
            # Format jumlah ringkas dengan unit dan konversi otomatis untuk gram
            if log.unit == "gram":
                # Gunakan satu satuan saja: tampilkan sebagai kg selalu
                jumlah_display = f"{log.jumlah/1000:.2f} kg"
            elif log.unit == "ml":
                jumlah_display = f"{log.jumlah} ml"
            elif log.unit == "pcs":
                jumlah_display = f"{log.jumlah} pcs"
            else:
                jumlah_display = f"{log.jumlah} {log.unit}"

            print(
                f"| {i:<3} | {log.waktu:<19} | {log.username:<12} | {log.aksi:<6} | "
                f"{log.bahan:<28} | {jumlah_display:<15} |"
            )

        print("="*width)


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

    def get_active(self):
        """Kembalikan daftar pesanan aktif (belum diambil/batal)."""
        return [p for p in self.antrian if p.status not in [StatusPesanan.DIAMBIL, StatusPesanan.BATAL]]

    def show_antrian(self):
        """Tampilkan antrian pesanan yang belum selesai"""
        # Filter hanya pesanan yang belum diambil/batal
        active = [p for p in self.antrian if p.status not in [StatusPesanan.DIAMBIL, StatusPesanan.BATAL]]
        
        header = f"| {'No':<3} | {'ID Transaksi':<20} | {'Status':<10} | {'Kasir':<14} | {'Waktu Dibuat':<19} |"
        table_width = len(header)
        sep = "-" * table_width
        
        print("\n" + "=" * table_width)
        print("ANTRIAN PESANAN - NGOPIKUY".center(table_width))
        print("=" * table_width)
        
        if not active:
            print("Tidak ada pesanan dalam antrian")
            print("=" * table_width)
            return
        
        print(header)
        print(sep)
        
        for i, pesanan in enumerate(active, start=1):
            waktu = pesanan.waktu_dibuat.strftime("%Y-%m-%d %H:%M:%S")
            row = f"| {i:<3} | {pesanan.id_transaksi:<20} | {pesanan.status:<10} | {pesanan.username:<14} | {waktu:<19} |"
            print(row)
        
        print("=" * table_width)
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
        """Tampilkan detail resep menu individual"""
        header = f"| {'No':<3} | {'Nama Bahan':<28} | {'Jumlah':>8} | {'Satuan':^8} | {'Keterangan':<15} |"
        table_width = len(header)
        sep = "-" * table_width

        print("\n" + "=" * table_width)
        print("DETAIL RESEP MENU - NGOPIKUY".center(table_width))
        print("=" * table_width)
        print(f"Menu     : {self.name}")
        print(f"Kategori : {self.kategori}")
        print(f"Harga    : Rp {self.price:,}")
        print(sep)
        print(header)
        print(sep)

        for i, (bahan, data) in enumerate(self.recipe.items(), start=1):
            row = (
                f"| {i:<3} | {bahan:<28} | "
                f"{data['qty']:>8} | {data['unit']:^8} | "
                f"{data.get('note', '-'):<15} |"
            )
            print(row)

        print("=" * table_width)
    
    def format_recipe_for_order(self, index):
        """Format resep untuk ditampilkan dalam order detail gabungan (tanpa judul umum)"""
        lines = []
        indent = "    "
        
        # Header dengan nama produk
        lines.append(f"[{index}] {self.name}")
        lines.append(f"{indent}Kategori : {self.kategori} | Harga : Rp {self.price:,}")
        
        # Buat header tabel
        header = f"| {'No':<3} | {'Nama Bahan':<28} | {'Jumlah':>8} | {'Satuan':^8} | {'Keterangan':<15} |"
        table_width = len(header)
        sep = "-" * table_width
        
        lines.append(indent + sep)
        lines.append(indent + header)
        lines.append(indent + sep)
        
        # Baris data resep
        for i, (bahan, data) in enumerate(self.recipe.items(), start=1):
            row = (
                f"| {i:<3} | {bahan:<28} | "
                f"{data['qty']:>8} | {data['unit']:^8} | "
                f"{data.get('note', '-'):<15} |"
            )
            lines.append(indent + row)
        
        # Footer
        lines.append(indent + sep)
        return "\n".join(lines)


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

    def hapus_produk_by_index(self, index):
        """Hapus produk berdasarkan nomor (index 0-based)."""
        if 0 <= index < len(self.products):
            removed = self.products.pop(index)
            return removed
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

    def show_products_table_only(self):
        """Tampilkan tabel produk tanpa judul (untuk konteks dengan judul custom)"""
        header = f"| {'No':<3} | {'Nama Produk':<26} | {'Harga':>14} | {'Kategori':<16} |"
        table_width = len(header)
        sep = "-" * table_width
        
        print(header)
        print(sep)

        if not self.products:
            print(f"| {'--':<3} | {'BELUM ADA PRODUK':<26} | {' ':>14} | {' ':<16} |")
        else:
            for i, product in enumerate(self.products, start=1):
                row = (
                    f"| {i:<3} | {product.name:<26} | "
                    f"Rp {product.price:>11,} | {product.get_label():<16} |"
                )
                print(row)

        print("=" * table_width)

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
        print("\n" + "="*86)
        print("RIWAYAT PENJUALAN - NGOPIKUY".center(86))
        print("="*86)
        if not self.riwayat_penjualan:
            print("Belum ada transaksi penjualan")
        else:
            for i, trx in enumerate(self.riwayat_penjualan, 1):
                print(f"\n--- Penjualan #{i} ---")
                trx.cetak_struk()
    
    def tampilkan_riwayat_pembelian(self):
        """Menampilkan semua riwayat pembelian"""
        print("\n" + "="*86)
        print("RIWAYAT PEMBELIAN - NGOPIKUY".center(86))
        print("="*86)
        if not self.riwayat_pembelian:
            print("Belum ada transaksi pembelian")
        else:
            print(f"| {'No':<3} | {'ID Transaksi':<20} | {'Tanggal':<19} | {'Supplier':<22} | {'Total':>12} |")
            print("-"*86)
            for i, trx in enumerate(self.riwayat_pembelian, 1):
                total = trx.konfirmasi_pembelian()
                print(
                    f"| {i:<3} | {trx.id_transaksi:<20} | {trx.tanggal_transaksi:<19} | {trx.kode_supplier:<22} | Rp {total:>9,} |"
                )
            print("="*86)


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
        
        total_subtotal = 0
        total_ppn = 0
        
        for trx in transaksi_manager.riwayat_penjualan:
            total_subtotal += trx.hitung_subtotal()
            total_ppn += trx.hitung_ppn()
        
        total_pendapatan = total_subtotal + total_ppn
        
        print(f"Total Transaksi      : {total_transaksi}")
        print(f"Subtotal             : Rp {total_subtotal:,}")
        print(f"PPN 11%              : Rp {total_ppn:,}")
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
            total = trx.hitung_total_dengan_ppn()
            
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
    print("3. Tambah Produk Baru")
    print("4. Tambah / Restock Bahan")
    print("5. Jual Menu (Penjualan)")
    print("6. Beli Bahan dari Supplier (Pembelian)")
    print("7. Lihat Antrian Pesanan")
    print("8. Update Status Pesanan")
    print("9. Laporan & Analisis")
    print("10. Audit Log Stok")
    print("11. Hapus Produk")
    print("12. Keluar")
    print("="*70)


# ===============================
# SUPPLIER CATALOG & TABLE VIEW
# ===============================
# Daftar supplier beserta bahan yang disediakan
SUPPLIERS = {
    # Harga per satuan mengikuti satuan di inventory (gram/ml/pcs)
    "SUP-COF": {
        "nama": "Sumatra Coffee Co.",
        "produk": {
            "Bubuk Kopi": 200,      # Rp per gram
            "Cup": 500               # Rp per pcs
        }
    },
    "SUP-DAI": {
        "nama": "Fresh Dairy",
        "produk": {
            "Susu Full Cream": 2,   # Rp per ml
            "Susu Oat": 3           # Rp per ml
        }
    },
    "SUP-SYR": {
        "nama": "Syrup House",
        "produk": {
            "Caramel Syrup": 2,     # Rp per ml
            "Gula Aren": 50         # Rp per gram
        }
    },
    "SUP-POW": {
        "nama": "Powder Mate",
        "produk": {
            "Matcha Powder": 150,   # Rp per gram
            "Taro Powder": 80,      # Rp per gram
            "Coklat Bubuk": 60      # Rp per gram
        }
    },
    "SUP-BAK": {
        "nama": "Bakery Supply",
        "produk": {
            "Tepung Terigu": 15,    # Rp per gram
            "Mentega": 30           # Rp per gram
        }
    },
    "SUP-PKG": {
        "nama": "Pack&Go",
        "produk": {
            "Cup": 450,             # Rp per pcs (alternatif supplier)
            "Sedotan Hitam": 150    # Rp per pcs
        }
    },
    "SUP-WAT": {
        "nama": "Aqua Pure",
        "produk": {
            "Air": 1                # Rp per ml
        }
    },
}

def show_suppliers_table():
    print("\n" + "="*86)
    print("DAFTAR SUPPLIER - NGOPIKUY".center(86))
    print("="*86)
    print(f"| {'No':<3} | {'Kode':<10} | {'Nama Supplier':<24} | {'Menyediakan':<42} |")
    print("-"*86)
    supplier_list = sorted(SUPPLIERS.keys())
    for i, kode in enumerate(supplier_list, start=1):
        data = SUPPLIERS[kode]
        items = list(data.get("produk", {}).keys())
        if not items and "menyediakan" in data:
            items = data["menyediakan"]
        menyediakan = ", ".join(items)[:42]
        print(f"| {i:<3} | {kode:<10} | {data['nama']:<24} | {menyediakan:<42} |")
    print("="*86)


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
# FUNGSI UTAMA
# ===============================
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
            while True:
                product_manager.show_products()
                
                print("\nOpsi:")
                print("- Ketik nomor produk untuk lihat detail resep")
                print("- Tekan Enter untuk kembali ke menu utama")
                
                lihat_resep = input("\nPilihan: ").strip()
                
                # Jika Enter (kosong), kembali ke menu utama
                if not lihat_resep:
                    break
                
                # Validasi input angka
                if not lihat_resep.isdigit():
                    print("❌ Input harus berupa angka!")
                    input("\nTekan Enter untuk melanjutkan...")
                    continue
                
                # Ambil produk berdasarkan nomor
                index = int(lihat_resep) - 1
                product = product_manager.get_product_by_index(index)
                
                if product:
                    product.show_recipe_table()
                    input("\nTekan Enter untuk melanjutkan...")
                else:
                    print("❌ Nomor produk tidak valid!")
                    input("\nTekan Enter untuk melanjutkan...")

        # ===============================
        # 2. LIHAT STOK BAHAN
        # ===============================
        elif pilihan == "2":
            while True:
                inventory.show_stock_table()
                
                print("\nOpsi:")
                print("- Ketik nomor bahan untuk detail")
                print("- Tekan Enter untuk kembali ke menu utama")
                
                pilih_bahan = input("\nPilihan: ").strip()
                
                # Jika Enter (kosong), kembali ke menu utama
                if not pilih_bahan:
                    break
                
                # Validasi input angka
                if not pilih_bahan.isdigit():
                    print("❌ Input harus berupa angka!")
                    input("\nTekan Enter untuk melanjutkan...")
                    continue
                
                # Ambil bahan berdasarkan nomor
                index = int(pilih_bahan) - 1
                bahan_list = list(inventory.stock.items())
                
                if 0 <= index < len(bahan_list):
                    nama_bahan, data = bahan_list[index]
                    status = inventory.get_status(data['qty'])
                    print(f"\n✓ Detail Bahan:")
                    print(f"  Nama   : {nama_bahan}")
                    print(f"  Stok   : {data['qty']} {data['unit']}")
                    print(f"  Status : {status}")
                else:
                    print("❌ Nomor bahan tidak valid!")
                
                input("\nTekan Enter untuk melanjutkan...")

        # ===============================
        # 3. TAMBAH PRODUK BARU
        # ===============================
        elif pilihan == "3":
            print("\n" + "="*60)
            print("TAMBAH PRODUK BARU - NGOPIKUY".center(60))
            print("="*60)
            print("(Tekan Enter tanpa isi untuk kembali)")
            nama = input("Nama produk: ").strip()
            if not nama:
                print("↩ Kembali ke menu utama")
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
            # Siapkan list bahan untuk validasi nomor
            bahan_list = list(inventory.stock.items())
            inventory.show_recipe_helper_table()
            
            print()
            print("Format: No_Bahan = Jumlah Satuan [Keterangan]")
            print("Contoh: 1 = 18 gram")
            print("        1 = 18 gram Espresso Hot")
            print("        3 = 150 ml Steamed Milk")
            print(f"Gunakan nomor urut 1-{len(bahan_list)} sesuai tabel di atas")
            print("Ketik 'selesai' untuk mengakhiri\n")

            while True:
                data = input("> ").strip()
                if data.lower() == "selesai":
                    break

                if "=" not in data:
                    print("❌ Format salah! Harus ada tanda '=' antara nomor bahan dan detail")
                    continue

                try:
                    nomor_str, detail = data.split("=", 1)
                    nomor_str = nomor_str.strip()
                    
                    # Validasi nomor
                    try:
                        nomor = int(nomor_str)
                        if nomor <= 0 or nomor > len(bahan_list):
                            print(f"❌ Nomor bahan tidak valid! Gunakan nomor 1-{len(bahan_list)}")
                            continue
                    except ValueError:
                        print(f"❌ Nomor '{nomor_str}' harus berupa angka!")
                        continue
                    
                    # Ambil nama bahan dari nomor
                    bahan = bahan_list[nomor - 1][0]
                    bahan_unit = bahan_list[nomor - 1][1]["unit"]
                    
                    parts = detail.strip().split()
                    
                    if len(parts) < 2:
                        print("❌ Format salah! Minimal harus ada Jumlah dan Satuan")
                        continue
                    
                    # Validasi jumlah
                    try:
                        jumlah = int(parts[0])
                        if jumlah <= 0:
                            print("❌ Jumlah harus lebih dari 0!")
                            continue
                    except ValueError:
                        print(f"❌ Jumlah '{parts[0]}' harus berupa angka!")
                        continue
                    
                    # Validasi satuan
                    satuan = parts[1].lower()
                    if satuan not in ["gram", "ml", "pcs"]:
                        print(f"❌ Satuan '{satuan}' tidak valid! Gunakan: gram, ml, atau pcs")
                        continue
                    
                    # Peringatan jika satuan tidak sesuai dengan bahan
                    if satuan != bahan_unit:
                        print(f"⚠ Warning: Bahan '{bahan}' biasanya menggunakan satuan '{bahan_unit}', bukan '{satuan}'")
                    
                    # Gabungkan semua kata setelah satuan sebagai keterangan
                    keterangan = " ".join(parts[2:]) if len(parts) > 2 else "-"
                    
                    recipe[bahan] = {
                        "qty": jumlah,
                        "unit": satuan,
                        "note": keterangan
                    }
                    print(f"✓ {bahan} ({jumlah} {satuan}) ditambahkan ke resep")
                    
                except Exception as e:
                    print(f"❌ Error: {str(e)}")

            if not recipe:
                print("❌ Minimal harus ada 1 resep!")
                continue
            
            product_manager.add_product(
                ProductFactory.create_product(nama, kategori, harga, recipe)
            )
            print(f"✓ Produk '{nama}' berhasil ditambahkan")

        # (slot 5 moved)

        # ===============================
        # 4. TAMBAH / RESTOCK BAHAN
        # ===============================
        elif pilihan == "4":
            print("\n" + "="*60)
            print("RESTOCK BAHAN - NGOPIKUY".center(60))
            print("="*60)
            try:
                print("(Tekan Enter tanpa isi untuk kembali)")
                bahan = input("Nama bahan: ").strip()
                if not bahan:
                    print("↩ Kembali ke menu utama")
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

        # (slot 7 re-mapped below for Pembelian)

        

        # ===============================
        # 5. JUAL MENU (PENJUALAN)
        # ===============================
        elif pilihan == "5":
            print("\n" + "="*65)
            print("TRANSAKSI PENJUALAN - NGOPIKUY".center(65))
            print("="*65)
            
            daftar_pesanan = []  # Simpan produk yang akan dijual
            
            # Loop untuk memungkinkan menambah multiple produk
            while True:
                product_manager.show_products_table_only()
                
                try: 
                    # Validasi input nomor menu dengan strict
                    while True:
                        pilih_input = input("\nPilih nomor menu: ").strip()
                        try:
                            pilih = int(pilih_input) - 1
                            product = product_manager.get_product_by_index(pilih)
                            if product:
                                break
                            else:
                                print("❌ Nomor menu tidak valid! Pilih dari daftar yang tersedia")
                        except ValueError:
                            print("❌ Input harus berupa angka!")
                    
                    # Validasi input jumlah pesanan dengan strict
                    while True:
                        jumlah_input = input("Jumlah pesanan: ").strip()
                        try:
                            jumlah_order = int(jumlah_input)
                            if jumlah_order > 0:
                                break
                            else:
                                print("❌ Jumlah harus lebih dari 0!")
                        except ValueError:
                            print("❌ Input harus berupa angka!")

                    # Pilih ukuran (hanya untuk produk kategori coffee/non-coffee, bukan pastry)
                    ukuran = "Regular"
                    harga_adjustment = 0
                    
                    if product.kategori.lower() in ["coffee", "non-coffee"]:
                        # Loop pilih ukuran dengan retry
                        while True:
                            print("\nPilih Ukuran:")
                            print("1. Kecil (S) - Rp 0")
                            print("2. Sedang (M) - Rp +2.000")
                            print("3. Besar (L) - Rp +4.000")
                            
                            ukuran_input = input("Pilihan (1-3): ").strip()
                            ukuran_map = {
                                "1": {"ukuran": "Kecil (S)", "harga": 0},
                                "2": {"ukuran": "Sedang (M)", "harga": 2000},
                                "3": {"ukuran": "Besar (L)", "harga": 4000}
                            }
                            
                            if ukuran_input in ukuran_map:
                                ukuran = ukuran_map[ukuran_input]["ukuran"]
                                harga_adjustment = ukuran_map[ukuran_input]["harga"]
                                break
                            else:
                                print("❌ Pilihan tidak valid! Masukkan 1, 2, atau 3")
                        
                        # Loop pilih suhu dengan retry
                        while True:
                            print("\nPilih Suhu:")
                            print("1. Panas")
                            print("2. Dingin")
                            
                            suhu_input = input("Pilihan (1-2): ").strip()
                            suhu_map = {"1": "Panas", "2": "Dingin"}
                            
                            if suhu_input in suhu_map:
                                suhu = suhu_map[suhu_input]
                                break
                            else:
                                print("❌ Pilihan tidak valid! Masukkan 1 atau 2")
                    else:
                        suhu = "-"

                    # Simpan pesanan ke daftar dengan detail ukuran & suhu
                    daftar_pesanan.append({
                        "produk": product,
                        "jumlah": jumlah_order,
                        "ukuran": ukuran,
                        "suhu": suhu,
                        "harga_adjustment": harga_adjustment
                    })
                    
                    print(f"\n✓ {product.name} ({ukuran}) {suhu} x{jumlah_order} ditambahkan ke pesanan")
                    
                    # Konfirmasi apakah ingin menambah produk lagi dengan validasi ketat
                    print("\n" + "-"*60)
                    while True:
                        lanjut = input("Tambah produk lagi? (ya/tidak): ").strip().lower()
                        if lanjut in ["ya", "y", "yes"]:
                            print("-"*60)
                            break
                        elif lanjut in ["tidak", "n", "no"]:
                            break
                        else:
                            print("❌ Input tidak valid! Masukkan 'ya' atau 'tidak'")
                    
                    if lanjut not in ["ya", "y", "yes"]:
                        break
                    
                except ValueError:
                    print("❌ Input tidak valid")
                    continue
            
            # Jika ada pesanan, lanjutkan ke detail dan pembayaran
            if not daftar_pesanan:
                print("❌ Tidak ada pesanan yang dibuat")
                continue
            
            try:
                # Tampilkan ringkasan pesanan dengan tabel yang rapi
                indent = "    "
                header = f"| {'No':<3} | {'Nama Bahan':<28} | {'Jumlah':>8} | {'Satuan':^8} | {'Keterangan':<15} |"
                table_width = len(header)
                sep = "-" * table_width
                
                print("\n" + "="*80)
                print("DETAIL RESEP PESANAN - NGOPIKUY".center(80))
                print("="*80)
                
                # Tampilkan setiap produk dengan format gabungan
                for i, item in enumerate(daftar_pesanan, 1):
                    product = item['produk']
                    jumlah = item['jumlah']
                    ukuran = item.get('ukuran', 'Regular')
                    suhu = item.get('suhu', '-')
                    harga_adjustment = item.get('harga_adjustment', 0)
                    harga_total = product.price + harga_adjustment
                    
                    print(f"\n[{i}] {product.name} ({ukuran}) {suhu} x{jumlah}")
                    print(f"{indent}Kategori : {product.kategori} | Harga : Rp {product.price:,}", end="")
                    if harga_adjustment > 0:
                        print(f" + Rp {harga_adjustment:,} (ukuran) = Rp {harga_total:,}")
                    else:
                        print()
                    
                    print(indent + sep)
                    print(indent + header)
                    print(indent + sep)
                    
                    for j, (bahan, data) in enumerate(product.recipe.items(), start=1):
                        row = (
                            f"| {j:<3} | {bahan:<28} | "
                            f"{data['qty']:>8} | {data['unit']:^8} | "
                            f"{data.get('note', '-'):<15} |"
                        )
                        print(indent + row)
                    
                    print(indent + sep)
                
                print("\n" + "="*80)

                # Input metode pembayaran dengan menu numerik dan retry logic
                metode_bayar = ""
                while True:
                    print("\nPilih Metode Pembayaran:")
                    print("1. Tunai")
                    print("2. Debit Card")
                    print("3. QRIS")
                    
                    metode_input = input("\nPilihan (1-3): ").strip()
                    
                    if metode_input == "1":
                        metode_bayar = "Tunai"
                        break
                    elif metode_input == "2":
                        # Sub-menu untuk jenis kartu debit dengan retry
                        while True:
                            print("\nPilih Jenis Kartu Debit:")
                            print("1. BCA Debit")
                            print("2. Mandiri Debit")
                            print("3. BRI Debit")
                            print("4. BNI Debit")
                            
                            debit_input = input("\nPilihan (1-4): ").strip()
                            debit_map = {
                                "1": "Debit - BCA",
                                "2": "Debit - Mandiri",
                                "3": "Debit - BRI",
                                "4": "Debit - BNI"
                            }
                            
                            if debit_input in debit_map:
                                metode_bayar = debit_map[debit_input]
                                break
                            else:
                                print("❌ Pilihan tidak valid! Masukkan 1, 2, 3, atau 4")
                        break
                        
                    elif metode_input == "3":
                        # Sub-menu untuk provider QRIS dengan retry
                        while True:
                            print("\nPilih Provider QRIS:")
                            print("1. GoPay")
                            print("2. DANA")
                            print("3. ShopeePay")
                            print("4. BCA Mobile")
                            
                            qris_input = input("\nPilihan (1-4): ").strip()
                            qris_map = {
                                "1": "QRIS - GoPay",
                                "2": "QRIS - DANA",
                                "3": "QRIS - ShopeePay",
                                "4": "QRIS - BCA Mobile"
                            }
                            
                            if qris_input in qris_map:
                                metode_bayar = qris_map[qris_input]
                                break
                            else:
                                print("❌ Pilihan tidak valid! Masukkan 1-4")
                        break
                    else:
                        print("❌ Pilihan tidak valid! Masukkan 1, 2, atau 3")

                # Buat transaksi penjualan
                id_penjualan = generate_id_penjualan(len(riwayat_transaksi))
                transaksi = Penjualan(id_penjualan, metode_bayar, username)
                
                # Cek & kurangi stok untuk setiap pesanan
                try:
                    for item in daftar_pesanan:
                        product = item['produk']
                        jumlah = item['jumlah']
                        harga_adjustment = item.get('harga_adjustment', 0)
                        
                        for _ in range(jumlah):
                            for bahan, data in product.recipe.items():
                                inventory.use_stock(bahan, data["qty"], username)
                            # Tambah produk dengan harga yang sudah disesuaikan dengan ukuran
                            transaksi.daftar_item.append({
                                "nama_produk": f"{product.name} ({item.get('ukuran', 'Regular')}) {item.get('suhu', '-')}",
                                "harga": product.price + harga_adjustment,
                                "jumlah": 1
                            })
                    
                    # Cetak struk
                    transaksi.cetak_struk()
                    
                    # Simpan ke riwayat
                    riwayat_transaksi.append(transaksi)
                    transaksi_manager.tambah_penjualan(transaksi)
                    
                    # Tambahkan ke antrian pesanan
                    antrian_pesanan.tambah_pesanan(transaksi)
                    
                    print(f"✓ TRANSAKSI BERHASIL | Total: Rp {transaksi.hitung_total_dengan_ppn():,}")
                    
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
        # 6. BELI BAHAN DARI SUPPLIER (PEMBELIAN)
        # ===============================
        elif pilihan == "6":
            while True:
                show_suppliers_table()
                
                # Input supplier
                supplier_list = sorted(SUPPLIERS.keys())
                supplier_input = input("\nPilih Nomor Supplier (kembali = menu utama): ").strip().lower()
                
                # Opsi keluar
                if supplier_input == "kembali":
                    print("Kembali ke menu utama...")
                    break
                
                if not supplier_input.isdigit():
                    print("❌ Input harus nomor atau 'kembali'!")
                    continue
                
                idx = int(supplier_input)
                if idx < 1 or idx > len(supplier_list):
                    print(f"❌ Nomor tidak valid! Pilih 1-{len(supplier_list)} atau 'kembali'")
                    continue
                
                kode_supplier = supplier_list[idx - 1]
                supplier = SUPPLIERS[kode_supplier]
                supplier_label = f"{kode_supplier} - {supplier['nama']}"
                
                katalog = list(supplier.get("produk", {}).items())
                if not katalog:
                    print("❌ Supplier tidak memiliki katalog")
                    continue
                
                # Tampilkan katalog dengan format rapi
                header = f"| {'No':<3} | {'Nama Bahan':<30} | {'Unit':^10} | {'Harga/Satuan':>14} |"
                table_width = len(header)
                sep = "-" * table_width
                
                print("\n" + "=" * table_width)
                print(f"KATALOG - {supplier['nama']}".center(table_width))
                print("=" * table_width)
                print(header)
                print(sep)
                for i, (bahan_nama, harga_unit) in enumerate(katalog, start=1):
                    unit = inventory.stock.get(bahan_nama, {}).get("unit", "pcs")
                    row = (
                        f"| {i:<3} | {bahan_nama:<30} | {unit:^10} | "
                        f"Rp {harga_unit:>12,} |"
                    )
                    print(row)
                print("=" * table_width)
                
                # Buat transaksi pembelian
                id_pembelian = generate_id_pembelian(len(transaksi_manager.riwayat_pembelian))
                transaksi_beli = Pembelian(id_pembelian, supplier_label, username)
                
                # Loop pilih item
                while True:
                    pilih_item = input("\nPilih Nomor Item: ").strip()
                    
                    if not pilih_item.isdigit():
                        print("❌ Input harus nomor!")
                        continue
                    
                    idx_item = int(pilih_item) - 1
                    if idx_item < 0 or idx_item >= len(katalog):
                        print(f"❌ Nomor tidak valid! Pilih 1-{len(katalog)}")
                        continue
                    
                    nama_bahan, harga_satuan = katalog[idx_item]
                    unit = inventory.stock.get(nama_bahan, {}).get("unit", "pcs")
                    
                    try:
                        jumlah = int(input(f"Jumlah ({unit}): "))
                        if jumlah <= 0:
                            print("❌ Jumlah harus lebih dari 0")
                            continue
                    except ValueError:
                        print("❌ Input tidak valid")
                        continue
                    
                    # Tambah item dan update stok
                    transaksi_beli.tambah_bahan(nama_bahan, jumlah, harga_satuan)
                    inventory.add_stock(nama_bahan, jumlah, username, unit=unit)
                    subtotal = jumlah * harga_satuan
                    print(f"✓ {nama_bahan} x{jumlah} {unit} @ Rp {harga_satuan:,} = Rp {subtotal:,}")
                    
                    # Konfirmasi tambah item lagi
                    tambah_lagi = input("\nTambah item lagi? (y/n): ").strip().lower()
                    if tambah_lagi != "y":
                        break
                
                # Tampilkan struk pembelian
                if transaksi_beli.daftar_item:
                    print("\n" + "="*86)
                    print("STRUK PEMBELIAN".center(86))
                    print("="*86)
                    print(f"Supplier: {supplier_label}")
                    print(f"ID Transaksi: {id_pembelian}")
                    print("-"*86)
                    for idx, item in enumerate(transaksi_beli.daftar_item, start=1):
                        subtotal = item['jumlah'] * item['harga_satuan']
                        print(f"{idx}. {item['nama_bahan']} x{item['jumlah']} @ Rp {item['harga_satuan']:,} = Rp {subtotal:,}")
                    total = transaksi_beli.konfirmasi_pembelian()
                    print("-"*86)
                    print(f"{'TOTAL':>66} Rp {total:>15,}")
                    print("="*86)
                    
                    transaksi_manager.tambah_pembelian(transaksi_beli)
                else:
                    print("\n⚠ Tidak ada item yang dipilih")
                
                # Konfirmasi sebelum kembali ke daftar supplier
                input("\nTekan Enter untuk kembali ke daftar supplier...")

        # ===============================
        # 7. LIHAT ANTRIAN PESANAN
        # ===============================
        elif pilihan == "7":
            antrian_pesanan.show_antrian()
            input("\nTekan Enter untuk kembali...")

        # ===============================
        # 8. UPDATE STATUS PESANAN
        # ===============================
        elif pilihan == "8":
            antrian_pesanan.show_antrian()
            
            # Jika tidak ada pesanan aktif, jangan minta input
            active_orders = antrian_pesanan.get_active()
            if not active_orders:
                input("\nTekan Enter untuk kembali...")
                continue
            
            try:
                # Validasi input nomor antrian dengan strict retry logic
                nomor_antrian = None
                while nomor_antrian is None:
                    try:
                        nomor_input = input("\nNomor urut pesanan (dari tabel di atas): ").strip()
                        nomor_antrian = int(nomor_input)
                        
                        if nomor_antrian <= 0 or nomor_antrian > len(active_orders):
                            print(f"❌ Nomor pesanan tidak valid! Gunakan nomor 1-{len(active_orders)}")
                            nomor_antrian = None
                    except ValueError:
                        print("❌ Input harus berupa angka!")
                
                pesanan = active_orders[nomor_antrian - 1]
                id_transaksi = pesanan.id_transaksi
                
                # Validasi pilihan status dengan strict retry logic
                status_baru = None
                while status_baru is None:
                    print("\nPilih Status Baru:")
                    print(f"1. {StatusPesanan.DISEDUH}")
                    print(f"2. {StatusPesanan.SIAP}")
                    print(f"3. {StatusPesanan.DIAMBIL}")
                    print(f"4. {StatusPesanan.BATAL}")
                    
                    status_pilihan = input("Pilih (1-4): ").strip()
                    
                    status_map = {
                        "1": StatusPesanan.DISEDUH,
                        "2": StatusPesanan.SIAP,
                        "3": StatusPesanan.DIAMBIL,
                        "4": StatusPesanan.BATAL
                    }
                    
                    if status_pilihan in status_map:
                        status_baru = status_map[status_pilihan]
                        antrian_pesanan.update_status_pesanan(id_transaksi, status_baru, username)
                    else:
                        print("❌ Pilihan tidak valid! Masukkan 1, 2, 3, atau 4")
                
            except ValueError:
                print("❌ Input tidak valid")
            
            input("\nTekan Enter untuk kembali...")

        # ===============================
        # 9. LAPORAN & ANALISIS
        # ===============================
        elif pilihan == "9":
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
        # 10. AUDIT LOG STOK
        # ===============================
        elif pilihan == "10":
            inventory.show_audit_logs(limit=30)
            input("\nTekan Enter untuk kembali...")

        # ===============================
        # 11. HAPUS PRODUK
        # ===============================
        elif pilihan == "11":
            product_manager.show_products()
            pilih = input("\nNomor produk yang ingin dihapus: ").strip()
            if not pilih.isdigit():
                print("❌ Input harus berupa angka!")
                continue
            index = int(pilih) - 1
            try:
                removed = product_manager.hapus_produk_by_index(index)
                print(f"✓ Produk '{removed.name}' berhasil dihapus")
            except ValueError as e:
                print(f"❌ {e}")

        # ===============================
        # 12. KELUAR
        # ===============================
        elif pilihan == "12":
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
