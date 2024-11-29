import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
from typing import Tuple
import argparse

def get_image_dimensions(path: str) -> Tuple[int, int, int]:
    """
    получает размеры изображения по заданному пути.

    Args:
        path (str): путь к изображению.

    Returns:
        Tuple[int, int, int]: кортеж, содержащий ширину, высоту и глубину изображения.
    """
    with Image.open(path) as img:
        width, height = img.size
        depth = len(img.getbands())
    return width, height, depth

def filter_images_by_size(df: pd.DataFrame, max_width: int, max_height: int) -> pd.DataFrame:
    """
    фильтрует DataFrame по заданным  значениям ширины и высоты.

    Args:
        df (pd.DataFrame): исходный DataFrame.
        max_width (int): максимальная ширина изображения.
        max_height (int): максимальная высота изображения.

    Returns:
        pd.DataFrame: фильтрованный DataFrame.
    """
    return df[(df['width'] <= max_width) & (df['height'] <= max_height)]

def plot_area_histogram(df: pd.DataFrame) -> None:
    """
    строит гистограмму распределения площадей.

    Args:
        df (pd.DataFrame): DataFrame, содержащий информацию о площадях изображений.
    """
    plt.hist(df['area'], bins=20, edgecolor='black')
    plt.xlabel('Площадь изображения')
    plt.ylabel('Частота')
    plt.title('Распределение площадей изображений')
    plt.show()

def main(csv_path: str, max_width: int, max_height: int) -> None:
    """
    Args:
        csv_path (str): Путь к CSV файлу с аннотациями.
        max_width (int): Максимальная ширина изображения.
        max_height (int): Максимальная высота изображения.
    """

    df = pd.read_csv(csv_path)

    df.columns = ['abs_path', 'rel_path']

    print("Первые несколько строк DataFrame:")
    print(df.head())
    print()

    # применение функции к каждому абсолютному пути
    df[['width', 'height', 'depth']] = df['abs_path'].apply(lambda x: pd.Series(get_image_dimensions(x)))

    print("Первые несколько строк DataFrame после добавления столбцов с размерами изображения:")
    print(df.head())
    print()

    statistics = df[['width', 'height', 'depth']].describe()
    print("Статистическая информация:")
    print(statistics)
    print()

    # фильтрация по заданным параметрам
    df_filtered = filter_images_by_size(df, max_width, max_height).copy()

    # создание столбца с площадью
    df_filtered['area'] = df_filtered['width'] * df_filtered['height']

    # сортировка по площади
    df_sorted = df_filtered.sort_values(by='area')

    print("Первые несколько строк отсортированного DataFrame:")
    print(df_sorted.head())
    print()

    # строим гистограмму
    plot_area_histogram(df_sorted)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process image annotations and filter by size.")
    parser.add_argument("csv_path", type=str, help="Path to the CSV file with annotations.")
    parser.add_argument("max_width", type=int, help="Maximum width of the image.")
    parser.add_argument("max_height", type=int, help="Maximum height of the image.")

    args = parser.parse_args()

    main(args.csv_path, args.max_width, args.max_height)
