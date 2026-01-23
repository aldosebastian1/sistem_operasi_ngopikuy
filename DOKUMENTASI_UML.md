# Dokumentasi Class Diagram UML - NGOPIKUY Coffee Shop

## Ringkasan Sistem

Sistem POS konsol NGOPIKUY dibangun dengan OOP dan pola desain untuk modularitas dan konsistensi state.

**Design Patterns**: Inheritance (Transaksi → Penjualan/Pembelian), Singleton (ManajemenPersediaan), Observer, Strategy, Factory, Iterator.

**Fitur Inti**: Penjualan multi-item (ukuran/suhu/metode bayar), pembelian/restock 7 supplier, inventory real-time + audit log, antrian pesanan dengan status, laporan penjualan/pembelian/metode bayar/stok menipis, CRUD produk dengan resep.

---

## Fokus Class UML

| Tipe        | Class               | Status         | Alasan                                                  |
| ----------- | ------------------- | -------------- | ------------------------------------------------------- |
| Child Class | Penjualan           | ✅ CLASS UTAMA | Dipakai langsung untuk transaksi penjualan              |
| Child Class | Pembelian           | ✅ CLASS UTAMA | Dipakai langsung untuk transaksi pembelian              |
| Singleton   | ManajemenPersediaan | ✅ CLASS UTAMA | Inventori tunggal, mengelola stok dan audit log         |
| Base Class  | Transaksi           | ⚠️ SUPPORTING  | Abstrak untuk inheritance, tidak diinstansiasi langsung |

Class pendukung: `Observer`, `StatusStrategy`, `AuditLog` (implementasi pola).

---

## Diagram UML (teks)

### 1) Hierarki Transaksi

```
                  ┌──────────────────────────┐
                  │    <<abstract>>          │
                  │       Transaksi          │
                  ├──────────────────────────┤
                  │ - id_transaksi: str      │
                  │ - tanggal_transaksi: str │
                  │ - username: str          │
                  │ - daftar_item: list      │
                  ├──────────────────────────┤
                  │ + tambah_item(item)      │
                  └──────────────────────────┘
                           △
                           │
              ┌────────────┴────────────┐
              │                         │
    ┌─────────────────────┐   ┌────────────────────┐
    │     Penjualan       │   │     Pembelian      │
    ├─────────────────────┤   ├────────────────────┤
    │ - metode_bayar: str │   │ - kode_supplier: str│
    │ - status: str       │   │ - total_beli: int   │
    │ - waktu_*: datetime │   ├────────────────────┤
    ├─────────────────────┤   │ + tambah_bahan()    │
    │ + update_status()   │   │ + konfirmasi_       │
    │ + hitung_subtotal() │   │   pembelian()       │
    │ + hitung_ppn()      │   └────────────────────┘
    │ + hitung_total_     │
    │   dengan_ppn()      │
    │ + cetak_struk()     │
    └─────────────────────┘
```

Sumber: [ngopikuy.py](ngopikuy.py#L1-L220)

### 2) Inventory (Singleton + Observer + Strategy)

```
              ┌─────────────────────────────────────┐
              │  <<singleton>> ManajemenPersediaan  │
              ├─────────────────────────────────────┤
              │ - _instance: static                 │
              │ - stock, alias, audit_logs          │
              │ - observers: list[Observer]         │
              │ - status_strategy: StatusStrategy   │
              ├─────────────────────────────────────┤
              │ + add_stock(bahan, jumlah, unit)    │
              │ + use_stock(bahan, jumlah)          │
              │ + cari_bahan(nama)                  │
              │ + get_status(jumlah)                │
              │ + show_stock_table()                │
              │ + show_audit_logs(limit)            │
              │ + tambah_observer(obs)              │
              └─────────────────────────────────────┘
                    │ uses       │ uses        │ contains
                    ▼            ▼             ▼
        ┌────────────────┐  ┌────────────────┐  ┌─────────────────┐
        │ <<interface>>  │  │ <<interface>>  │  │    AuditLog     │
        │   Observer     │  │ StatusStrategy │  ├─────────────────┤
        ├────────────────┤  ├────────────────┤  │- username: str  │
        │+ update(msg)   │  │+ get_status(q) │  │- aksi: str      │
        └────────────────┘  └────────────────┘  │- bahan: str     │
               △                   △             │- jumlah: int    │
               │ implements        │ implements  │- unit: str      │
        ┌──────────────┐   ┌─────────────────┐   │- waktu: str     │
        │NotifikasiStok│   │DefaultStatus    │   └─────────────────┘
        └──────────────┘   │Strategy         │
                           └─────────────────┘
```

Catatan: `use_stock` dapat melempar `StokTidakCukupError` bila stok kurang.
Sumber: [ngopikuy.py](ngopikuy.py#L221-L570)

### 3) Relasi Utama (ringkas)

```
Transaksi △── Penjualan
Transaksi △── Pembelian
Penjualan ──uses──▶ ManajemenPersediaan
Pembelian ──uses──▶ ManajemenPersediaan
ManajemenPersediaan ◆── AuditLog (composition)
Observer ◁── NotifikasiStok
StatusStrategy ◁── DefaultStatusStrategy
```

---

## Detail Kelas Inti

**Penjualan (CLASS UTAMA)**

- Atribut: id_transaksi, metode_bayar, status, waktu_dibuat/diseduh/siap/selesai, daftar_item
- Method: update_status, tambah_produk, hitung_subtotal, hitung_ppn, hitung_total_dengan_ppn, cetak_struk
- Logika: ukuran S/M/L (adjust harga), suhu panas/dingin, metode bayar Tunai/Debit/QRIS, auto-kurangi stok, PPN 11%, masuk antrian pesanan

**Pembelian (CLASS UTAMA)**

- Atribut: id_transaksi, kode_supplier, total_beli, daftar_item
- Method: tambah_bahan, konfirmasi_pembelian
- Logika: katalog 7 supplier, auto-update stok, multi-item per transaksi

**ManajemenPersediaan (CLASS UTAMA, Singleton)**

- Atribut: stock, alias, audit_logs, observers, status_strategy
- Method: add_stock, use_stock, cari_bahan, get_status, show_stock_table, show_audit_logs, tambah_observer
- Logika: konversi kg→gram, alias nama bahan, audit trail, observer notif MENIPIS/HABIS, strategy status stok

**Transaksi (Base, Supporting)**

- Atribut: id_transaksi, tanggal_transaksi, username, daftar_item
- Method: tambah_item
- Peran: base/abstrak, tidak diinstansiasi langsung

---

## Panduan Gambar Diagram (ringkas)

1. Empat kelas utama: Transaksi (<<abstract>>), Penjualan, Pembelian, ManajemenPersediaan (<<singleton>>)
2. Generalization: Penjualan → Transaksi, Pembelian → Transaksi (segitiga putih ke parent)
3. Dependency: Penjualan/Pembelian → ManajemenPersediaan (panah putus-putus <<uses>>)
4. Composition: ManajemenPersediaan ◆→ AuditLog (0..\*)
5. Implementasi: Observer ◁── NotifikasiStok, StatusStrategy ◁── DefaultStatusStrategy

---

## Ringkasan Pattern vs Kelas

| Pattern     | Kelas                                                 | Catatan                       |
| ----------- | ----------------------------------------------------- | ----------------------------- |
| Singleton   | ManajemenPersediaan                                   | Instance tunggal inventory    |
| Inheritance | Transaksi → Penjualan, Pembelian                      | Reuse atribut/metode dasar    |
| Observer    | Observer, NotifikasiStok                              | Notifikasi stok MENIPIS/HABIS |
| Strategy    | StatusStrategy, DefaultStatusStrategy                 | Logika status stok fleksibel  |
| Factory     | ProductFactory                                        | Pembuatan produk terpusat     |
| Iterator    | ManajemenPersediaan.**iter**, ProductManager.**iter** | Iterasi stok/produk           |

---

Rujukan kode: [ngopikuy.py](ngopikuy.py)
