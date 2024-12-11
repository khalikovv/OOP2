import xml.etree.ElementTree as ET
import csv
import time
import os

def read_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    data = []
    for item in root.findall('item'):
        city = item.get('city')
        street = item.get('street')
        house = item.get('house')
        floor = item.get('floor')
        data.append((city, street, house, floor))
    return data

def read_csv(file_path):
    data = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file, delimiter=';')
        for row in csv_reader:
            city = row['city']
            street = row['street']
            house = row['house']
            floor = row['floor']
            data.append((city, street, house, floor))
    return data

def process_data(data):
    duplicates = {}
    floor_count = {}

    for record in data:
        key = (record[0], record[1], record[2])
        if key in duplicates:
            duplicates[key] += 1
        else:
            duplicates[key] = 1

        if record[0] not in floor_count:
            floor_count[record[0]] = {str(i): 0 for i in range(1, 6)}
        floor_count[record[0]][record[3]] += 1

    return duplicates, floor_count

def statistics(duplicates, floor_count, processing_time):
    print(f"Время обработки файла: {processing_time:.2f} секунд")

    print("\nДублирующиеся записи:")
    for key, count in duplicates.items():
        if count > 1:
            print(f"Город: {key[0]}, Улица: {key[1]}, Дом: {key[2]}, Количество повторений: {count}")

    print("\nКоличество зданий по этажности в каждом городе:")
    for city, floors in floor_count.items():
        print(f"Город: {city}")
        for floor, count in floors.items():
            print(f"  {floor}-этажных зданий: {count}")

def main():
    while True:
        file_path = input("Введите путь до файла-справочника (или 'exit' для завершения): ")
        if file_path.lower() == 'exit':
            break

        if not os.path.exists(file_path):
            print("Файл не найден. Попробуйте еще раз.")
            continue

        start_time = time.time()

        if file_path.endswith('.xml'):
            data = read_xml(file_path)
        elif file_path.endswith('.csv'):
            data = read_csv(file_path)
        else:
            print("Неподдерживаемый формат файла. Поддерживаются только XML и CSV.")
            continue

        duplicates, floor_count = process_data(data)
        processing_time = time.time() - start_time

        statistics(duplicates, floor_count, processing_time)

if __name__ == "__main__":
    main()
