import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from matplotlib.ticker import FuncFormatter

sns.set(style='dark')

# Menyiapkan data day_df
day_df = pd.read_csv("./main_data.csv")

# Menyiapkan daily_rent_df

def create_daily_rent_df(df):
    daily_rent_df = df.groupby(by='dateday').agg({
        'count': 'sum'
    }).reset_index()
    return daily_rent_df

# Menyiapkan daily_casual_rent_df

def create_daily_casual_rent_df(df):
    daily_casual_rent_df = df.groupby(by='dateday').agg({
        'casual': 'sum'
    }).reset_index()
    return daily_casual_rent_df

# Menyiapkan daily_registered_rent_df

def create_daily_registered_rent_df(df):
    daily_registered_rent_df = df.groupby(by='dateday').agg({
        'registered': 'sum'
    }).reset_index()
    return daily_registered_rent_df

# Menyiapkan season_rent_df

def create_season_rent_df(df):
    season_rent_df = df.groupby(by='season')[
        ['registered', 'casual']].sum().reset_index()
    return season_rent_df

# Menyiapkan monthly_rent_df

def create_monthly_rent_df(df):
    monthly_rent_df = df.groupby(by='month').agg({
        'count': 'sum'
    }).reset_index()
    ordered_months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    monthly_rent_df['month'] = pd.Categorical(
        monthly_rent_df['month'], categories=ordered_months, ordered=True)
    monthly_rent_df = monthly_rent_df.sort_values('month')
    return monthly_rent_df

# Menyiapkan weekday_rent_df

def create_weekday_rent_df(df):
    weekday_rent_df = df.groupby(by='weekday').agg({
        'count': 'sum'
    }).reset_index()
    return weekday_rent_df

# Menyiapkan workingday_rent_df

def create_workingday_rent_df(df):
    workingday_rent_df = df.groupby(by='workingday').agg({
        'count': 'sum'
    }).reset_index()
    return workingday_rent_df

# Menyiapkan holiday_rent_df

def create_holiday_rent_df(df):
    holiday_rent_df = df.groupby(by='holiday').agg({
        'count': 'sum'
    }).reset_index()
    return holiday_rent_df

# Menyiapkan weather_rent_df

def create_weather_rent_df(df):
    weather_rent_df = df.groupby(by='weather_cond').agg({
        'count': 'sum'
    }).reset_index()
    return weather_rent_df


# Membuat komponen filter
min_date = pd.to_datetime(day_df['dateday']).dt.date.min()
max_date = pd.to_datetime(day_df['dateday']).dt.date.max()

with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df['dateday'] >= str(start_date)) &
                 (day_df['dateday'] <= str(end_date))]

# Menyiapkan berbagai dataframe
daily_rent_df = create_daily_rent_df(main_df)
daily_casual_rent_df = create_daily_casual_rent_df(main_df)
daily_registered_rent_df = create_daily_registered_rent_df(main_df)
season_rent_df = create_season_rent_df(main_df)
monthly_rent_df = create_monthly_rent_df(main_df)
weekday_rent_df = create_weekday_rent_df(main_df)
workingday_rent_df = create_workingday_rent_df(main_df)
holiday_rent_df = create_holiday_rent_df(main_df)
weather_rent_df = create_weather_rent_df(main_df)
print(daily_rent_df)
print(daily_casual_rent_df)
print(daily_registered_rent_df)
print(season_rent_df)
print(monthly_rent_df)
print(weekday_rent_df)
print(workingday_rent_df)
print(holiday_rent_df)
print(weather_rent_df)


# Membuat Dashboard secara lengkap
st.header('Bike Rental Dashboard 🚲')

# Membuat jumlah penyewaan harian
st.subheader('Daily Rentals')
col1, col2, col3 = st.columns(3)

with col1:
    daily_rent_casual = daily_casual_rent_df['casual'].sum()
    st.metric('Casual User', value=daily_rent_casual)

with col2:
    daily_rent_registered = daily_registered_rent_df['registered'].sum()
    st.metric('Registered User', value=daily_rent_registered)

with col3:
    daily_rent_total = daily_rent_df['count'].sum()
    st.metric('Total User', value=daily_rent_total)


# Peran cuaca dalam mempengaruhi jumlah peminjaman sepeda
st.subheader('Jumlah Pengguna Sepeda berdasarkan Cuaca')

def y_format(y, _):
    return '{:,.0f}'.format(y).replace(',', '.')

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    x='weather_cond',
    y='count',
    data=weather_rent_df,
    ax=ax,
)
ax.set_title('Jumlah Pengguna Sepeda berdasarkan Cuaca')
ax.set_xlabel('Kondisi Cuaca')
ax.set_ylabel('Jumlah Pengguna Sepeda')
ax.yaxis.set_major_formatter(FuncFormatter(y_format))

st.pyplot(fig)

# Pola penggunaan sepeda berdasarkan musim?
st.subheader('Jumlah Penyewaan Sepeda berdasarkan Musim')

def y_format(y, _):
    return '{:,.0f}'.format(y).replace(',', '.')

seasonal_usage = season_rent_df
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(seasonal_usage['season'], seasonal_usage['casual'],
       label='Casual', color='tab:green')
ax.bar(seasonal_usage['season'], seasonal_usage['registered'],
       label='Registered', bottom=seasonal_usage['casual'], color='tab:blue')
ax.set_title('Jumlah Penyewaan Sepeda berdasarkan Musim')
ax.legend()
ax.yaxis.set_major_formatter(FuncFormatter(y_format))

st.pyplot(fig)

# Tren penggunaan sepeda dalam 12 bulan berdasarkan casual dan registered user
st.subheader('Jumlah Total Sepeda yang Disewakan berdasarkan Bulan dan Tipe Pengguna')

# Define the correct order of months
ordered_months = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
]

# Apply the correct order to the month column
day_df['month'] = pd.Categorical(day_df['month'], categories=ordered_months, ordered=True)

# Group by month and user type
monthly_counts_casual = day_df.groupby(by=["month"], observed=True).agg({"casual": "sum"}).reset_index()
monthly_counts_registered = day_df.groupby(by=["month"], observed=True).agg({"registered": "sum"}).reset_index()

# Add user type columns
monthly_counts_casual['user_type'] = 'Casual'
monthly_counts_registered['user_type'] = 'Registered'

# Rename columns for concatenation
monthly_counts_casual = monthly_counts_casual.rename(columns={"casual": "count"})
monthly_counts_registered = monthly_counts_registered.rename(columns={"registered": "count"})

# Concatenate the two DataFrames
monthly_counts = pd.concat([monthly_counts_casual, monthly_counts_registered])

# Plot the data
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=monthly_counts, x="month", y="count", hue="user_type", palette="rocket", marker="o", ax=ax)
ax.set_title("Jumlah Total Sepeda yang Disewakan berdasarkan Bulan dan Tipe Pengguna")
ax.legend(title="Tipe Pengguna", loc="upper right")
st.pyplot(fig)

# Kondisi penggunaan sepeda pada hari libur dibandingkan dengan holiday, hari kerja dan akhir pekan?
st.subheader(
    'Jumlah Pengguna Sepeda berdasarkan Hari Kerja, Libur, dan Akhir Pekan')
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(15, 10))

# Berdasarkan workingday
sns.barplot(x='workingday', y='count', data=workingday_rent_df, ax=axes[0])
axes[0].set_title('Jumlah Pengguna Sepeda berdasarkan Hari Kerja')
axes[0].set_xlabel('Hari Kerja')
axes[0].set_ylabel('Jumlah Pengguna Sepeda')

# Berdasarkan holiday
sns.barplot(x='holiday', y='count', data=holiday_rent_df, ax=axes[1])
axes[1].set_title('Jumlah Pengguna Sepeda berdasarkan Hari Libur')
axes[1].set_xlabel('Hari Libur')
axes[1].set_ylabel('Jumlah Pengguna Sepeda')

# Berdasarkan weekday
sns.barplot(x='weekday', y='count', data=weekday_rent_df, ax=axes[2])
axes[2].set_title('Jumlah Pengguna Sepeda berdasarkan Hari dalam Seminggu')
axes[2].set_xlabel('Hari dalam Seminggu')
axes[2].set_ylabel('Jumlah Pengguna Sepeda')

plt.tight_layout()
st.pyplot(fig)

# Tren penggunaan sepeda dalam setahun dari tahun 2011 - 2012
st.subheader('Jumlah Total Sepeda yang Disewakan berdasarkan Bulan dan Tahun')
monthly_counts = day_df.groupby(by=["month", "year"], observed=True).agg({
    "count": "sum"}).reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=monthly_counts, x="month", y="count",
             hue="year", palette="rocket", marker="o", ax=ax)
ax.set_title("Jumlah Total Sepeda yang Disewakan berdasarkan Bulan dan Tahun")
ax.legend(title="Tahun", loc="upper right")
st.pyplot(fig)

# Variabel temp dan atemp dapat mempengaruhi jumlah total penggunaan sepeda?
st.subheader(
    'Pengaruh Temperature dan Feels Like Temperature terhadap Jumlah Pengguna Sepeda')
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(14, 6))

# Scatter plot untuk 'temp' vs 'count'
sns.scatterplot(x='temp', y='count', data=day_df, alpha=0.5, ax=axes[0])
axes[0].set_title('Temperature vs Count')

# Scatter plot untuk 'atemp' vs 'count'
sns.scatterplot(x='atemp', y='count', data=day_df, alpha=0.5, ax=axes[1])
axes[1].set_title('Feels Like Temperature vs Count')

st.pyplot(fig)

# Faktor-faktor yang paling mempengaruhi jumlah total peminjaman sepeda?
st.subheader('Hubungan Antar Variabel terhadap Jumlah Total Peminjaman Sepeda')
fig = sns.pairplot(
    day_df, vars=['count', 'season', 'weekday', 'weather_cond', 'holiday'])
fig.fig.suptitle('Pair Plot Hubungan Antar Variabel', y=1.02)
st.pyplot(fig)

st.caption('Submission Sebastian Luth Hasibuan untuk Belajar Analisis Data dengan Python')