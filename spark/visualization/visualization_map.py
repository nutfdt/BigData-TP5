import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# Charger le shapefile des pays
world = gpd.read_file("../data/naturalearth_lowres/ne_110m_admin_0_countries.shp")

# Charger les données de suicides
suicide_data = pd.read_csv("../data/uploads/average_suicides_per_100k.csv/average_suicides_per_100k.csv")

# Vérifier les colonnes disponibles pour adapter les noms, si nécessaire
print(suicide_data.columns)

# Normalisation des noms des pays dans le shapefile et les données CSV
world['ADMIN'] = world['ADMIN'].str.strip().str.lower()  # Normalisation des noms dans le shapefile
suicide_data['country'] = suicide_data['country'].str.strip().str.lower()  # Normalisation des noms dans les données CSV

# Afficher les valeurs uniques des colonnes pour mieux comprendre les différences
print("Valeurs uniques dans le shapefile (ADMIN) :")
print(world['ADMIN'].unique())

print("Valeurs uniques dans les données CSV (country) :")
print(suicide_data['country'].unique())

# Dictionnaire pour corriger les correspondances
name_corrections = {
    "united states": "united states of america",
    "republic of korea": "south korea",
    "serbia": "republic of serbia",
    "russian federation": "russia",
    "czech republic": "czechia",
}

# Appliquer les corrections
suicide_data['country'] = suicide_data['country'].replace(name_corrections)

# Fusionner les données sur le nom du pays
world = world.merge(suicide_data, how="left", left_on="ADMIN", right_on="country")

# Vérifier si la fusion a bien fonctionné, afficher les pays sans données
missing_data = world[world['avg_suicides_per_100k'].isna()]
print("Pays sans données après fusion:")
print(missing_data[['ADMIN', 'avg_suicides_per_100k']])

# S'assurer que la projection est correcte (coordonnées géographiques)
world = world.to_crs(epsg=4326)  # Projection WGS84 (latitude/longitude)

# Créer la figure et les axes
fig, ax = plt.subplots(1, 1, figsize=(15, 10))

# Tracer la carte choroplèthe
world.boundary.plot(ax=ax, linewidth=0.5)
world.plot(column='avg_suicides_per_100k', ax=ax, cmap="OrRd", edgecolor="0.8", legend=True,
           legend_kwds={'label': "Moyenne des suicides pour 100k habitants (2010-2016)", 'orientation': "horizontal"})

# Ajuster les limites pour afficher toute la carte
ax.set_xlim(world.bounds['minx'].min(), world.bounds['maxx'].max())
ax.set_ylim(world.bounds['miny'].min(), world.bounds['maxy'].max())

# Personnaliser l'affichage
ax.set_title("Moyenne des suicides pour 100k habitants (2010-2016) par pays", fontsize=15)
ax.set_axis_off()

# Enregistrer la carte en tant que fichier PNG
plt.savefig("suicide_map.png", format="png", bbox_inches="tight", dpi=300)

# Afficher la carte
plt.show()
