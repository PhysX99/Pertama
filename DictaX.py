# ===========================================
# >>>  D I C T A X   by  P H Y S X  <<<
# ===========================================
# PROGRAM NAME : DictaX
# DIBUAT OLEH   : PhysX
# VERSI         : Final + CLI Menu + Custom Output Name
# ===========================================

import os
from itertools import product
from datetime import datetime

def kapital_variasi(kata):
    return list(set([kata.lower(), kata.upper(), kata.capitalize()]))

def vokal_to_angka(kata):
    trans = str.maketrans('aiueoAIUEO', '4133041330')
    return kata.translate(trans)

def tambah_simbol(kata):
    simbol = ['!', '@', '#', '$', '%', '&']
    hasil = []
    for s in simbol:
        hasil.append(s + kata)
        hasil.append(kata + s)
    return hasil

def gabung_tanggal(nama, tanggal):
    hasil = []
    for tgl in tanggal:
        hasil.append(nama + tgl)
        hasil.append(nama + '_' + tgl)
    return hasil

def gabung_kata_kunci(nama, kunci):
    hasil = []
    for k in kunci:
        hasil.append(nama + k)
        hasil.append(nama + '_' + k)
        hasil.append(nama + ' ' + k)
    return hasil

def gabung_angka_otomatis(nama):
    hasil = []
    for i in range(1, 6):
        num = ''.join(str(n) for n in range(1, i + 1))
        hasil.append(nama + num)
    return hasil

def load_leak_passwords(file_path):
    try:
        with open(file_path, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except:
        print("⚠️ Gagal membaca file leak.")
        return []

def generate_wordlist(nama_list, kata_kunci, tanggal_list, leak_list):
    hasil = set()

    for nama in nama_list:
        variasi_nama = kapital_variasi(nama.strip())

        for vn in variasi_nama:
            hasil.add(vn)
            hasil.add(vokal_to_angka(vn))

            for komb in gabung_kata_kunci(vn, kata_kunci):
                hasil.add(komb)
                hasil.add(vokal_to_angka(komb))

            for tanggal in gabung_tanggal(vn, tanggal_list):
                hasil.add(tanggal)
                hasil.add(vokal_to_angka(tanggal))

            for angka in gabung_angka_otomatis(vn):
                hasil.add(angka)

            for dengan_simbol in tambah_simbol(vn):
                hasil.add(dengan_simbol)

    hasil.update(leak_list)
    return sorted(hasil)

def tampil_menu():
    print("""
================================
   D I C T A X   -  by PhysX
================================
1. Generate Wordlist
2. Keluar
""")

def main():
    while True:
        tampil_menu()
        pilihan = input("Pilih menu (1/2): ")

        if pilihan == '1':
            nama_input = input("\nMasukkan daftar nama (pisah koma): ").split(',')
            kata_kunci_input = input("Masukkan kata kunci (pisah koma): ").split(',')
            tanggal_input = input("Masukkan tanggal (contoh: 08031999, pisah koma): ").split(',')

            use_leak = input("\nGunakan file leak password tambahan? (y/n): ").lower()
            leak_list = []
            if use_leak == 'y':
                path_leak = input("Masukkan path file leak (misal /sdcard/leak.txt): ")
                leak_list = load_leak_passwords(path_leak)

            wordlist = generate_wordlist(nama_input, kata_kunci_input, tanggal_input, leak_list)

            print("\n--- Penyimpanan Output ---")
            custom_filename = input("Masukkan nama file output (tanpa .txt), kosongkan untuk otomatis: ").strip()
            if custom_filename:
                filename = custom_filename + ".txt"
            else:
                filename = f"dictax_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

            path = "/data/data/com.termux/files/home/wordlist/"
            os.makedirs(path, exist_ok=True)
            full_path = os.path.join(path, filename)

            with open(full_path, 'w') as f:
                for word in wordlist:
                    f.write(word + '\n')

            print(f"\n✅ Wordlist berhasil disimpan di: {full_path}\n")
            input("Tekan Enter untuk kembali ke menu...")

        elif pilihan == '2':
            print("Keluar... Thanks For Using DictaX!")
            break
        else:
            print("Pilihan tidak valid. Coba lagi.")

if __name__ == "__main__":
    main()
