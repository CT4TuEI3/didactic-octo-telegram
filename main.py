import pandas as pd
import matplotlib.pyplot as plt

# Указать путь к CSV файлу
df = pd.read_csv('События-2025-09-02-2025-09-09.csv')

# Гипотеза:
# Существует положительная корреляция между временем суток (как количественной переменной)
# и уровнем активности пользователей в приложении

print("Первые 5 строк данных:")
print(df.head())
print(f"Всего записей: {len(df)}")

# Преобразуем период в datetime (берем начало каждого часового интервала)
df['Период'] = df['Период'].str.split(' - ').str[0]  # Берем начало периода
df['datetime'] = pd.to_datetime(df['Период'], format='%Y-%m-%d %H:%M:%S')

# Сортируем по времени для правильного отображения на графике
df = df.sort_values('datetime')

# Функция для определения времени суток
def get_time_period(hour):
    if 8 <= hour < 16:  # Первая половина дня: с 8:00 до 16:00
        return 'first_half'
    elif 16 <= hour < 24:  # Вторая половина дня: с 16:00 до 00:00
        return 'second_half'
    else:  # Ночь: с 00:00 до 8:00
        return 'night'

# Добавляем колонку с периодом дня
df['hour'] = df['datetime'].dt.hour
df['time_period'] = df['hour'].apply(get_time_period)

# Создаем график
plt.figure(figsize=(15, 8))

# График событий vpn_connected
plt.plot(df['datetime'], df['vpn_connected'], 
         marker='o', markersize=3, linewidth=2, color='blue', alpha=0.7)

# Настройка оформления
plt.title('Количество подключений VPN по часам\n(период: 2-9 сентября 2025)', fontsize=16, fontweight='bold')
plt.xlabel('Дата и время', fontsize=12)
plt.ylabel('Количество подключений VPN', fontsize=12)
plt.grid(True, alpha=0.3)

# Форматирование оси времени
import matplotlib.dates as mdates
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d.%m %H:%M'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
plt.gcf().autofmt_xdate()  # Наклон подписей дат

# Добавляем среднюю линию
mean_value = df['vpn_connected'].mean()
plt.axhline(y=mean_value, color='red', linestyle='--', alpha=0.8, 
            label=f'Среднее: {mean_value:.0f} подключений/час')

# Выделяем периоды дня разными цветами фона
for i in range(len(df)):
    hour = df['datetime'].iloc[i].hour
    if 8 <= hour < 16:  # Первая половина дня
        plt.axvspan(df['datetime'].iloc[i], df['datetime'].iloc[i] + pd.Timedelta(hours=1), 
                   alpha=0.1, color='lightgreen')
    elif 16 <= hour < 24:  # Вторая половина дня
        plt.axvspan(df['datetime'].iloc[i], df['datetime'].iloc[i] + pd.Timedelta(hours=1), 
                   alpha=0.1, color='lightcoral')

# Показываем статистику
print("\nСтатистика по VPN подключениям:")
print(f"Общее количество подключений: {df['vpn_connected'].sum():,}")
print(f"Среднее в час: {mean_value:.0f}")
print(f"Максимальное в час: {df['vpn_connected'].max()}")
print(f"Минимальное в час: {df['vpn_connected'].min()}")
print(f"Медиана: {df['vpn_connected'].median()}")

# Статистика по периодам дня
period_stats = df.groupby('time_period')['vpn_connected'].agg(['mean', 'std', 'count', 'sum'])
print("\nСтатистика по периодам дня:")
print(period_stats)

plt.show()

# Дополнительный график: распределение по часам суток
plt.figure(figsize=(14, 6))

# Группируем по часам
hourly_stats = df.groupby(df['datetime'].dt.hour)['vpn_connected'].agg(['mean', 'std'])

plt.bar(hourly_stats.index, hourly_stats['mean'], 
        yerr=hourly_stats['std'], alpha=0.7, capsize=5, color='lightblue')

plt.title('Среднее количество подключений VPN по часам суток', fontsize=14)
plt.xlabel('Час дня', fontsize=12)
plt.ylabel('Среднее количество подключений', fontsize=12)
plt.xticks(range(0, 24))
plt.grid(True, alpha=0.3)

# Выделяем новые периоды дня
plt.axvspan(8, 15.9, alpha=0.2, color='lightgreen', label='Первая половина дня (8:00-16:00)')
plt.axvspan(16, 23.9, alpha=0.2, color='lightcoral', label='Вторая половина дня (16:00-00:00)')
plt.axvspan(0, 7.9, alpha=0.2, color='lightgray', label='Ночь (00:00-8:00)')

plt.legend()
plt.tight_layout()
plt.show()

# Сравнение первой и второй половины дня
first_half = df[df['time_period'] == 'first_half']['vpn_connected']
second_half = df[df['time_period'] == 'second_half']['vpn_connected']

print(f"\nСравнение половин дня:")
print(f"Первая половина (8:00-16:00): {first_half.mean():.1f} ± {first_half.std():.1f} подключений/час")
print(f"Вторая половина (16:00-00:00): {second_half.mean():.1f} ± {second_half.std():.1f} подключений/час")
print(f"Разница: {second_half.mean() - first_half.mean():.1f} подключений/час")
