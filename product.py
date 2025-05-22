from datetime import datetime

class Product:
    def __init__(self, name: str, brutto: float, mwst: float = 19.0, menge: int = 1, rabatt: float = 0.0):
        self.name = name
        self.menge = menge
        self.brutto_einzel = round(brutto, 2)
        self.rabatt = rabatt
        self.brutto = round(self.brutto_einzel * self.menge * (1 - rabatt / 100), 2)
        self.mwst_rate = mwst
        self.netto = round(self.brutto / (1 + mwst / 100), 2)
        self.mwst = round(self.brutto - self.netto, 2)
        self.datum = datetime.now().strftime("%d.%m.%Y")

    def file_list(self):
        return [self.datum, self.name, self.menge, self.brutto_einzel, self.rabatt, self.brutto, self.mwst_rate, self.mwst, self.netto]
