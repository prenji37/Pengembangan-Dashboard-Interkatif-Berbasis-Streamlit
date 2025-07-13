
import streamlit as st
import pandas as pd
import os
import plotly.express as px


# ---------------------
# 🧱 Konfigurasi Awal
# ---------------------
st.set_page_config(page_title="Dashboard Statistik Tulungagung", layout="wide", page_icon="📊")
st.title("📊 Dashboard Interaktif Statistik Pembangunan Kabupaten Tulungagung")
st.caption("Disusun oleh: Riva Dian Ardiansyah • S1 Sains Data – Universitas Negeri Surabaya")

DATA_FOLDER = "data_folder/Data Clean"

@st.cache_data
def load_csv_files(folder_path):
    data = {}
    for file in os.listdir(folder_path):
        if file.endswith(".csv"):
            try:
                df = pd.read_csv(os.path.join(folder_path, file))
                
                # Konversi semua kolom 'tahun' jadi angka aman (tanpa error)
                for col in df.columns:
                    if "tahun" in col.lower():
                        df[col] = pd.to_numeric(df[col], errors="coerce")  # ubah ke angka, yang aneh jadi NaN

                data[file] = df
            except Exception as e:
                st.warning(f"Gagal memuat {file}: {e}")
    return data


data_dict = load_csv_files(DATA_FOLDER)
file_list = list(data_dict.keys())

# ---------------------
# Sidebar: Pilih Data
# ---------------------
st.sidebar.title("📁 Sumber Data")
data_source = st.sidebar.radio("Pilih sumber data:", ["Gunakan Data Bawaan", "Unggah File Sendiri"])

if data_source == "Unggah File Sendiri":
    uploaded_file = st.sidebar.file_uploader("Unggah file CSV atau Excel", type=["csv", "xlsx"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
        selected_file = uploaded_file.name
    else:
        st.stop()
else:
    selected_file = st.sidebar.selectbox("Pilih file dari data bawaan:", file_list)
    df = data_dict[selected_file]

# ---------------------
# Tampilkan Dataset & Statistik Ringkas
# ---------------------
st.subheader(f"Dataset: {selected_file}")
st.dataframe(df.head(), use_container_width=True)

with st.expander("Statistik Ringkasan Dataset"):
    st.write(df.describe(include='all').transpose())

# ---------------------
# Filter Dinamis
# ---------------------
st.sidebar.markdown("### Filter Data")
filterable_cols = ["tahun", "kecamatan", "kabupaten", "provinsi", "jenis kelamin", "kelompok umur", "agama"]
filtered_df = df.copy()
for col in df.columns:
    if col.lower() in filterable_cols and df[col].nunique() <= 30:
        options = st.sidebar.multiselect(f"{col.title()} yang ditampilkan", sorted(df[col].dropna().unique()), default=sorted(df[col].dropna().unique()))
        filtered_df = filtered_df[filtered_df[col].isin(options)]

if filtered_df.empty:
    st.warning("Data kosong setelah filter.")
    st.stop()

# ---------------------
# Fungsi: Ambil data berdasarkan indikator
# ---------------------
def get_df_by_indikator(indikator, data_dict):
    for key in data_dict:
        if indikator.lower() in key.lower():
            return data_dict[key], key
    return None, None

# ---------------------
# Ringkasan Beberapa Indikator Terpilih
# ---------------------
st.sidebar.markdown("### Pilih Topik untuk Ringkasan")
topik_ringkasan = st.sidebar.multiselect(
    "Pilih indikator untuk ditampilkan di Ringkasan:",
    options=["IPM", "TPAK", "AHH", "Kemiskinan", "Melek Huruf", "Penduduk", "Fasilitas"],
    default=["IPM", "AHH"],
    key="ringkasan_multiselect"
)

if topik_ringkasan:
    st.subheader("📌 Ringkasan Beberapa Indikator Terpilih")
    cols = st.columns(2)
    count = 0
    for indikator in topik_ringkasan:
        file_candidates = [key for key in data_dict if indikator.lower() in key.lower()]
        if file_candidates:
            ringkasan_df = data_dict[file_candidates[0]]
            tahun_col = next((col for col in ringkasan_df.columns if "tahun" in col.lower()), None)
            y_col = ringkasan_df.columns[-1]
            if tahun_col:
                if indikator in ["IPM", "AHH"]:
                    fig = px.line(ringkasan_df, x=tahun_col, y=y_col, markers=True,
                                title=f"Tren {indikator}", template="plotly_white")
                elif indikator == "TPAK":
                    fig = px.bar(ringkasan_df, x=tahun_col, y=y_col,
                                title=f"Distribusi {indikator}", template="plotly_white")
                elif indikator == "Kemiskinan":
                    fig = px.bar(ringkasan_df, x=tahun_col, y=y_col,
                                title=f"Tingkat {indikator}", template="plotly_white")
                elif indikator == "Melek Huruf":
                    fig = px.area(ringkasan_df, x=tahun_col, y=y_col,
                                title=f"Tingkat {indikator}", template="plotly_white")
                elif indikator == "Penduduk":
                    fig = px.pie(ringkasan_df, names=tahun_col, values=y_col,
                                title=f"Distribusi {indikator}", template="plotly_white")
                else:
                    fig = px.line(ringkasan_df, x=tahun_col, y=y_col, title=f"{indikator}", template="plotly_white")

                cols[count % 2].plotly_chart(fig, use_container_width=True)
                count += 1
            else:
                st.warning(f"Tidak ditemukan kolom tahun di dataset {file_candidates[0]}")
        else:
            st.warning(f"Tidak ditemukan dataset untuk indikator {indikator}")

# ---------------------
# Visualisasi Interaktif
# ---------------------
st.markdown("### 📊 Visualisasi Interaktif")
chart_type = st.selectbox("Pilih Jenis Grafik", [
    "Line Chart", "Bar Chart", "Area Chart", "Scatter Plot", "Pie Chart", 
    "Histogram", "Box Plot", "3D Scatter Plot"])

numeric_cols = [col for col in filtered_df.columns if pd.api.types.is_numeric_dtype(filtered_df[col])]
category_cols = [col for col in filtered_df.columns if filtered_df[col].dtype == "object" or "tahun" in col.lower()]

x_axis = st.selectbox("Kolom X", category_cols)
y_axis = st.selectbox("Kolom Y", numeric_cols)

if x_axis.lower() == "tahun":
    filtered_df[x_axis] = pd.to_numeric(filtered_df[x_axis], errors="coerce")
    filtered_df[x_axis] = filtered_df[x_axis].dropna().astype(int)

if chart_type == "Line Chart":
    fig = px.line(filtered_df, x=filtered_df[x_axis].astype(str), y=y_axis, text= y_axis, markers=True, template="plotly_white")
elif chart_type == "Bar Chart":
    fig = px.bar(filtered_df, x=x_axis, y=y_axis, text=y_axis, template="plotly_white")
elif chart_type == "Area Chart":
    fig = px.area(filtered_df, x=x_axis, y=y_axis, text=y_axis, template="plotly_white")
elif chart_type == "Scatter Plot":
    fig = px.scatter(filtered_df, x=x_axis, y=y_axis, template="plotly_white")
elif chart_type == "Pie Chart":
    pie_df = filtered_df.groupby(x_axis)[y_axis].sum().reset_index()
    fig = px.pie(pie_df, names=x_axis, values=y_axis, template="plotly_white")
elif chart_type == "Histogram":
    fig = px.histogram(filtered_df, x=x_axis, y=y_axis, text_auto= True, template="plotly_white")
elif chart_type == "Box Plot":
    fig = px.box(filtered_df, x=x_axis, y=y_axis, template="plotly_white")
elif chart_type == "3D Scatter Plot":
    z_axis = st.selectbox("Kolom Z", numeric_cols)
    fig = px.scatter_3d(filtered_df, x=x_axis, y=y_axis, z=z_axis, color=x_axis, template="plotly_dark")

st.plotly_chart(fig, use_container_width=True)

# ---------------------
# Penjelasan Grafik Otomatis
# ---------------------
def generate_explanation(file_name, x, y):
    file_name = file_name.lower()
    x = x.lower()
    y = y.lower()
    if "ipm" in file_name:
        return f"Grafik menunjukkan tren **IPM** berdasarkan {x}. Nilai {y} mencerminkan pembangunan manusia."
    elif "tpak" in file_name:
        return f"Grafik menunjukkan **TPAK** berdasarkan {x}, merefleksikan partisipasi angkatan kerja."
    elif "ahh" in file_name:
        return f"Visualisasi **AHH** menunjukkan harapan hidup berdasarkan {x}."
    elif "kemiskinan" in file_name:
        return f"Grafik menampilkan tingkat kemiskinan berdasarkan {x} dengan nilai {y}."
    elif "melek" in file_name:
        return f"Grafik ini menampilkan **tingkat melek huruf** menurut {x}."
    elif "penduduk" in file_name:
        return f"Visualisasi distribusi jumlah penduduk berdasarkan {x} dengan nilai {y}."
    else:
        return f"Grafik menampilkan hubungan antara {x} dan {y}."

st.markdown("### 📝 Penjelasan Grafik Otomatis")
explanation = generate_explanation(selected_file, x_axis, y_axis)
st.info(explanation)

# ---------------------
# Unduh Data
# ---------------------
st.markdown("### 💾 Unduh Data")
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Unduh Data CSV", csv, f"filtered_{selected_file}", "text/csv")
