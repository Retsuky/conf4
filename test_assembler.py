from assembler import load_command, read_command, write_command, max_command, serializer

def load_command(B, offset):
    return serializer(43, [(B, 6)], 5)  # Загрузка константы

def test_load_command():
    """Тест для загрузки константы"""
    B = 457
    expected_bytes = bytes([0x6B, 0x72, 0x00, 0x00, 0x00])  # Ожидаемый результат
    result = load_command(B, 0)
    print(f"load_command - Result: {', '.join(f'0x{byte:02X}' for byte in result)}")  # Форматированный вывод
    assert result == expected_bytes, f"Expected: {expected_bytes.hex()}, Got: {result.hex()}"

def read_command(B, offset):
    return serializer(2, [(B, 6)], 3)  # Чтение значения из памяти

def test_read_command():
    """Тест для чтения значения из памяти"""
    B = 680
    expected_bytes = bytes([0x02, 0xAA, 0x00])  # Ожидаемый результат
    result = read_command(B, 0)
    print(f"read_command - Result: {', '.join(f'0x{byte:02X}' for byte in result)}")  # Форматированный вывод
    assert result == expected_bytes, f"Expected: {expected_bytes.hex()}, Got: {result.hex()}"

def write_command(B, offset):
    return serializer(53, [(B, 6)], 3)  # Запись значения в память

def test_write_command():
    """Тест для записи значения в память"""
    B = 625
    expected_bytes = bytes([0x75, 0x9C, 0x00])  # Ожидаемый результат
    result = write_command(B, 0)
    print(f"write_command - Result: {', '.join(f'0x{byte:02X}' for byte in result)}")  # Форматированный вывод
    assert result == expected_bytes, f"Expected: {expected_bytes.hex()}, Got: {result.hex()}"

def max_command(B, offset):
    return serializer(61, [(B, 6)], 3)  # 61 - код команды, B в 15 бит, сдвиг на 6 бит

def test_max_command():
    """Тест для бинарной операции max()"""
    B = 506
    expected_bytes = bytes([0xBD, 0x7E, 0x00])  # Ожидаемый результат
    result = max_command(B, 0)
    print(f"max_command - Result: {', '.join(f'0x{byte:02X}' for byte in result)}")  # Форматированный вывод
    assert result == expected_bytes, f"Expected: {expected_bytes.hex()}, Got: {result.hex()}"

# Запуск тестов
def run_tests():
    test_load_command()
    test_read_command()
    test_write_command()
    test_max_command()
    print("All tests passed successfully!")

# Запускаем все тесты
if __name__ == "__main__":
    run_tests()
