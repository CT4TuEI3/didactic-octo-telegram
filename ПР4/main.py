import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams["font.family"] = "Arial"
plt.rcParams["figure.figsize"] = (10, 6)

url = "https://kamaz.ru/production/serial/"
response = requests.get(url)
response.encoding = "utf-8"

soup = BeautifulSoup(response.text, "html.parser")

# Извлечение всех таблиц с сайта
tables = soup.find_all("table")
dataframes = []

for table in tables:
    headers = [th.text.strip() for th in table.find_all("th")]
    rows = []
    for tr in table.find_all("tr")[1:]:
        cells = [td.text.strip() for td in tr.find_all("td")]
        if cells:
            rows.append(cells)

    if rows and headers:
        df = pd.DataFrame(rows, columns=headers)

        # Удаляем первый столбец (с изображением)
        if df.columns[0] == "" or df[df.columns[0]].isna().all() or df[df.columns[0]].eq("").all():
            df.drop(df.columns[0], axis=1, inplace=True)

        dataframes.append(df)

# Объединение всех таблиц в один DataFrame
kamaz_df = pd.concat(dataframes, ignore_index=True)
print("Объединённый DataFrame:")
print(kamaz_df.head())

# Приведение типов данных
text_columns = ["Модель", "Колесная формула", "Тип кабины"]

kamaz_clean = kamaz_df.copy()

for col in kamaz_clean.columns:
    if col not in text_columns:
        kamaz_clean[col] = kamaz_clean[col].str.replace(" ", "", regex=False)
        kamaz_clean[col] = kamaz_clean[col].str.replace(",", ".", regex=False)
        kamaz_clean[col] = kamaz_clean[col].replace("", None)
        kamaz_clean[col] = pd.to_numeric(kamaz_clean[col], errors="ignore")

for int_col in ["Число передач", "База, мм", "Длина, мм"]:
    if int_col in kamaz_clean.columns:
        kamaz_clean[int_col] = pd.to_numeric(kamaz_clean[int_col], errors="coerce").astype("Int64")

kamaz_clean.to_csv("kamaz_models.csv", index=False, encoding="utf-8-sig")
print(kamaz_clean.head())

# Автоматическое определение ключевых колонок
cols = kamaz_clean.columns
power_col = next((c for c in cols if "мощн" in c.lower()), None)
mass_col = next((c for c in cols if "мас" in c.lower()), None)


#1. Barplot — мощность по моделям
plt.figure()
sns.barplot(x="Модель", y=power_col, data=kamaz_clean)
plt.title("Мощность двигателей КАМАЗ по моделям")
plt.xlabel("Модель автомобиля")
plt.ylabel(power_col)
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()


#2. Lineplot — зависимость полной массы от мощности
plt.figure()
sns.lineplot(x=power_col, y=mass_col, data=kamaz_clean, marker="o")
plt.title("Зависимость полной массы от мощности двигателя")
plt.xlabel(power_col)
plt.ylabel(mass_col)
plt.grid(True)
plt.tight_layout()
plt.show()

#3. KDE Plot — распределение мощности
plt.figure()
sns.kdeplot(x=power_col, data=kamaz_clean, fill=True, color="skyblue")
plt.title("Плотность распределения мощности двигателей КАМАЗ")
plt.xlabel(power_col)
plt.ylabel("Плотность вероятности")
plt.grid(True)
plt.tight_layout()
plt.show()

#4. Violin Plot — распределение полной массы
plt.figure()
sns.violinplot(y=mass_col, data=kamaz_clean, color="lightcoral")
plt.title("Распределение полной массы моделей КАМАЗ")
plt.ylabel(mass_col)
plt.grid(True)
plt.tight_layout()
plt.show()

#5. Heatmap — корреляция между числовыми параметрами
numeric_df = kamaz_clean.select_dtypes(include=["float64", "int64"])
corr = numeric_df.corr()

plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap="RdBu", fmt=".2f", vmin=-1, vmax=1)
plt.title("Корреляция числовых параметров модельного ряда КАМАЗ")
plt.tight_layout()
plt.show()

# Выводы:
# 1. Barplot: показывает мощность по моделям (удобное сравнение).
# 2. Lineplot: чем выше мощность, тем больше допустимая масса.
# 3. KDE: распределение мощности близко к нормальному, с пиком около 300–350 л.с.
# 4. Violinplot: большинство моделей имеют массу от 10 до 25 тонн.
# 5. Heatmap: мощность и масса положительно коррелируют.
