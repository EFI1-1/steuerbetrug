import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from product import Product
from excelManager import ExcelManager
from sqliteManager import SQLiteManager
from datetime import datetime

class ProduktApp:
    def __init__(self, root):
        self.sql_manager = SQLiteManager()

        self.root = root
        self.root.title("Produkt-Eingabe")
        self.manager = ExcelManager("produkte.xlsx")

        tk.Label(root, text="Produktname:").grid(row=0, column=0)
        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=0, column=1)

        tk.Label(root, text="Einzelpreis (€)").grid(row=1, column=0)
        self.brutto_entry = tk.Entry(root)
        self.brutto_entry.grid(row=1, column=1)

        tk.Label(root, text="Menge:").grid(row=2, column=0)
        self.menge_entry = tk.Entry(root)
        self.menge_entry.insert(0, "1")
        self.menge_entry.grid(row=2, column=1)

        tk.Label(root, text="Rabatt (%):").grid(row=3, column=0)
        self.rabatt_entry = tk.Entry(root)
        self.rabatt_entry.insert(0,"0")
        self.rabatt_entry.grid(row=3, column=1)

        tk.Label(root, text="MwSt (%):").grid(row=4, column=0)
        self.mwst_var = tk.StringVar(value="19")
        ttk.Combobox(root, textvariable=self.mwst_var, values=["19", "7"], state="readonly").grid(row=4, column=1)

        self.save_excel = tk.BooleanVar(value=True)
        self.save_csv = tk.BooleanVar(value=False)
        tk.Checkbutton(root, text="Als Excel speichern", variable=self.save_excel).grid(row=5, column=0, sticky="w")
        tk.Checkbutton(root, text="Als CSV speichern", variable=self.save_csv).grid(row=5, column=1, sticky="w")

        tk.Button(root, text="Speichern", command=self.save_product).grid(row=6, columnspan=2, pady=10)

        # --- Anzeige-Optionen ---
        tk.Label(root, text="Von (TT.MM.JJJJ):").grid(row=7, column=0)
        self.start_entry = tk.Entry(root)
        self.start_entry.grid(row=7, column=1)

        tk.Label(root, text="Bis (TT.MM.JJJJ):").grid(row=8, column=0)
        self.end_entry = tk.Entry(root)
        self.end_entry.grid(row=8, column=1)

        tk.Label(root, text="Produktfilter:").grid(row=9, column=0)
        self.filter_name = tk.Entry(root)
        self.filter_name.grid(row=9, column=1)

        tk.Button(root, text="Verkäufe anzeigen", command=self.show_sales).grid(row=10, columnspan=2, pady=10)

        columns = ("Datum", "Produkt", "Menge", "Einzelpreis", "Rabatt", "Brutto", "MwSt", "Netto")
        self.sales_table = ttk.Treeview(root, columns=columns, show="headings", height=10)

        for col in columns:
            self.sales_table.heading(col, text=col)
            self.sales_table.column(col, anchor="center", width=100)

        self.sales_table.grid(row=11, columnspan=2)

    def show_sales(self):
        raw_start = self.start_entry.get().strip()
        raw_end = self.end_entry.get().strip()
        name_filter = self.filter_name.get().strip()

        def convert_date(date_str):
            try:
                return datetime.strptime(date_str, "%Y-%m-%d").strftime("%d.%m.%Y")
            except ValueError:
                return None

        start_date = convert_date(raw_start) if raw_start else None
        end_date = convert_date(raw_end) if raw_end else None

        results = self.sql_manager.query_sales(start_date, end_date, name_filter)

        for i in self.sales_table.get_children():
            self.sales_table.delete(i)

        if not results:
            self.sales_table.insert("", "end", values=("Keine Einträge gefunden.", "", "", "", "", "", "", ""))
        else:
            for row in results:
                self.sales_table.insert("", "end", values=(
                    row[1],  # Datum
                    row[0],  # Produktname
                    row[2],  # Menge
                    f"{row[3]:.2f} €",
                    f"{row[4]}%",
                    f"{row[5]:.2f} €",
                    f"{row[6]:.2f} €",
                    f"{row[7]:.2f} €"
                ))

    def save_product(self):
        try:
            name = self.name_entry.get()
            brutto = float(self.brutto_entry.get().replace(",", "."))
            menge = int(self.menge_entry.get())
            rabatt = float(self.rabatt_entry.get())
            mwst = float(self.mwst_var.get())

            product = Product(name, brutto, mwst, menge, rabatt)

            self.sql_manager.insert_sale(product)

            if self.save_excel.get():
                self.manager.save_entry(product)
            if self.save_csv.get():
                self.manager.save_csv(product)

            messagebox.showinfo("Erfolg", "Produkt gespeichert.")
            self.clear_entries()
        except Exception as e:
            messagebox.showerror("Fehler", f"Ungültige Eingabe: {e}")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.brutto_entry.delete(0, tk.END)
        self.menge_entry.delete(0, tk.END)
        self.rabatt_entry.delete(0, tk.END)
        self.menge_entry.insert(0, "1")
        self.rabatt_entry.insert(0, "0")
        self.mwst_var.set("19")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProduktApp(root)
    root.mainloop()