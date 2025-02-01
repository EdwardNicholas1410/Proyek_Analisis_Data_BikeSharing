# Import semua library data analysis dan visualisasi dan pembuatan dashboard
import pandas as pd # data analisis
import matplotlib.pyplot as plt # visualisasi
import seaborn as sns # visualisasi
import streamlit as st # pembuatan dashboard

sns.set(style='dark')

# Fungsi fungsi persiapan dataframe
def create_byseason_df(df):
    byseason_df = df.groupby(by='season').agg({
    'total': 'sum',
    }).reset_index()

    return byseason_df

def create_byweather_situation_df(df):
    byweather_situation_df = df.groupby(by='weather_situation').agg({
    'total': 'sum',
    }).reset_index()

    return byweather_situation_df

def create_byworkingday_mean_df(df):
    byworkingday_mean_df = df.groupby(by='workingday').agg({
    'casual': 'mean',
    'registered': 'mean',
    'total': 'mean',
    }).reset_index()

    byworkingday_mean_df = byworkingday_mean_df.melt(id_vars=['workingday'], var_name='kategori')

    return byworkingday_mean_df

def create_byworkingday_sum_df(df):
    byworkingday_sum_df = df.groupby(by='workingday').agg({
    'casual': 'sum',
    'registered': 'sum',
    'total': 'sum',
    }).reset_index()

    byworkingday_sum_df = byworkingday_sum_df.melt(id_vars=['workingday'], var_name='kategori')

    return byworkingday_sum_df

def create_byhourtime_cluster_df(df):
    byhourtime_cluster_df = df.groupby(by='hourtime_cluster').agg({
    'total': 'sum'
    }).reset_index()

    return byhourtime_cluster_df

# Ubah dataset yang sudah di cleaning menjadi dataframe
daily_df = pd.read_csv('dashboard/cleaned_day.csv')
hourly_df = pd.read_csv('dashboard/cleaned_hour.csv')

# Konversi tipe data supaya bisa dipakai di filter
daily_df['date'] = pd.to_datetime(daily_df['date'])
hourly_df['date'] = pd.to_datetime(hourly_df['date'])

# Sidebar untuk menampung filter berdasarkan tanggal
with st.sidebar:

    # Buat variabel menampung tanggal paling kecil dan paling besar di dalam masing masing (daily dan hourly) dataframe
    min_date = daily_df['date'].min()
    max_date = daily_df['date'].max()

    min_hour = hourly_df['hour'].min()
    max_hour = hourly_df['hour'].max()

    # Judul sidebar
    st.header('Sidebar Dashboard Bike Sharing')

    # Filter menurut tanggal
    st.subheader('Filter Tanggal')
    start_date, end_date = st.date_input(
        label='Tanggal',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date],
    )
    # Konversi tipe data supaya bisa dipakai filter
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    # Filter menurut jam
    st.subheader('Filter Jam')
    start_hour, end_hour = st.slider(
        label='Jam',
        min_value=min_hour,
        max_value=max_hour,
        value=[min_hour, max_hour]
    )

# Eksekusi hasil filter
daily_main_df = daily_df[(daily_df['date'] >= start_date) & (daily_df['date'] <= end_date)]
hourly_main_df = hourly_df[(hourly_df['date'] >= start_date) & (hourly_df['date'] <= end_date)]
hourly_main_df = hourly_main_df[(hourly_main_df['hour'] >= start_hour) & (hourly_main_df['hour'] <= end_hour)]

# Eksekusi fungsi persiapan frame
# Di lakukan setelah mengeksekusi hasil filter supaya nilai data sesuai
byseason_df = create_byseason_df(hourly_main_df)
byweather_situation_df = create_byweather_situation_df(hourly_main_df)
byworkingday_mean_df = create_byworkingday_mean_df(daily_main_df)
byworkingday_sum_df = create_byworkingday_sum_df(daily_main_df)
byhourtime_cluster_df = create_byhourtime_cluster_df(hourly_main_df)

# Dashboard
st.header('Dashboard Bike Sharing') # Judul dashboard

st.subheader('Total Penyewaan Menurut Kondisi Lingkungan') # Judul visualisasi pertanyaan no 1

col1, col2 = st.columns(2)

with col1:
    # Visualisasi chart total penyewaan berdasarkan musim
    fig, ax = plt.subplots(figsize=(20,20))
    colors = ['blue', 'grey', 'grey', 'grey']
    sns.barplot(
        x='season',
        y='total',
        data=byseason_df,
        palette=colors,
        hue='season',
        legend=False,
        ax=ax,
        order=['spring','summer','fall','winter'],
    )
    ax.set_title('Jumlah Penyewaan Sepeda Berdasarkan Musim', fontsize=45)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='y', labelsize=35)
    ax.tick_params(axis='x', labelsize=35)
    ax.ticklabel_format(style='plain', axis='y')

    st.pyplot(fig)

with col2:
    # Visualisasi chart total penyewaan berdasarkan cuaca
    fig, ax = plt.subplots(figsize=(20,20))
    colors = ['blue', 'grey', 'grey', 'grey']
    sns.barplot(
        x='weather_situation',
        y='total',
        data=byweather_situation_df,
        palette=colors,
        hue='weather_situation',
        legend=False,
        ax=ax,
        order=['clear','cloudy/mist','light rain/snow','heavy rain/ice'],
    )
    ax.set_title('Jumlah Penyewaan Sepeda Berdasarkan Kondisi Cuaca', fontsize=45)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='y', labelsize=35)
    ax.tick_params(axis='x', labelsize=35)
    ax.ticklabel_format(style='plain', axis='y')

    st.pyplot(fig)

st.subheader('Perbandingan Penyewaan di Hari Libur vs Hari Kerja') # Judul visualisasi pertanyaan no 2

# Visualisasi chart perbandingan rata rata penyewaan hari libur dan hari kerja
fig, ax = plt.subplots(figsize=(16,8))
colors = ['red', 'blue', 'green']
sns.barplot(
    x='workingday',
    y='value',
    data=byworkingday_mean_df,
    palette=colors,
    hue='kategori',
    legend=True,
    ax=ax,
)
ax.set_title('Rata-Rata Penyewaan Sepeda per Hari oleh Pengguna (Hari Kerja vs. Libur)', fontsize=20)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=15)
ax.tick_params(axis='x', labelsize=15)
ax.ticklabel_format(style='plain', axis='y')
ax.set_xticks([0,1], labels=['Hari Libur', 'Hari Kerja'])

st.pyplot(fig)

# Visualisasi chart perbandingan total penyewaan hari libur dan hari kerja
fig, ax = plt.subplots(figsize=(16,8))
colors = ['red', 'blue', 'green']
sns.barplot(
    x='workingday',
    y='value',
    data=byworkingday_sum_df,
    palette=colors,
    hue='kategori',
    legend=True,
    ax=ax,
)
ax.set_title('Total Penyewaan Sepeda oleh Pengguna (Hari Kerja vs. Libur)', fontsize=20)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=15)
ax.tick_params(axis='x', labelsize=15)
ax.ticklabel_format(style='plain', axis='y')
ax.set_xticks([0,1], labels=['Hari Libur', 'Hari Kerja'])

st.pyplot(fig)

st.subheader('Total Penyewaan Berdasarkan Clustering Waktu') # Judul visualisasi pertanyaan no 3
# Visualisasi chart hasil clustering waktu
fig, ax = plt.subplots(figsize=(16,8))
colors = ['grey', 'blue', 'grey', 'grey']
sns.barplot(
    x='hourtime_cluster',
    y='total',
    data=byhourtime_cluster_df,
    palette=colors,
    hue='hourtime_cluster',
    legend=False,
    ax=ax,
    order=['morning','afternoon','evening','night'],
)
ax.set_title('Jumlah Penyewaan Sepeda Berdasarkan Waktu', fontsize=18)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=12)
ax.ticklabel_format(style='plain', axis='y')

st.pyplot(fig)