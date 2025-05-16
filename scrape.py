import requests
from datetime import datetime, timedelta
import time
import numpy as np
import pandas as pd
import os

# Daftar provinsi
provinsi_target = [
    "Aceh", "Bali", "Banten", "Bengkulu", "D.I Yogyakarta", "DKI Jakarta", "Gorontalo", "Jambi", "Jawa Barat",
    "Jawa Tengah", "Jawa Timur", "Kalimantan Barat", "Kalimantan Selatan", "Kalimantan Tengah", "Kalimantan Timur",
    "Kalimantan Utara", "Kepulauan Bangka Belitung", "Kepulauan Riau", "Lampung", "Maluku", "Maluku Utara",
    "Nusa Tenggara Barat", "Nusa Tenggara Timur", "Papua", "Papua Barat", "Papua Barat Daya", "Papua Pegunungan",
    "Papua Selatan", "Papua Tengah", "Riau", "Sulawesi Barat", "Sulawesi Selatan", "Sulawesi Tengah",
    "Sulawesi Tenggara", "Sulawesi Utara", "Sumatera Barat", "Sumatera Selatan", "Sumatera Utara"
]

def scrape_harga(tanggal, komoditas_id=27, komoditas_nama="Beras Premium", level_harga_id="3", max_retries=3):
    url = "https://api-panelhargav2.badanpangan.go.id/api/front/harga-peta-provinsi"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    tgl_format = tanggal.strftime("%d/%m/%Y")
    params = {
        "level_harga_id": level_harga_id,
        "komoditas_id": komoditas_id,
        "period_date": f"{tgl_format} - {tgl_format}",
        "multi_status_map[0]": "",
        "multi_province_id[0]": ""
    }

    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
        except requests.exceptions.RequestException as e:
            print(f"❌ Error koneksi saat mengakses {tgl_format}: {e}")
            time.sleep(5)
            continue

        if response.status_code == 200:
            try:
                data = response.json()
                hasil = []
                provinsi_ditemukan = set()

                for item in data.get("data", []):
                    provinsi = item.get("province_name", "").strip()
                    if provinsi in provinsi_target:
                        harga = item.get("rata_rata_geometrik")
                        try:
                            harga = float(harga) if harga not in [None, ""] else np.nan
                        except:
                            harga = np.nan

                        hasil.append({
                            "Tanggal": tgl_format,
                            "Komoditas": komoditas_nama,
                            "Provinsi": provinsi,
                            "Harga": harga
                        })
                        provinsi_ditemukan.add(provinsi)

                for provinsi in set(provinsi_target) - provinsi_ditemukan:
                    hasil.append({
                        "Tanggal": tgl_format,
                        "Komoditas": komoditas_nama,
                        "Provinsi": provinsi,
                        "Harga": np.nan
                    })

                return hasil
            except ValueError:
                print(f"❌ Response bukan JSON untuk {tgl_format}: {response.text}")
                return []
        elif response.status_code == 429:
            wait_time = 10 * (attempt + 1)
            print(f"🚫 Rate limit 429 untuk {tgl_format}. Menunggu {wait_time} detik...")
            time.sleep(wait_time)
        else:
            print(f"⚠️ Gagal akses {tgl_format}: {response.status_code}")
            return []

    print(f"❌ Gagal setelah {max_retries} percobaan untuk {tgl_format}.")
    return []

def tanggal_terakhir_tersimpan(file_csv):
    if os.path.exists(file_csv):
        df = pd.read_csv(file_csv, parse_dates=["Tanggal"], dayfirst=True)
        return df["Tanggal"].max().date()
    return None

if __name__ == "__main__":
    file_csv = "harga_beras_premium.csv"
    tanggal_akhir = datetime.today().date()
    tanggal_awal = tanggal_akhir - timedelta(days=3*365)

    tanggal_mulai = tanggal_awal
    last_saved_date = tanggal_terakhir_tersimpan(file_csv)
    if last_saved_date:
        tanggal_mulai = last_saved_date + timedelta(days=1)

    semua_data = []

    total_hari = (tanggal_akhir - tanggal_mulai).days + 1
    for i in range(total_hari):
        tgl = tanggal_mulai + timedelta(days=i)
        print(f"📅 Mengambil data tanggal {tgl.strftime('%d/%m/%Y')} ({i+1}/{total_hari})")
        hasil = scrape_harga(datetime.combine(tgl, datetime.min.time()))
        if hasil:
            df = pd.DataFrame(hasil)
            if os.path.exists(file_csv):
                df.to_csv(file_csv, mode="a", index=False, header=False)
            else:
                df.to_csv(file_csv, index=False)
            print(f"✅ Tersimpan: {tgl.strftime('%d/%m/%Y')}")
        else:
            print(f"⚠️ Data kosong/gagal untuk {tgl.strftime('%d/%m/%Y')}")

    print("🎉 Proses selesai.")