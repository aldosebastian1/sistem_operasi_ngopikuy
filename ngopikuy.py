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
