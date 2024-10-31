import argparse
import re
from collections import Counter


def parse_args() -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str)
    args = parser.parse_args()
    return args.filename


def get_text(filename: str) -> str:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            text: str = file.read()
        return text
    except FileNotFoundError:
        print(f"Ошибка: Файл '{filename}' не найден.")
        exit(1)
    except IOError:
        print(f"Ошибка: Не удалось прочитать файл '{filename}'.")
        exit(1)


def find_operator_codes(text: str) -> list:
    # Регулярное выражение для поиска операторских кодов (+7 XXX)
    pattern_phone = r'\+7\s*(\d{3})'
    codes = re.findall(pattern_phone, text)
    return codes


def count_codes(codes: list) -> dict:
    # Подсчитываем частоту встречаемости кодов
    return Counter(codes)


def main():
    filename = parse_args()
    text = get_text(filename)
    codes = find_operator_codes(text)
    code_counts = count_codes(codes)

    if code_counts:
        # Находим наиболее частый код оператора
        most_common_code, count = code_counts.most_common(1)[0]
        print(f"Наиболее часто встречающийся код оператора: +7 {most_common_code}, число вхождений: {count}")
    else:
        print("Коды операторов не найдены.")


if __name__ == "__main__":
    main()