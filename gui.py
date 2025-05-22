import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from product import Product
from excelManager import ExcelManager

class ProduktApp:
    def __init__(self, root):
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

    def save_product(self):
        try:
            name = self.name_entry.get()
            brutto = float(self.brutto_entry.get().replace(",", "."))
            menge = int(self.menge_entry.get())
            rabatt = float(self.rabatt_entry.get())
            mwst = float(self.mwst_var.get())

            product = Product(name, brutto, mwst, menge, rabatt)

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