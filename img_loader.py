import csv
import os
from typing import List

class ImgLoader:
    def __init__(self, ann_file: str) -> None:
        """Инициализируем загрузчик."""
        self.ann_file = ann_file
        self.img_paths: List[str] = []
        self.index = 0
        self.load_ann()

    def load_ann(self) -> None:
        """Загружаем аннотации из CSV файла."""
        with open(self.ann_file, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # пропускаем заголовок
            self.img_paths = [row[0] for row in reader]

    def __iter__(self):
        """Возвращаем итератор."""
        return self

    def __next__(self) -> str:
        """Возвращаем следующий путь к изображению."""
        if self.index < len(self.img_paths):
            img_path = self.img_paths[self.index]
            self.index += 1
            return img_path
        else:
            raise StopIteration
