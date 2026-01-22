# Dokumentasi Class Diagram UML - NGOPIKUY Coffee Shop

## 📋 Ringkasan Sistem

Sistem Manajemen Coffee Shop "NGOPIKUY" menggunakan prinsip OOP dengan beberapa design pattern:

- **Inheritance** (Pewarisan)
- **Singleton** (ManajemenPersediaan)
- **Observer** (Notifikasi Stok)
- **Strategy** (Status Stok)
- **Factory** (ProductFactory)

---

## 🎯 CLASS UTAMA UNTUK DIAGRAM UML

### **1. TRANSACTION HIERARCHY (Inheritance)**

```
┌──────────────────┐
│    Transaksi     │ (Base Class)
├──────────────────┤
│ - id_transaksi   │
│ - tanggal        │
│ - username       │
│ - daftar_item[]  │
├──────────────────┤
│ + tambah_item()  │
└──────────────────┘
         △
         │ inherits
    ┌────┴─────┐
    │           │
┌───────────┐ ┌──────────────┐
│ Penjualan │ │  Pembelian   │
├───────────┤ ├──────────────┤
│-metode_   │ │-kode_        │
│  bayar    │ │  supplier    │
│-status    │ │-total_beli   │
│-waktu_    │ ├──────────────┤
│  diseduh  │ │+ tambah_     │
│-waktu_siap│ │  bahan()     │
├───────────┤ │+ konfirmasi_ │
│+ update_  │ │  pembelian() │
│  status() │ └──────────────┘
│+ hitung_  │
│  subtotal │
│+ cetak_   │
│  struk()  │
└───────────┘
```

**File Reference:** [ngopikuy.py](ngopikuy.py#L83-L201)

| Class       | Type       | Deskripsi                                                                                  |
| ----------- | ---------- | ------------------------------------------------------------------------------------------ |
| `Transaksi` | Base Class | Kelas dasar untuk semua transaksi, menyimpan ID, tanggal, user, dan daftar item            |
| `Penjualan` | Child      | Transaksi penjualan ke customer dengan tracking status (DIBUAT → DISEDUH → SIAP → DIAMBIL) |
| `Pembelian` | Child      | Transaksi pembelian bahan baku dari supplier                                               |

---

### **2. INVENTORY MANAGEMENT (Singleton + Pattern)**

```
┌─────────────────────────────┐
│  ManajemenPersediaan        │ (Singleton)
├─────────────────────────────┤
│ - _instance (static)        │
│ - stock {}                  │
│ - alias {}                  │
│ - audit_logs[]              │
│ - observers[]               │
│ - status_strategy           │
├─────────────────────────────┤
│ + __new__()                 │
│ + add_stock()               │
│ + use_stock()               │
│ + cari_bahan()              │
│ + show_stock_table()        │
│ + tambah_observer()         │
│ + _notify()                 │
│ + __iter__()                │
└─────────────────────────────┘
        │ uses
        ├─────────────────────┬───────────────────┐
        │                     │                   │
   ┌─────────────┐    ┌───────────────┐   ┌─────────────┐
   │ Observer    │    │ StatusStrategy│   │  AuditLog   │
   ├─────────────┤    ├───────────────┤   ├─────────────┤
   │+ update()   │    │+ get_status() │   │- username   │
   └─────────────┘    └───────────────┘   │- aksi       │
        △                    △              │- bahan      │
        │ implements         │ implements   │- jumlah     │
   ┌─────────────────┐  ┌──────────────────┐ │- unit    │
   │NotifikasiStok   │  │DefaultStatus     │ │- waktu    │
   │                 │  │Strategy          │ └─────────────┘
   └─────────────────┘  └──────────────────┘
```

**File Reference:** [ngopikuy.py](ngopikuy.py#L222-L570)

| Class                   | Type           | Deskripsi                                                                     |
| ----------------------- | -------------- | ----------------------------------------------------------------------------- |
| `ManajemenPersediaan`   | Singleton      | Mengelola stok bahan, menggunakan Singleton pattern agar hanya ada 1 instance |
| `Observer`              | Interface/Base | Base class untuk observer pattern                                             |
| `NotifikasiStok`        | Observer       | Implementasi observer untuk notifikasi stok yang menipis                      |
| `StatusStrategy`        | Interface/Base | Base class untuk strategy pattern                                             |
| `DefaultStatusStrategy` | Strategy       | Menentukan status stok: HABIS, MENIPIS, AMAN                                  |
| `AuditLog`              | Data Class     | Mencatat setiap perubahan stok (TAMBAH/PAKAI)                                 |

---

### **3. PRODUCT MANAGEMENT (Factory Pattern)**

```
┌──────────────────┐
│    Product       │ (Base Class)
├──────────────────┤
│ - name           │
│ - price          │
│ - ingredients[]  │
├──────────────────┤
│ + get_resep()    │
│ + get_harga()    │
└──────────────────┘
        △
        │ inherits
    ┌───┴────┬──────────┐
    │        │          │
┌──────────┐ ┌──────────┐ ┌──────────┐
│ Coffee   │ │NonCoffee │ │ Pastry   │
│Product   │ │Product   │ │Product   │
└──────────┘ └──────────┘ └──────────┘

┌──────────────────────┐
│  ProductFactory      │ (Factory Pattern)
├──────────────────────┤
│ + create_product()   │
│ + get_all_products() │
└──────────────────────┘
        │ creates
        └──→ Product instances

┌──────────────────────┐
│  ProductManager      │
├──────────────────────┤
│ - daftar_produk[]    │
├──────────────────────┤
│ + tampilkan_menu()   │
│ + cari_produk()      │
│ + lihat_resep()      │
└──────────────────────┘
```

**File Reference:** [ngopikuy.py](ngopikuy.py#L641-L800)

| Class              | Type       | Deskripsi                                     |
| ------------------ | ---------- | --------------------------------------------- |
| `Product`          | Base Class | Kelas dasar untuk semua produk                |
| `CoffeeProduct`    | Child      | Produk minuman kopi                           |
| `NonCoffeeProduct` | Child      | Produk minuman non-kopi                       |
| `PastryProduct`    | Child      | Produk makanan/pastry                         |
| `ProductFactory`   | Factory    | Factory pattern untuk membuat instance produk |
| `ProductManager`   | Manager    | Mengelola daftar produk dan menampilkan menu  |

---

### **4. QUEUE MANAGEMENT**

```
┌──────────────────────┐
│  AntrianPesanan      │ (Queue Data Structure)
├──────────────────────┤
│ - antrian []         │
│ - counter_id         │
├──────────────────────┤
│ + tambah_pesanan()   │
│ + ambil_pesanan()    │
│ + tampilkan_antrian()│
│ + ukuran()           │
└──────────────────────┘
        │ uses
        └──→ Penjualan
```

**File Reference:** [ngopikuy.py](ngopikuy.py#L571-L640)

| Class            | Deskripsi                                                  |
| ---------------- | ---------------------------------------------------------- |
| `AntrianPesanan` | Mengelola antrian pesanan dengan implementasi queue (FIFO) |

---

### **5. TRANSACTION & REPORT MANAGEMENT**

```
┌──────────────────────────┐
│  TransaksiManager        │
├──────────────────────────┤
│ - riwayat_penjualan[]    │
│ - riwayat_pembelian[]    │
├──────────────────────────┤
│ + tambah_penjualan()     │
│ + tambah_pembelian()     │
│ + tampilkan_riwayat_     │
│   penjualan()            │
│ + tampilkan_riwayat_     │
│   pembelian()            │
└──────────────────────────┘
        │ contains
        ├──→ Penjualan[]
        └──→ Pembelian[]

┌──────────────────────────┐
│  LaporanManager          │ (Static Methods)
├──────────────────────────┤
│ + laporan_penjualan_     │
│   harian()               │
│ + laporan_stok_menipis() │
└──────────────────────────┘
        │ uses
        ├──→ TransaksiManager
        └──→ ManajemenPersediaan
```

**File Reference:** [ngopikuy.py](ngopikuy.py#L804-L891)

| Class              | Deskripsi                                                 |
| ------------------ | --------------------------------------------------------- |
| `TransaksiManager` | Mengelola riwayat semua transaksi (penjualan & pembelian) |
| `LaporanManager`   | Membuat laporan analisis penjualan dan stok               |

---

### **6. STATUS & EXCEPTION**

```
┌──────────────────────┐
│  StatusPesanan       │ (Constants)
├──────────────────────┤
│ + DIBUAT             │
│ + DISEDUH            │
│ + SIAP               │
│ + DIAMBIL            │
│ + BATAL              │
└──────────────────────┘

┌──────────────────────┐
│StokTidakCukupError   │ (Exception)
├──────────────────────┤
│ inherits from        │
│ Exception            │
└──────────────────────┘
```

**File Reference:** [ngopikuy.py](ngopikuy.py#L204-L220)

---

## 📊 RELATIONSHIP DIAGRAM

### **Associations & Dependencies:**

```
┌────────────────────────────────────────────────────────────┐
│                      SISTEM NGOPIKUY                        │
└────────────────────────────────────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
        ▼           ▼           ▼
   Penjualan   Pembelian   AntrianPesanan
        │           │           │
        ├─────────┬─┘           │
        │         │             │
        └─────────┼─────────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
        ▼                   ▼
TransaksiManager    ProductManager
        │                   │
        ├───────────┬───────┘
        │           │
        ▼           ▼
   LaporanManager  ManajemenPersediaan
        │                   │
        └───────────┬───────┘
                    │
            ┌───────┴───────┐
            │               │
            ▼               ▼
        Observer        Strategy
            │               │
            ▼               ▼
    NotifikasiStok  DefaultStatusStrategy
```

---

## 🔑 KEY DESIGN PATTERNS DIGUNAKAN

| Pattern         | Class                                                  | Fungsi                                       |
| --------------- | ------------------------------------------------------ | -------------------------------------------- |
| **Inheritance** | Transaksi → Penjualan/Pembelian                        | Polymorphism untuk berbagai tipe transaksi   |
| **Inheritance** | Product → CoffeeProduct/NonCoffeeProduct/PastryProduct | Polymorphism untuk berbagai tipe produk      |
| **Singleton**   | ManajemenPersediaan                                    | Hanya ada 1 instance untuk manajemen stok    |
| **Observer**    | NotifikasiStok extends Observer                        | Notifikasi otomatis saat stok berubah        |
| **Strategy**    | DefaultStatusStrategy implements StatusStrategy        | Fleksibilitas untuk mengubah logika status   |
| **Factory**     | ProductFactory                                         | Membuat instance produk dengan cara terpusat |
| **Manager**     | TransaksiManager, ProductManager, LaporanManager       | Centralized management untuk berbagai entity |

---

## 📌 ATTRIBUTE & METHOD DETAILS

### **Penjualan Class (Most Important)**

```
Attributes:
  - id_transaksi: str
  - metode_bayar: str (cash/card/transfer)
  - status: str (StatusPesanan enum)
  - waktu_dibuat, waktu_diseduh, waktu_siap, waktu_selesai: datetime
  - daftar_item: list[dict]

Methods:
  - update_status(status_baru, username): void
  - tambah_produk(produk: Product, jumlah: int): void
  - hitung_subtotal(): int
  - hitung_ppn(): int
  - hitung_total_dengan_ppn(): int
  - cetak_struk(): void
```

### **ManajemenPersediaan Class (Most Important)**

```
Singleton Pattern:
  - _instance: static

Attributes:
  - stock: dict {nama_bahan: {qty, unit}}
  - alias: dict {alias_name: actual_name}
  - audit_logs: list[AuditLog]
  - observers: list[Observer]

Methods:
  - add_stock(bahan, jumlah, username, unit): void
  - use_stock(bahan, jumlah, username): void
  - cari_bahan(nama): dict
  - get_status(jumlah): str
  - show_stock_table(): void
  - tambah_observer(observer): void
```

### **ProductManager Class**

```
Attributes:
  - daftar_produk: list[Product]

Methods:
  - tampilkan_menu(): void
  - cari_produk(nama): Product
  - lihat_resep(produk_name): void
```

---

## 🎨 UML DIAGRAM SUMMARY

Untuk membuat diagram UML di tool seperti:

- **Lucidchart**
- **Draw.io** (diagrams.net)
- **PlantUML**
- **StarUML**
- **ArgoUML**

**Gunakan informasi:**

1. **Class Boxes** dengan 3 section (Name, Attributes, Methods)
2. **Arrows untuk Inheritance**: Segitiga putih menunjuk ke parent
3. **Arrows untuk Composition**: Diamond hitam untuk "uses"
4. **Arrows untuk Association**: Garis biasa untuk relationships
5. **Multiplicity**: \* untuk many, 1 untuk one

---

## 📝 NOTES UNTUK DOKUMENTASI

- **Singleton Pattern**: ManajemenPersediaan hanya boleh ada 1 instance di seluruh aplikasi
- **Observer Pattern**: Sistem akan notify semua observers saat ada perubahan stok
- **Strategy Pattern**: Status stok bisa diubah dengan mengimplementasi interface StatusStrategy
- **Inheritance Chain**: Penjualan & Pembelian mewarisi dari Transaksi base class
- **Queue Implementation**: AntrianPesanan menggunakan FIFO (First In First Out)

---

**Generated for**: UTS - Pemrograman Berbasis Object  
**Program**: Sistem Manajemen Coffee Shop NGOPIKUY  
**Date**: January 2026
