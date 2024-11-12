import pandas as pd
import matplotlib.pyplot as plt

# Charger les données de suicides
suicide_data = pd.read_csv("../data/uploads/average_suicides_per_100k_with_sex.csv/average_suicides_per_100k_with_sex.csv")

# Vérifier les colonnes disponibles pour adapter les noms
print(suicide_data.columns)

# Normalisation des noms des pays dans les données CSV
suicide_data['country'] = suicide_data['country'].str.strip().str.lower()  # Normalisation des noms dans les données CSV

# Dictionnaire pour corriger les correspondances
name_corrections = {
    "republic of korea": "Corée du Sud",
    "lithuania": "Lituanie",
    "guyana": "Guyane",
    "suriname": "Suriname",
    "belarus": "Biélorussie",
    "japan": "Japon",
}

# Appliquer les corrections
suicide_data['country'] = suicide_data['country'].replace(name_corrections)

# Filtrer les données pour les hommes et les femmes séparément
suicide_data_men = suicide_data[suicide_data['sex'] == 'male']
suicide_data_women = suicide_data[suicide_data['sex'] == 'female']

# Trier les données par "avg_suicides_per_100k" et prendre le top 5 pour les hommes et les femmes
top_5_men = suicide_data_men[['country', 'avg_suicides_per_100k']].sort_values(by='avg_suicides_per_100k', ascending=False).head(5)
top_5_women = suicide_data_women[['country', 'avg_suicides_per_100k']].sort_values(by='avg_suicides_per_100k', ascending=False).head(5)

# Créer la figure et les axes pour les deux barplots
fig, ax = plt.subplots(1, 2, figsize=(18, 8))

# Tracer le barplot pour les hommes
top_5_men.plot(kind='bar', x='country', y='avg_suicides_per_100k', ax=ax[0], legend=False, color='lightcoral', edgecolor='black')
ax[0].set_title('Top 5 nombres de suicides hommes pour 100k habitants (2010-2016)', fontsize=14)
ax[0].set_xlabel('Pays', fontsize=12)
ax[0].set_ylabel('Moyenne des suicides pour 100k habitants', fontsize=12)
ax[0].set_xticklabels(ax[0].get_xticklabels(), rotation=45, ha='right')

# Ajouter les valeurs entières au-dessus des barres pour les hommes
for p in ax[0].patches:
    ax[0].annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                   ha='center', va='center', fontsize=12, color='black', xytext=(0, 5), textcoords='offset points')

# Tracer le barplot pour les femmes
top_5_women.plot(kind='bar', x='country', y='avg_suicides_per_100k', ax=ax[1], legend=False, color='lightgreen', edgecolor='black')
ax[1].set_title('Top 5 nombres de suicides femmes par 100k habitants (2010-2016)', fontsize=14)
ax[1].set_xlabel('Pays', fontsize=12)
ax[1].set_ylabel('Moyenne des suicides pour 100k habitants', fontsize=12)
ax[1].set_xticklabels(ax[1].get_xticklabels(), rotation=45, ha='right')

# Ajouter les valeurs entières au-dessus des barres pour les femmes
for p in ax[1].patches:
    ax[1].annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                   ha='center', va='center', fontsize=12, color='black', xytext=(0, 5), textcoords='offset points')

# Ajuster l'affichage et sauvegarder l'image
plt.tight_layout()
plt.savefig("top_5_suicide_rate_men_women.png", format="png", bbox_inches="tight", dpi=300)  # Sauvegarder en PNG
plt.show()
