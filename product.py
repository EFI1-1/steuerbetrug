from datetime import datetime

class Product:
        def __init__(self, name: str, brutto: float, mwst: float = 19.0):
            self.name = name
            self.brutto = round(brutto, 2)
            self.mwst = mwst
            self.netto = round(self.brutto / (1 + mwst / 100), 2)
            self.mwst = round(self.brutto - self.netto, 2)
            self.datum = datetime.now().strftime("%d.%m.%Y")


        def file_list(self):
            return [self.datum, self.name, self.brutto, self.mwst, self.netto]

