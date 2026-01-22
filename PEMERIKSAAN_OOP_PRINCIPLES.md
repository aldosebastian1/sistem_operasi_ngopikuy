# PEMERIKSAAN OOP PRINCIPLES & DESIGN PATTERNS

## Sistem Manajemen Coffee Shop - NGOPIKUY

---

## ✅ 1. SOLID PRINCIPLES

### S - Single Responsibility Principle ✅

Setiap class memiliki tanggung jawab tunggal:

- **ManajemenPersediaan**: Hanya mengelola stok bahan
- **Product**: Hanya merepresentasikan produk dan resepnya
- **TransaksiManager**: Hanya mengelola riwayat transaksi
- **LaporanManager**: Hanya membuat laporan analisis
- **ProductManager**: Hanya mengelola daftar produk
- **AntrianPesanan**: Hanya mengelola antrian pesanan

**File Reference**: [ngopikuy.py](ngopikuy.py#L273-L900)

---

### O - Open/Closed Principle ✅

Class terbuka untuk ekstensi, tertutup untuk modifikasi:

- **StatusStrategy**: Terbuka untuk menambah strategy baru
- **Product subclass**: Terbuka untuk menambah tipe produk baru (CoffeeProduct, NonCoffeeProduct, PastryProduct)
- **Observer**: Terbuka untuk menambah observer baru

**File Reference**:

- Strategy: [ngopikuy.py](ngopikuy.py#L255-L268)
- Product inheritance: [ngopikuy.py](ngopikuy.py#L720-L730)

---

### L - Liskov Substitution Principle ✅

Subclass dapat menggantikan superclass tanpa error:

- **CoffeeProduct** dapat digunakan di tempat **Product**
- **NonCoffeeProduct** dapat digunakan di tempat **Product**
- **PastryProduct** dapat digunakan di tempat **Product**
- **Penjualan** dapat digunakan di tempat **Transaksi**
- **Pembelian** dapat digunakan di tempat **Transaksi**
- **NotifikasiStok** dapat digunakan di tempat **Observer**

**File Reference**: [ngopikuy.py](ngopikuy.py#L96-L200)

---

### I - Interface Segregation Principle ✅

Interface yang spesifik dan tidak "gemuk":

- **Observer** - interface hanya dengan method `update()`
- **StatusStrategy** - interface hanya dengan method `get_status()`

**File Reference**: [ngopikuy.py](ngopikuy.py#L242-L268)

---

### D - Dependency Inversion Principle ✅

Ketergantungan pada abstraksi, bukan implementasi:

- ManajemenPersediaan bergantung pada **StatusStrategy** (abstraksi), bukan implementasi langsung
- Observer bergantung pada **Observer** base class, bukan NotifikasiStok langsung
- ProductFactory mengembalikan **Product** (abstraksi), bukan concrete class

**File Reference**: [ngopikuy.py](ngopikuy.py#L325), [ngopikuy.py](ngopikuy.py#L740-L755)

---

## ✅ 2. INHERITANCE (Pewarisan)

### 1. Transaction Hierarchy

```
Transaksi (Base Class)
├── Penjualan
└── Pembelian
```

**File Reference**: [ngopikuy.py](ngopikuy.py#L83-L200)

### 2. Product Hierarchy

```
Product (Base Class)
├── CoffeeProduct
├── NonCoffeeProduct
└── PastryProduct
```

**File Reference**: [ngopikuy.py](ngopikuy.py#L647-L730)

### 3. Observer Hierarchy

```
Observer (Base Class)
└── NotifikasiStok
```

**File Reference**: [ngopikuy.py](ngopikuy.py#L242-L251)

### 4. Strategy Hierarchy

```
StatusStrategy (Base Class)
└── DefaultStatusStrategy
```

**File Reference**: [ngopikuy.py](ngopikuy.py#L255-L268)

---

## ✅ 3. POLYMORPHISM

### Method Overriding

- **get_label()** di-override di CoffeeProduct, NonCoffeeProduct, PastryProduct
- \***\*str**()\*\* di-override di AuditLog
- \***\*iter**()\*\* di-override di ManajemenPersediaan

**File Reference**: [ngopikuy.py](ngopikuy.py#L722-L730)

### Polymorphic Calls

```python
# Dapat dipanggil dengan parent type tapi eksekusi child method
for product in product_list:
    print(product.get_label())  # Panggil method anak sesuai type-nya
    print(product.show_recipe_table())  # Polymorphic call
```

---

## ✅ 4. EXCEPTION HANDLING

### Custom Exception

```python
class StokTidakCukupError(Exception):
    pass
```

**File Reference**: [ngopikuy.py](ngopikuy.py#L204-L207)

### Try-Catch Usage

1. **Input validation**

   ```python
   try:
       jumlah = int(jumlah_str)
   except ValueError:
       print("❌ Input tidak valid")
   ```

2. **Stok checking**

   ```python
   if self.stock[bahan]["qty"] < jumlah:
       raise StokTidakCukupError(...)
   ```

3. **General exception handling**
   ```python
   try:
       # Operasi
   except ValueError as e:
       print(f"❌ {e}")
   except Exception as e:
       print(f"❌ Error: {str(e)}")
   ```

**File Reference**: [ngopikuy.py](ngopikuy.py#L1340-1360), [ngopikuy.py](ngopikuy.py#L1560-1590)

---

## ✅ 5. ITERATOR PATTERN

### **iter** Implementation

```python
def __iter__(self):
    return iter(self.stock.items())
```

**File Reference**: [ngopikuy.py](ngopikuy.py#L330-331)

### Usage

```python
# Iterasi stok menggunakan for loop
for bahan, data in inventory:
    print(f"{bahan}: {data['qty']} {data['unit']}")
```

---

## ✅ 6. DESIGN PATTERNS

### A. Singleton Pattern ✅

**Class**: ManajemenPersediaan, AntrianPesanan

```python
class ManajemenPersediaan:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

**Tujuan**: Hanya ada 1 instance inventory di seluruh aplikasi
**File Reference**: [ngopikuy.py](ngopikuy.py#L273-L290)

---

### B. Factory Pattern ✅

**Class**: ProductFactory

```python
class ProductFactory:
    @staticmethod
    def create_product(name, kategori, price, recipe):
        kategori = kategori.lower()
        if kategori == "coffee":
            return CoffeeProduct(...)
        elif kategori == "non-coffee":
            return NonCoffeeProduct(...)
        # ... dll
```

**Tujuan**: Membuat objek dengan cara terpusat dan fleksibel
**File Reference**: [ngopikuy.py](ngopikuy.py#L745-L758)

---

### C. Observer Pattern ✅

**Classes**: Observer, NotifikasiStok

```python
class Observer:
    def update(self, message):
        pass

class NotifikasiStok(Observer):
    def update(self, message):
        print(f"[NOTIFIKASI] {message}")

# Penggunaan
inventory.tambah_observer(NotifikasiStok())
inventory.add_stock(...)  # Akan trigger observer
```

**Tujuan**: Notifikasi otomatis saat stok berubah
**File Reference**: [ngopikuy.py](ngopikuy.py#L242-L251), [ngopikuy.py](ngopikuy.py#L366-370)

---

### D. Strategy Pattern ✅

**Classes**: StatusStrategy, DefaultStatusStrategy

```python
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

# Penggunaan
self.status_strategy = DefaultStatusStrategy()
status = self.get_status(jumlah)
```

**Tujuan**: Fleksibilitas mengubah algoritma status stok
**File Reference**: [ngopikuy.py](ngopikuy.py#L255-L268), [ngopikuy.py](ngopikuy.py#L325)

---

### E. Decorator Pattern ✅

**Function**: highlight_menu

```python
def highlight_menu(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

**File Reference**: [ngopikuy.py](ngopikuy.py#L630-635)

---

### F. Manager/Coordinator Pattern ✅

**Classes**: TransaksiManager, ProductManager, LaporanManager

- **TransaksiManager**: Mengkoordinir riwayat penjualan & pembelian
- **ProductManager**: Mengkoordinir daftar produk
- **LaporanManager**: Mengkoordinir laporan analisis

**File Reference**: [ngopikuy.py](ngopikuy.py#L820-920)

---

### G. Data Class Pattern ✅

**Class**: AuditLog, StatusPesanan

Menyimpan data dengan method tambahan untuk manipulasi

**File Reference**: [ngopikuy.py](ngopikuy.py#L222-238), [ngopikuy.py](ngopikuy.py#L211-220)

---

## 📊 RINGKASAN IMPLEMENTASI

| Aspek               | Status     | Bukti                              |
| ------------------- | ---------- | ---------------------------------- |
| **SOLID**           | ✅ Lengkap | 5/5 prinsip ter-implementasi       |
| **Inheritance**     | ✅ Lengkap | 4 hierarchy classes                |
| **Polymorphism**    | ✅ Lengkap | Method override di subclass        |
| **Exception**       | ✅ Lengkap | Custom exception + try-catch       |
| **Iterator**        | ✅ Lengkap | `__iter__` di ManajemenPersediaan  |
| **Design Patterns** | ✅ Lengkap | 7 design patterns ter-implementasi |

---

## 🎯 DESIGN PATTERNS YANG DIIMPLEMENTASIKAN

1. ✅ **Singleton** - ManajemenPersediaan, AntrianPesanan
2. ✅ **Factory** - ProductFactory
3. ✅ **Observer** - NotifikasiStok, Observer base
4. ✅ **Strategy** - StatusStrategy, DefaultStatusStrategy
5. ✅ **Decorator** - @highlight_menu
6. ✅ **Manager/Coordinator** - TransaksiManager, ProductManager, LaporanManager
7. ✅ **Iterator** - `__iter__` method

---

## 📝 KESIMPULAN

**Seluruh kode sudah memiliki:**

- ✅ SOLID Principles (5/5)
- ✅ Inheritance (4 hierarchy)
- ✅ Polymorphism (method override)
- ✅ Exception Handling (custom exception)
- ✅ Iterator Pattern (dunder methods)
- ✅ 7 Design Patterns

**Kode ini sudah LENGKAP dan SIAP untuk tugas UTS Pemrograman Berbasis Object!**

---

Generated: January 2026  
Program: Sistem Manajemen Coffee Shop NGOPIKUY
