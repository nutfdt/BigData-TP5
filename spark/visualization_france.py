import pandas as pd
import matplotlib.pyplot as plt

# Charger les données de suicides
france_data = pd.read_csv("../data/uploads/average_suicides_france.csv/average_suicides_france.csv")

# Vérifier les colonnes disponibles pour adapter les noms
print(france_data.columns)

# Sélectionner les colonnes nécessaires : 'age', 'avg_suicides_per_100k'
france_data = france_data[['age', 'avg_suicides_per_100k']]

# Remplacer "years" par "ans" et ajuster les tranches d'âge pour correspondre à ce format
france_data['age'] = france_data['age'].str.replace('years', 'ans')  # Remplacer "years" par "ans"
france_data['age'] = france_data['age'].str.replace('5-14', '5-15')  # Si nécessaire ajuster 5-14 years à 5-15 ans, etc.

# Créer une colonne "age_min" qui extrait l'âge minimum de chaque tranche
france_data['age_min'] = france_data['age'].str.split('-').str[0].replace('75+ ans', '75').astype(int)

# Trier les données par la tranche d'âge minimale (age_min)
france_data_sorted = france_data.sort_values(by='age_min')

# Créer la figure et les axes pour le barplot
fig, ax = plt.subplots(figsize=(10, 6))

# Tracer le barplot pour la France
france_data_sorted.plot(kind='bar', x='age', y='avg_suicides_per_100k', ax=ax, legend=False, color='lightblue', edgecolor='black')

# Ajouter les titres et étiquettes
ax.set_title('Suicides par tranche d\'âge pour 100k habitants en France (2010-2016)', fontsize=14)
ax.set_xlabel('Tranche d\'âge', fontsize=12)  # Modifié pour inclure "ans"
ax.set_ylabel('Moyenne des suicides pour 100k habitants', fontsize=12)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

# Ajouter les valeurs entières au-dessus des barres
for p in ax.patches:
    ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', fontsize=12, color='black', xytext=(0, 5), textcoords='offset points')

# Ajuster l'affichage et sauvegarder l'image
plt.tight_layout()
plt.savefig("france_suicide_rate_by_age.png", format="png", bbox_inches="tight", dpi=300)  # Sauvegarder en PNG
plt.show()
