import xml.etree.ElementTree as ET
import csv
import time
import os

class AddressKey:
    def __init__(self, city, street, house):
        self.city = city
        self.street = street
        self.house = house

    def __eq__(self, other):
        return (self.city, self.street, self.house) == (other.city, other.street, other.house)

    def __hash__(self):
        return hash((self.city, self.street, self.house))

    def __repr__(self):
        return f"AddressKey(city={self.city}, street={self.street}, house={self.house})"

class AddressRecord:
    def __init__(self, city, street, house, floor):
        self.city = city
        self.street = street
        self.house = house
        self.floor = floor

    def __repr__(self):
        return f"AddressRecord(city={self.city}, street={self.street}, house={self.house}, floor={self.floor})"

class DataReader:
    def read_xml(self, file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()
        data = []
        for item in root.findall('item'):
            city = item.get('city')
            street = item.get('street')
            house = item.get('house')
            floor = item.get('floor')
            data.append(AddressRecord(city, street, house, floor))
        return data

    def read_csv(self, file_path):
        data = []
        with open(file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file, delimiter=';')
            for row in csv_reader:
                city = row['city']
                street = row['street']
                house = row['house']
                floor = row['floor']
                data.append(AddressRecord(city, street, house, floor))
        return data

class DataProcessor:
    def process_data(self, data):
        duplicates = {}
        floor_count = {}

        for record in data:
            key = AddressKey(record.city, record.street, record.house)
            if key in duplicates:
                duplicates[key] += 1
            else:
                duplicates[key] = 1

            if record.city not in floor_count:
                floor_count[record.city] = {str(i): 0 for i in range(1, 6)}
            floor_count[record.city][record.floor] += 1

        return duplicates, floor_count

class StatisticsPrinter:
    def print_statistics(self, duplicates, floor_count, processing_time):
        print(f"Время обработки файла: {processing_time:.2f} секунд")

        print("\nДублирующиеся записи:")
        for key, count in duplicates.items():
            if count > 1:
                print(f"Город: {key.city}, Улица: {key.street}, Дом: {key.house}, Количество повторений: {count}")

        print("\nКоличество зданий по этажности в каждом городе:")
        for city, floors in floor_count.items():
            print(f"Город: {city}")
            for floor, count in floors.items():
                print(f"  {floor}-этажных зданий: {count}")

class MainApp:
    def __init__(self):
        self.data_reader = DataReader()
        self.data_processor = DataProcessor()
        self.statistics_printer = StatisticsPrinter()

    def run(self):
        while True:
            file_path = input("Введите путь до файла-справочника (или 'exit' для завершения): ")
            if file_path.lower() == 'exit':
                break

            if not os.path.exists(file_path):
                print("Файл не найден. Попробуйте еще раз.")
                continue

            start_time = time.time()

            if file_path.endswith('.xml'):
                data = self.data_reader.read_xml(file_path)
            elif file_path.endswith('.csv'):
                data = self.data_reader.read_csv(file_path)
            else:
                print("Неподдерживаемый формат файла. Поддерживаются только XML и CSV.")
                continue

            duplicates, floor_count = self.data_processor.process_data(data)
            processing_time = time.time() - start_time

            self.statistics_printer.print_statistics(duplicates, floor_count, processing_time)

if __name__ == "__main__":
    app = MainApp()
    app.run()
