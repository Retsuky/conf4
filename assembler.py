import argparse
import struct
import xml.etree.ElementTree as ET

# Логирование операций в XML
def log_operation(log_path, operation_code, *args):
    if log_path:
        # Загружаем существующий XML или создаем новый
        try:
            tree = ET.parse(log_path)
            root = tree.getroot()
        except FileNotFoundError:
            root = ET.Element("Operations")  # Если файл не существует, создаем новый корень

        # Добавляем новый элемент для операции
        operation = ET.SubElement(root, "Operation")
        operation.set("Code", str(operation_code))
        operation.set("B", str(args[0]))
        operation.set("C", str(args[1]))

        # Записываем обновленное дерево в файл
        tree.write(log_path, encoding="utf-8", xml_declaration=True)

# Сериализация команды в бинарный формат
def serializer(cmd, fields, size):
    bits = 0
    bits |= cmd
    for value, offset in fields:
        bits |= (value << offset)
    return bits.to_bytes(size, "little")

# Команды УВМ
def load_command(B, C):
    """Загрузка константы в стек (5 байт)"""
    return serializer(43, [(B, 6)], 5)  # 43 - код команды, B в 32 бита

def read_command(B, C):
    """Чтение из памяти (3 байта)"""
    return serializer(2, [(B, 6)], 3)  # 2 - код команды, B в 15 бит

def write_command(B, C):
    """Запись в память (3 байта)"""
    return serializer(53, [(B, 6)], 3)  # 53 - код команды, B в 14 бит

def max_command(B, C):
    """Операция max (3 байта)"""
    return serializer(61, [(B, 6)], 3)  # 61 - код команды, B в 15 бит

# Ассемблер
def assembler(instructions, log_path=None):
    byte_code = []
    for operation, *args in instructions:
        if operation == "load":
            B, C = args
            byte_code += load_command(B, C)
            log_operation(log_path, 43, B, C)
        elif operation == "read":
            B, C = args
            byte_code += read_command(B, C)
            log_operation(log_path, 2, B, C)
        elif operation == "write":
            B, C = args
            byte_code += write_command(B, C)
            log_operation(log_path, 53, B, C)
        elif operation == "max":
            B, C = args
            byte_code += max_command(B, C)
            log_operation(log_path, 61, B, C)
        else:
            print(f"Unknown operation: {operation}")
    return byte_code

# Чтение инструкций и ассемблирование
def assemble(instructions_path, log_path=None):
    with open(instructions_path, "r", encoding="utf-8") as f:
        instructions = [[int(i) if i.isdigit() else i for i in line.split()] for line in f.readlines()]
    return assembler(instructions, log_path)

# Сохранение в бинарный файл
def save_to_bin(assembled_instructions, binary_path):
    with open(binary_path, "wb") as binary_file:
        binary_file.write(bytes(assembled_instructions))
    print(f"Binary file saved to: {binary_path}")

# Основная логика программы
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Assembling the instructions file to the byte-code.")
    parser.add_argument("instructions_path", help="Path to the instructions file (txt)")
    parser.add_argument("binary_path", help="Path to the binary file (bin)")
    parser.add_argument("log_path", help="Path to the log file (xml)")
    args = parser.parse_args()

    # Создаем и очищаем лог-файл, если он существует
    with open(args.log_path, "w", encoding="utf-8") as log_file:
        log_file.write('<?xml version="1.0" encoding="UTF-8"?>\n<Operations>\n</Operations>\n')

    # Ассемблирование инструкций
    assembled_instructions = assemble(args.instructions_path, args.log_path)
    
    # Сохранение бинарного файла
    save_to_bin(assembled_instructions, args.binary_path)

    # Вывод пути сохраненного лог-файла
    print(f"Log file saved to: {args.log_path}")
