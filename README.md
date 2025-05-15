# Produktliste mit Mehrwertsteuer (Python + Excel)

Dieses Python-Projekt ermöglicht es dir, Einkäufe mit Bruttobetrag zu erfassen. Die Anwendung berechnet automatisch die Mehrwertsteuer und den Nettobetrag und speichert alle Daten in einer Excel-Datei.

---

## Projektstruktur
├── product.py # Klasse zur Repräsentation eines Produkts

├── excelManager.py # Klasse zum Schreiben in die Excel-Datei

├── inputManager.py # Klasse für Benutzereingabe

├── main.py # Hauptprogramm

└── test.xlsx # Automatisch erstellte Excel-Tabelle mit Einträgen


---

## Funktionen

- Eingabe von Produktname und Bruttobetrag
- Automatische Berechnung von:
  - Mehrwertsteuer (standardmäßig 19 %)
  - Nettobetrag
- Speicherung der Daten in einer Excel-Datei
- Automatisches Anlegen der Excel-Datei beim ersten Start

---

## Installation

1. **Repository klonen oder Dateien herunterladen**
2. **Abhängigkeiten installieren**:

```bash
pip install openpyxl
