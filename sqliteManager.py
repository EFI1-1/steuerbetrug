import sqlite3
from product import Product

class SQLiteManager:
    def __init__(self, db_name="Datenbank.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS produkte (
            produkt_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            mwst_prozent REAL NOT NULL
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS verkaeufe (
            verkauf_id INTEGER PRIMARY KEY AUTOINCREMENT,
            produkt_id INTEGER,
            datum TEXT,
            menge INTEGER,
            brutto_einzel REAL,
            rabatt REAL,
            brutto_gesamt REAL,
            mwst_betrag REAL,
            netto_betrag REAL,
            FOREIGN KEY(produkt_id) REFERENCES produkte(produkt_id)
        )
        """)
        self.conn.commit()

    def insert_product_if_not_exists(self, name: str, mwst: float) -> int:
        self.cursor.execute("SELECT produkt_id FROM produkte WHERE name = ? AND mwst_prozent = ?", (name, mwst))
        result = self.cursor.fetchone()
        if result:
            return result[0]

        self.cursor.execute("INSERT INTO produkte (name, mwst_prozent) VALUES (?, ?)", (name, mwst))
        self.conn.commit()
        return self.cursor.lastrowid

    def insert_sale(self, product: Product):
        produkt_id = self.insert_product_if_not_exists(product.name, product.mwst_rate)
        self.cursor.execute("""
        INSERT INTO verkaeufe (
            produkt_id, datum, menge, brutto_einzel, rabatt, 
            brutto_gesamt, mwst_betrag, netto_betrag
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            produkt_id,
            product.datum,
            product.menge,
            product.brutto_einzel,
            product.rabatt,
            product.brutto,
            product.mwst,
            product.netto
        ))
        self.conn.commit()
        print("Verkauf in SQLite gespeichert.")

    def query_sales(self, start_date=None, end_date=None, name_filter=None):
        query = """
        SELECT p.name, v.datum, v.menge, v.brutto_einzel, v.rabatt, 
               v.brutto_gesamt, v.mwst_betrag, v.netto_betrag
        FROM verkaeufe v
        JOIN produkte p ON v.produkt_id = p.produkt_id
        WHERE 1=1
        """
        params = []
        if start_date:
            query += " AND date(v.datum) >= date(?)"
            params.append(start_date)
        if end_date:
            query += " AND date(v.datum) <= date(?)"
            params.append(end_date)
        if name_filter:
            query += " AND p.name LIKE ?"
            params.append(f"%{name_filter}%")

        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
