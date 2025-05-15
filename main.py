from excelManager import ExcelManager
from inputManager import InputManager

def main():
    manager = ExcelManager("test.xlsx")
    product = InputManager.enter_product()
    manager.save_entry(product)


if __name__ == "__main__": ## main
    main()