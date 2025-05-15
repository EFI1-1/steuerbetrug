from openpyxl import Workbook, load_workbook
import os
from product import Product

class ExcelManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.sheet_name = "Liste"
        self._initialize_file()

    def _initialize_file(self):
        if not os.path.exists(self.filename):
            wb = Workbook()
            ws = wb.active
            ws.title = self.sheet_name
            ws.append(["Datum", "Produktname", "Brutto Beitrag (€)", "MwSt (€)", "Netto Beitrag (€)"])
            wb.save(self.filename)

    def save_entry(self, product: Product):
        wb = load_workbook(self.filename)
        ws = wb[self.sheet_name]
        ws.append(product.file_list())
        wb.save(self.filename)
        print("Betrag wurde gespeichert!")