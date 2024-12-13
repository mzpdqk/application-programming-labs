import csv
import argparse
import os
from typing import List
from icrawler.builtin import GoogleImageCrawler

def fetch_imgs(term: str, folder: str, max_imgs: int = 100) -> List[str]:
    """Качаем изображения."""
    crawler = GoogleImageCrawler(storage={"root_dir": folder})
    crawler.crawl(keyword=term, max_num=max_imgs)

    return [os.path.join(folder, f) for f in os.listdir(folder)
            if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

def save_ann(img_paths: List[str], ann_file: str) -> None:
    """Записываем аннотации в CSV файл."""
    with open(ann_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['abs_path', 'rel_path'])
        for img in img_paths:
            writer.writerow([os.path.abspath(img), os.path.relpath(img, start=os.path.dirname(ann_file))])

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

def main():
    parser = argparse.ArgumentParser(description="загрузка изображений.")
    parser.add_argument("term", type=str, help="поисковый запрос")
    parser.add_argument("folder", type=str, help="папка для загрузки")
    parser.add_argument("ann_file", type=str, help="файл для аннотаций")
    args = parser.parse_args()

    os.makedirs(args.folder, exist_ok=True)
    img_paths = fetch_imgs(args.term, args.folder)
    save_ann(img_paths, args.ann_file)

    img_loader = ImgLoader(args.ann_file)
    for img_path in img_loader:
        print(img_path)

if __name__ == "__main__":
    main()
