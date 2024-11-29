import xml.etree.ElementTree as ET

def perform_max_operation(vector_a, vector_b):
    """
    Выполняет операцию max() поэлементно над двумя векторами
    и сохраняет результат во второй вектор.
    """
    result_vector = []
    
    # Поэлементно сравниваем элементы двух векторов
    for a, b in zip(vector_a, vector_b):
        result_vector.append(max(a, b))  # Сохраняем максимальное значение
    
    return result_vector

def save_result_to_xml(result_vector, file_path):
    """
    Сохраняет результат в XML файл.
    """
    root = ET.Element("Results")
    
    # Добавляем каждый элемент результата в XML
    for idx, value in enumerate(result_vector):
        elem = ET.SubElement(root, "Element")
        elem.set("Index", str(idx))
        elem.set("Value", str(value))
    
    # Записываем XML в файл
    tree = ET.ElementTree(root)
    tree.write(file_path)

def main():
    # Пример векторов
    vector_a = [1, 3, 5, 7, 9]
    vector_b = [2, 4, 6, 8, 10]
    
    # Выполняем операцию max() поэлементно
    result_vector = perform_max_operation(vector_a, vector_b)
    
    # Сохраняем результат в файл
    result_file = "test_result.xml"
    save_result_to_xml(result_vector, result_file)
    print(f"Результат записан в {result_file}")

if __name__ == "__main__":
    main()
