import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

dat = pd.read_csv("universal_top_spotify_songs.csv")

#Гипотеза: popularity песни положительно коррелирует с danceability.

print(f"Всего записей: {len(dat)}")

parms = ["name",
         "snapshot_date",
         "popularity",
         "danceability",
         "tempo",
         "energy"]

dat = dat[parms]

print(dat.head(3))

dat_filtered = dat[dat["snapshot_date"] == "2025-06-11"]

plt.figure(figsize=(15, 8))

# График популярности
plt.plot(dat_filtered.index,
         dat_filtered["popularity"])

plt.plot(dat_filtered.index, 
         dat_filtered["popularity"].rolling(30).mean(),
         color= "red")

plt.show()

corr = dat[["popularity",
            "danceability",
            "tempo",
            "energy"]].corr()
plt.imshow(corr,
           cmap= "seismic",
           vmin= -1,
           vmax= 1)

plt.colorbar()

plt.xticks(range(len(corr.columns)), corr.columns)
plt.yticks(range(len(corr.columns)), corr.columns)

plt.show()
