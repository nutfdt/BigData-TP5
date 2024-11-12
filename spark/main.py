import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg

# Initialiser la session Spark
spark = SparkSession.builder \
    .appName("SuicideAnalysis") \
    .getOrCreate()

# Charger les données depuis un fichier local
df = spark.read.load("../data/uploads/master.csv", format="csv", sep=",", inferSchema=True, header="true")

# Filtrer pour garder uniquement les années entre 2010 et 2016
filtered_df = df.filter((col("year") >= 2010) & (col("year") <= 2016))

# Calculer la moyenne de "suicides/100k pop" par pays
average_suicides_df = filtered_df.groupBy("country").agg(avg("suicides/100k pop").alias("avg_suicides_per_100k"))

# Écrire le DataFrame résultant dans un fichier CSV pour la visualisation avec une seule partition
output_dir_avg = "../data/uploads/average_suicides_per_100k.csv"
average_suicides_df.coalesce(1).write.mode("overwrite").csv(output_dir_avg, header=True)

# Renommer le fichier CSV généré pour "average_suicides_per_100k.csv"
for filename in os.listdir(output_dir_avg):
    if filename.startswith("part-"):
        os.rename(os.path.join(output_dir_avg, filename), os.path.join(output_dir_avg, "average_suicides_per_100k.csv"))
        break

# Calculer la moyenne de "suicides/100k pop" par pays et sexe
average_suicides_gender_df = filtered_df.groupBy("country", "sex").agg(
    avg("suicides/100k pop").alias("avg_suicides_per_100k")
)

# Écrire le DataFrame résultant dans un fichier CSV pour la visualisation avec une seule partition
output_dir_avg = "../data/uploads/average_suicides_per_100k_with_sex.csv"
average_suicides_gender_df.coalesce(1).write.mode("overwrite").csv(output_dir_avg, header=True)

# Renommer le fichier CSV généré pour "average_suicides_per_100k_with_sex.csv"
for filename in os.listdir(output_dir_avg):
    if filename.startswith("part-"):
        os.rename(os.path.join(output_dir_avg, filename), os.path.join(output_dir_avg, "average_suicides_per_100k_with_sex.csv"))
        break

# Filtrer les données pour ne garder que la France
france_data = filtered_df.filter(col("country") == "France")

# Sélectionner les colonnes nécessaires : 'age', 'suicides/100k pop'
france_data = france_data.select("age", "suicides/100k pop")

# Calculer la moyenne de "suicides/100k pop" par âge
average_suicides_france_df = france_data.groupBy("age").agg(
    avg("suicides/100k pop").alias("avg_suicides_per_100k")
)

# Écrire le DataFrame résultant dans un fichier CSV pour la visualisation avec une seule partition
output_dir_avg_france = "../data/uploads/average_suicides_france.csv"
average_suicides_france_df.coalesce(1).write.mode("overwrite").csv(output_dir_avg_france, header=True)

# Renommer le fichier CSV généré pour "average_suicides_france.csv"
for filename in os.listdir(output_dir_avg_france):
    if filename.startswith("part-"):
        os.rename(os.path.join(output_dir_avg_france, filename), os.path.join(output_dir_avg_france, "average_suicides_france.csv"))
        break

# Sélectionner les colonnes nécessaires
result_df = filtered_df.select(
    col("country"),
    col("year"),
    col("sex"),
    col("age"),
    col("suicides_no"),
    col("population"),
    col("suicides/100k pop")
)

# Vérifier s'il y a des valeurs négatives dans les colonnes numériques
negative_values_df = result_df.filter(
    (col("suicides_no") < 0) |
    (col("population") < 0) |
    (col("suicides/100k pop") < 0)
)

# Afficher les lignes avec des valeurs négatives, s'il y en a
if negative_values_df.count() > 0:
    print("Attention : Des valeurs négatives ont été trouvées dans les colonnes numériques suivantes :")
    negative_values_df.show()
else:
    print("Aucune valeur négative trouvée dans les colonnes numériques.")

# Écrire le résultat dans un fichier CSV avec une seule partition
output_dir_result = "../data/uploads/result-suicide-analysis.csv"
result_df.coalesce(1).write.mode("overwrite").csv(output_dir_result, header=True)

# Renommer le fichier CSV généré pour "result-suicide-analysis.csv"
for filename in os.listdir(output_dir_result):
    if filename.startswith("part-"):
        os.rename(os.path.join(output_dir_result, filename), os.path.join(output_dir_result, "result-suicide-analysis.csv"))
        break
