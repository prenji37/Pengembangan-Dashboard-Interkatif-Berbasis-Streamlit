# Pengembangan-Dashboard-Interkatif-Berbasis-Streamlit
Pengembangan Dashboar Interaktif berbasis Streamlit untuk Pembangunan Daerah Kabupaten Tulungagung

# 📊 Dashboard Interaktif Statistik Pembangunan Kabupaten Tulungagung

Proyek ini merupakan hasil pengembangan dashboard visualisasi interaktif menggunakan Python dan Streamlit. Dashboard ini ditujukan untuk menyajikan data statistik pembangunan daerah secara lebih mudah dipahami, informatif, dan interaktif.

## Fitur Utama

- Upload atau pilih dataset bawaan
- Filter dinamis (tahun, kecamatan, jenis kelamin, dll.)
- Visualisasi interaktif: Line, Bar, Area, Pie, Histogram, Box, hingga 3D Scatter
- Penjelasan otomatis tiap grafik
- Ringkasan multi-indikator
- Unduh data hasil filter (.csv)

## 📁 Dataset

Data yang digunakan berasal dari **Badan Pusat Statistik Kabupaten Tulungagung**, meliputi:

- Indeks Pembangunan Manusia (IPM)
- Tingkat Partisipasi Angkatan Kerja (TPAK)
- Angka Harapan Hidup (AHH)
- Kemiskinan & Pengangguran
- Melek Huruf
- Jumlah Penduduk
- Jumlah Fasilitas Publik
- Faktor Kependudukan

Letakkan data Anda dalam folder: `data_folder/Data Clean/`

## Tampilan Dashboard

![Dashboard Preview](images/dashboard-preview.png)

## 🛠Instalasi dan Jalankan Aplikasi

```bash
# Clone repository ini
git clone https://github.com/username/dashboard-statistik-tulungagung.git
cd dashboard-statistik-tulungagung

# Buat virtual environment (opsional tapi disarankan)
python -m venv venv
source venv/bin/activate  # (Linux/Mac) atau venv\Scripts\activate  # (Windows)

# Install dependensi
pip install -r requirements.txt

# Jalankan aplikasi
streamlit run app.py
