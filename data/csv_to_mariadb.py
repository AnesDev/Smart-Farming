import mariadb
import csv

conn = mariadb.connect(
    user="root",
    password="anesanes",
    host="localhost",
    database="smart_farming"
)
cur = conn.cursor()

with open("synthetic_data_2.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cur.execute("""
            INSERT INTO plant_data (
                `date`, `temperature_sol`, `humidite_sol`,
                `temperature_air`, `humidite_air`, `vecteur_latent`
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            row['date'],
            float(row['temperature_sol']),
            float(row['humidite_sol']),
            float(row['temperature_air']),
            float(row['humidite_air']),
            row['vecteur_latent']
        ))

conn.commit()
conn.close()
