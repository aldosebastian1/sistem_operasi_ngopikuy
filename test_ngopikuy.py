# Test Script untuk Sistem Ngopikuy
# Tes import dan fungsi dasar

print("="*70)
print("TEST SISTEM NGOPIKUY".center(70))
print("="*70)

try:
    # Test 1: Import module
    print("\n[TEST 1] Import module...")
    import ngopikuy
    print("✓ Import berhasil!")
    
    # Test 2: Singleton pattern
    print("\n[TEST 2] Test Singleton Pattern...")
    inv1 = ngopikuy.ManajemenPersediaan()
    inv2 = ngopikuy.ManajemenPersediaan()
    assert inv1 is inv2, "Singleton tidak bekerja!"
    print("✓ Singleton bekerja dengan baik!")
    
    # Test 3: Factory pattern
    print("\n[TEST 3] Test Factory Pattern...")
    product = ngopikuy.ProductFactory.create_product(
        "Test Coffee", "coffee", 25000, {}
    )
    assert isinstance(product, ngopikuy.CoffeeProduct)
    print("✓ Factory pattern bekerja!")
    
    # Test 4: Observer pattern
    print("\n[TEST 4] Test Observer Pattern...")
    observer = ngopikuy.NotifikasiStok()
    ngopikuy.inventory.tambah_observer(observer)
    print("✓ Observer berhasil ditambahkan!")
    
    # Test 5: Inventory operations
    print("\n[TEST 5] Test Inventory Operations...")
    before = ngopikuy.inventory.stock["Bubuk Kopi"]["qty"]
    ngopikuy.inventory.add_stock("Bubuk Kopi", 100)
    after = ngopikuy.inventory.stock["Bubuk Kopi"]["qty"]
    assert after == before + 100, "Add stock gagal!"
    print(f"✓ Add stock berhasil! {before} -> {after}")
    
    # Test 6: Strategy pattern
    print("\n[TEST 6] Test Strategy Pattern...")
    status_aman = ngopikuy.inventory.get_status(100)
    status_menipis = ngopikuy.inventory.get_status(5)
    status_habis = ngopikuy.inventory.get_status(0)
    assert status_aman == "AMAN"
    assert status_menipis == "MENIPIS"
    assert status_habis == "HABIS"
    print("✓ Strategy pattern bekerja!")
    
    # Test 7: Product Manager
    print("\n[TEST 7] Test Product Manager...")
    initial_count = len(ngopikuy.product_manager.products)
    test_product = ngopikuy.ProductFactory.create_product(
        "Test Matcha", "non-coffee", 28000, {}
    )
    ngopikuy.product_manager.add_product(test_product)
    new_count = len(ngopikuy.product_manager.products)
    assert new_count == initial_count + 1
    print(f"✓ Product Manager bekerja! Produk: {initial_count} -> {new_count}")
    
    # Test 8: Transaksi
    print("\n[TEST 8] Test Transaksi...")
    transaksi = ngopikuy.Penjualan("TEST-001", "Tunai")
    assert transaksi.id_transaksi == "TEST-001"
    assert transaksi.metode_bayar == "Tunai"
    print("✓ Transaksi berhasil dibuat!")
    
    # Test 9: Exception handling
    print("\n[TEST 9] Test Exception Handling...")
    try:
        ngopikuy.inventory.use_stock("Bubuk Kopi", 999999999)
        print("❌ Exception tidak ditangkap!")
    except ngopikuy.StokTidakCukupError:
        print("✓ Exception handling bekerja!")
    
    # Test 10: Iterator pattern
    print("\n[TEST 10] Test Iterator Pattern...")
    count = 0
    for bahan, data in ngopikuy.inventory:
        count += 1
    print(f"✓ Iterator bekerja! Total bahan: {count}")
    
    print("\n" + "="*70)
    print("SEMUA TEST BERHASIL! ✓".center(70))
    print("="*70)
    print("\nSistem siap digunakan!")
    print("Jalankan dengan: py ngopikuy.py")
    
except Exception as e:
    print(f"\n❌ TEST GAGAL: {e}")
    import traceback
    traceback.print_exc()
