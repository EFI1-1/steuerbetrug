from product import Product

class InputManager:
    @staticmethod
    def enter_product() -> Product:
        name = input("Produktname: ")
        while True:
            try:
                preis = input("Betrag in Euro (brutto): ")
                preiswithoutkomma = preis.replace(",", ".")
                brutto = float(preiswithoutkomma)
                break
            except ValueError:
                print("Ungültiger Betrag. Bitte gib eine Zahl ein.")
        return Product(name, brutto)
