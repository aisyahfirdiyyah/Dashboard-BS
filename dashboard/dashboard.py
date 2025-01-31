import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df_day = pd.read_csv("dashboard/day.csv")
df_hour = pd.read_csv("dashboard/hour.csv")

# Convert date columns to datetime format
df_day['dteday'] = pd.to_datetime(df_day['dteday'])
df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])

sns.set(style='dark')

# Function to create daily bike usage summary
def create_daily_orders_df(df_hour):
    daily_orders_df = df_hour.resample(rule='D', on='dteday').agg({"cnt": "sum"}).reset_index()
    daily_orders_df.rename(columns={"cnt": "total_bike_usage"}, inplace=True)
    return daily_orders_df

# Function to create hourly bike usage summary
def create_hourly_orders_df(df_hour):
    hourly_orders_df = df_hour.groupby("hr").agg({"cnt": "sum"}).reset_index()
    hourly_orders_df.rename(columns={"cnt": "total_bike_usage"}, inplace=True)
    return hourly_orders_df

# Function to analyze bike usage by weather condition
def create_by_weather_df(df_day):
    byweather_df = df_day.groupby("weathersit").agg({"cnt": "sum"}).reset_index()
    byweather_df.rename(columns={"cnt": "total_bike_usage"}, inplace=True)
    return byweather_df

# Function to analyze bike usage by day of the week
def create_by_day_of_week_df(df_day):
    bydayofweek_df = df_day.groupby("weekday").agg({"cnt": "sum"}).reset_index()
    bydayofweek_df.rename(columns={"cnt": "total_bike_usage"}, inplace=True)
    return bydayofweek_df

# Dashboard Title
st.header("Bike Sharing Dashboard 🚴‍♂️")

# Section: Bike usage by weather
st.subheader("Pengaruh Cuaca terhadap Jumlah Pengguna Sepeda")
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=df_day, x='weathersit', y='cnt')
plt.title('Penyewaan Sepeda Berdasarkan Cuaca')
plt.xlabel('Kondisi Cuaca (1: Cerah, 2: Berawan, 3: Gerimis/Salju, 4: Hujan/Salju Lebat)')
plt.ylabel('Jumlah Sepeda yang Disewa')
st.pyplot(fig)

# Section: Usage pattern by day of the week
st.subheader("Pola Penggunaan Sepeda Berdasarkan Hari dalam Seminggu")
df_hour['day_of_week'] = df_hour['dteday'].dt.dayofweek
usage_by_hour = df_hour.groupby('day_of_week')['cnt'].sum()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=usage_by_hour.index, y=usage_by_hour.values, palette='Blues_d')
plt.xlabel('Hari dalam Seminggu')
plt.ylabel('Jumlah Penggunaan Sepeda')
plt.title('Pola Penggunaan Sepeda Berdasarkan Hari dalam Seminggu')
plt.xticks(ticks=range(7), labels=['Sen', 'Sel', 'Rab', 'Kam', 'Jum', 'Sab', 'Min'])
st.pyplot(fig)

# Additional categorical mappings
season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
df_day['season_label'] = df_day['season'].map(season_map)
df_hour['season_label'] = df_hour['season'].map(season_map)

workingday_map = {0: 'Non-Working Day', 1: 'Working Day'}
df_day['workingday_label'] = df_day['workingday'].map(workingday_map)
df_hour['workingday_label'] = df_hour['workingday'].map(workingday_map)

def time_of_day(hour):
    if 0 <= hour < 6:
        return 'Midnight'
    elif 6 <= hour < 12:
        return 'Morning'
    elif 12 <= hour < 18:
        return 'Afternoon'
    else:
        return 'Evening'

df_hour['time_category'] = df_hour['hr'].apply(time_of_day)

def rental_category(cnt):
    if cnt < 100:
        return 'Low'
    elif 100 <= cnt < 500:
        return 'Medium'
    else:
        return 'High'

df_day['rental_category'] = df_day['cnt'].apply(rental_category)
df_hour['rental_category'] = df_hour['cnt'].apply(rental_category)

# Section: Distribution of bike rentals
st.subheader("Distribusi Penyewaan Berdasarkan Musim, Waktu, Hari Kerja Vs Libur, dan Tren Harian")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

sns.boxplot(ax=axes[0, 0], x="season_label", y="cnt", data=df_day)
axes[0, 0].set_title("Distribusi Penyewaan Sepeda Berdasarkan Musim")
axes[0, 0].set_xlabel("Musim")
axes[0, 0].set_ylabel("Jumlah Penyewaan")

sns.boxplot(ax=axes[0, 1], x="time_category", y="cnt", data=df_hour)
axes[0, 1].set_title("Distribusi Penyewaan Sepeda Berdasarkan Waktu")
axes[0, 1].set_xlabel("Kategori Waktu")
axes[0, 1].set_ylabel("Jumlah Penyewaan")

sns.barplot(ax=axes[1, 0], x="workingday_label", y="cnt", data=df_day)
axes[1, 0].set_title("Jumlah Penyewaan pada Hari Kerja vs Hari Libur")
axes[1, 0].set_xlabel("Kategori Hari")
axes[1, 0].set_ylabel("Jumlah Penyewaan")

axes[1, 1].plot(df_day['dteday'], df_day['cnt'], marker='o', linestyle='-', color='blue')
axes[1, 1].set_title("Tren Penyewaan Sepeda Harian")
axes[1, 1].set_xlabel("Tanggal")
axes[1, 1].set_ylabel("Jumlah Penyewaan")
axes[1, 1].tick_params(axis='x', rotation=45)
axes[1, 1].grid()

plt.tight_layout()
st.pyplot(fig)

# Footer
st.caption('Copyright © Bike Sharing Analysis 2025')
