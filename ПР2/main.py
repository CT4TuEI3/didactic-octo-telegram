import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Практическая работа №2
# Построить графики следующего вида:
# 1) построение обычного графика
# 2) работа с оформлением и стилями
# 3) оценка плотности
# 4) box plot
# 5) violin plot
# 6) pairGrid
# 7) heatmap
# 8) clustermap
# 9) jointplot

# Загружаем данные
df = pd.read_csv("universal_top_spotify_songs.csv")
dat_filtered = df[df["snapshot_date"] == "2025-06-11"]

#1. Обычный график зависимости popularity от danceability
plt.figure()
sns.lineplot(x="danceability", y="popularity", data=dat_filtered)
plt.title("График зависимости popularity от danceability")
plt.xlabel("danceability")
plt.ylabel("popularity")
plt.show()

#2. Работа с оформлением и стилями
plt.figure()
sns.set_theme(style="whitegrid") # стиль whitegrid
sns.scatterplot(x="tempo", y="energy", data=dat_filtered)
plt.title("Зависимость energy от tempo (whitegrid)")
plt.xlabel("tempo")
plt.ylabel("energy")
plt.show()

plt.figure()
sns.set_theme(style="darkgrid") # стиль darkgrid
sns.scatterplot(x="tempo", y="energy", data=dat_filtered)
plt.title("Зависимость energy от tempo (darkgrid)")
plt.xlabel("tempo")
plt.ylabel("energy")
plt.show()

#3. Оценка плотности распределения danceability
plt.figure()
sns.kdeplot(x="danceability", data=dat_filtered, fill=True)
plt.title("Оценка плотности danceability")
plt.xlabel("danceability")
plt.ylabel("Плотность")
plt.show()

#4. Box plot - распределение tempo
plt.figure()
sns.boxplot(y="tempo", data=dat_filtered)
plt.title("Box plot для tempo")
plt.ylabel("tempo")
plt.show()

#5. Violin plot — распределение loudness
plt.figure()
sns.violinplot(y="loudness", data=dat_filtered)
plt.title("Violin plot для loudness")
plt.ylabel("loudness")
plt.show()

#6. PairGrid - попарные зависимости нескольких переменных
g = sns.PairGrid(dat_filtered[["popularity", "danceability", "tempo", "energy"]])
g.map_diag(sns.kdeplot, fill=True)
g.map_offdiag(sns.scatterplot)
g.fig.suptitle("PairGrid: попарные зависимости между переменными", y=1.02)
plt.show()

#7. Heatmap - корреляция между числовыми признаками
plt.figure()
corr = dat_filtered[["popularity",
                     "danceability",
                     "tempo",
                     "energy",
                     "loudness",
                     "speechiness",
                     "duration_ms",
                     "daily_rank"]].corr()
sns.heatmap(corr, annot=True, cmap="RdBu", vmin=-1, vmax=1)
plt.title("Тепловая карта корреляций между числовыми признаками")
plt.show()

#8. Clustermap - кластеризация по корреляционной матрице
sns.clustermap(corr, cmap="coolwarm", annot=True)
plt.suptitle("Clustermap: кластеризация корреляций")
plt.show()

#9. Jointplot - взаимосвязь между loudness и energy
sns.jointplot(x="loudness", y="energy", data=dat_filtered, kind="scatter", color="purple")
plt.suptitle("Jointplot: взаимосвязь loudness и energy")
plt.show()
