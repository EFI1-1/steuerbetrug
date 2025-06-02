from excelManager import ExcelManager
from inputManager import InputManager
from sqliteManager import SQLiteManager

def main():
    manager = SQLiteManager()
    product = InputManager.enter_product()
    manager.insert_sale(product)
    manager.close()
    manager = ExcelManager("test.xlsx")
    product = InputManager.enter_product()
    manager.save_entry(product)


if __name__ == "__main__": ## main
    main()