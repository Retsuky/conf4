import argparse
import struct
import xml.etree.ElementTree as ET

# Функция для интерпретации бинарного файла
def interpreter(binary_path, result_path, memory_range):
    memory_size = 10240  # Увеличили размер памяти до 10240 ячеек
    memory = [0] * memory_size  
    stack = []
    memory[2] = 680
    with open(binary_path, "rb") as binary_file:
        byte_code = binary_file.read()

    i = 0
    while i < len(byte_code):
        command = byte_code[i]  # Первый байт указывает на команду
        A = command & 0x3F  # Биты 0-5 для команды
        B = int.from_bytes(byte_code[i + 1:i + 4], "little")  # Биты 6-37 (3 байта)
        C = 0  # C не используется в вашем описании, по умолчанию 0

        # Загрузка константы (43)
        if A == 43:
            # Загружаем константу в стек
            stack.append(B)
            i += 5  # Переход к следующей команде (размер команды 5 байт)

        # Чтение из памяти (2)
        elif A == 2:
            # Проверка на наличие элементов в стеке
            if stack:
                # Считываем адрес с вершины стека
                address = stack.pop() + B  # Адрес = верхушка стека + смещение B
                if 0 <= address < memory_size:  # Проверка на выход за границы памяти
                    stack.append(memory[address])  # Читаем из памяти и кладем в стек
                else:
                    pass  # Если адрес выходит за пределы, просто пропускаем
            i += 3  # Переход к следующей команде (размер команды 3 байта)

        # Запись в память (53)
        elif A == 53:
            # Проверка на наличие элементов в стеке
            if stack:
                # Считываем адрес из вершины стека
                address = stack.pop()
                if 0 <= B < memory_size:  # Проверка на выход за границы памяти
                    memory[B] = address  # Записываем в память по адресу B
                else:
                    pass  # Если адрес выходит за пределы, просто пропускаем
            i += 3  # Переход к следующей команде (размер команды 3 байта)

        # Операция max (61)
        elif A == 61:
            # Проверка на наличие элементов в стеке
            if len(stack) >= 2:
                # Считываем значения из памяти и стека
                address = stack.pop() + B  # Адрес = верхушка стека + смещение B
                if 0 <= address < memory_size:  # Проверка на выход за границы памяти
                    value_from_memory = memory[address]
                    value_from_stack = stack.pop()
                    stack.append(max(value_from_memory, value_from_stack))  # Результат max в стек
                else:
                    pass  # Если адрес выходит за пределы, просто пропускаем
            i += 3  # Переход к следующей команде (размер команды 3 байта)

        else:
            i += 1  # Если команда не распознана, пропускаем 1 байт

    # Запись результатов в XML
    root = ET.Element("Memory")
    for idx in range(memory_range[0], memory_range[1] + 1):
        elem = ET.SubElement(root, "Cell")
        elem.set("Address", str(idx))
        elem.set("Value", str(memory[idx]))
    
    tree = ET.ElementTree(root)
    tree.write(result_path)

# Основная логика
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interpreting the byte-code from the binary file to the result XML.")
    parser.add_argument("binary_path", help="Path to the binary file (bin)")
    parser.add_argument("result_path", help="Path to the result file (xml)")
    parser.add_argument("first_index", help="The first index of the memory range")
    parser.add_argument("last_index", help="The last index of the memory range")
    args = parser.parse_args()

    interpreter(args.binary_path, args.result_path, (int(args.first_index), int(args.last_index)))
