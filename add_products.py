import sqlite3

conn = sqlite3.connect("database.db")

cursor = conn.cursor()

# Supprime les anciens produits (optionnel)
cursor.execute("DELETE FROM products")

products = [

    (
        "Bracelet Nazar",
        "Bracelet fait main",
        25,
        "Bracelets",
        ""
    ),

    (
        "Collier Doré",
        "Collier élégant",
        35,
        "Colliers",
        ""
    ),

    (
        "Bague Perle",
        "Bague tendance",
        20,
        "Bagues",
        ""
    )

]

cursor.executemany(
    """
    INSERT INTO products
    (name, description, price, category, image)
    VALUES (?, ?, ?, ?, ?)
    """,
    products
)

conn.commit()
conn.close()

print("Produits ajoutés avec succès")