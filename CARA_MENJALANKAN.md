# SISTEM MANAJEMEN COFFEE SHOP - NGOPIKUY

## Cara Menjalankan Program

### 1. Pastikan Python Terinstall

```bash
py --version
```

Harus menampilkan Python 3.x.x

### 2. Jalankan Program

```bash
py ngopikuy.py
```

### 3. Menu Utama

Program akan menampilkan 9 menu pilihan:

1. **Tambah / Restock Bahan** - Menambah stok bahan baku
2. **Lihat Stok Bahan** - Menampilkan semua stok dengan status
3. **Tambah Produk** - Menambah menu produk baru
4. **Lihat Daftar Produk** - Menampilkan semua produk tersedia
5. **Cari Bahan** - Mencari bahan tertentu di inventory
6. **Jual Menu** - Proses transaksi penjualan
7. **Hapus Produk** - Menghapus produk dari daftar
8. **Laporan & Analisis** - Laporan penjualan dan stok
9. **Keluar** - Keluar dari program

## Fitur Program

### ✅ Pattern OOP yang Diimplementasikan:

1. **Inheritance** - Class Penjualan & Pembelian inherit dari Transaksi
2. **Polymorphism** - CoffeeProduct, NonCoffeeProduct, PastryProduct
3. **Encapsulation** - Private attributes dengan getter/setter
4. **Abstraction** - Class Product sebagai base class
5. **Singleton** - ManajemenPersediaan (hanya 1 instance)
6. **Factory Pattern** - ProductFactory untuk create produk
7. **Observer Pattern** - NotifikasiStok untuk monitoring stok
8. **Strategy Pattern** - StatusStrategy untuk status stok
9. **Decorator Pattern** - @highlight_menu untuk UI
10. **Iterator Pattern** - **iter** untuk iterasi koleksi

### 📦 Fitur Manajemen Stok:

- Auto-detect bahan habis/menipis
- Notifikasi real-time
- Support alias bahan (contoh: "Susu" → "Susu Full Cream")

### 💰 Fitur Transaksi:

- Cetak struk otomatis
- Multiple payment methods
- Riwayat transaksi
- Rollback jika stok tidak cukup

### 📊 Fitur Laporan:

- Laporan penjualan harian
- Laporan stok menipis
- Riwayat semua transaksi

## Produk Default:

- Latte (Coffee) - Rp 22,000
- Americano (Coffee) - Rp 20,000
- Taro Latte (Non-Coffee) - Rp 23,000
- Croissant (Pastry) - Rp 15,000

## Contoh Penggunaan:

### Jual Produk:

1. Pilih menu 6
2. Pilih nomor produk
3. Masukkan jumlah pesanan
4. Masukkan metode pembayaran
5. Struk akan tercetak otomatis

### Tambah Produk Baru:

1. Pilih menu 3
2. Masukkan nama produk
3. Pilih kategori (Coffee/Non-Coffee/Pastry)
4. Masukkan harga
5. Masukkan resep dengan format: `Bahan = jumlah satuan keterangan`
6. Ketik `stop` jika selesai

## Error Handling:

- ✅ Validasi input angka
- ✅ Validasi stok tersedia
- ✅ Exception handling untuk stok tidak cukup
- ✅ Rollback transaksi jika gagal

## Author:

Sistem Operasi Ngopikuy - © 2026
Pemrograman Berbasis Object - UTS

---

**Note**: Program menggunakan nama "NGOPIKUY" di seluruh interface untuk konsistensi branding.
