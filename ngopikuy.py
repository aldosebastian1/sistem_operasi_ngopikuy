# =========================
# DECORATOR
# =========================
def highlight_menu(func):
    def wrapper(*args, **kwargs):
        print("\n MENU PILIHAN ")
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

