import cv2
import matplotlib.pyplot as plt
import numpy as np
import argparse

def load_image(file_path: str) -> np.ndarray:
    """
    Загружает изображение из указанного пути, выбрасывает ValueError в случае ошибки
    :param file_path: путь к изображению
    :return: image
    raise: ValueError если не удается открыть файл.
    """
    image = cv2.imread(file_path)
    if image is None:
        raise ValueError(f"Unable to load image from {file_path}")
    return image

def display_image_size(image: np.ndarray, name: str) -> None:
    """
    Выводит размеры изображения в консоль
    :param image: изображение размеры которого выводятся
    :param name: название изображения
    """
    height, width, _ = image.shape
    print(f"Size of {name}: {width}x{height}")

def plot_histogram(image, title) -> None:
    """
    Строит и отображает гистограмму интенсивности цветов для изображения.
    :param image: изображение для построения гистограммы
    :param title: заголовок для гистограммы
    """
    color = ('b', 'g', 'r')
    for i, col in enumerate(color):
        histr = cv2.calcHist([image], [i], None, [256], [0, 256])
        plt.plot(histr, color=col)
        plt.xlim([0, 256])
    plt.title(title)
    plt.xlabel('Intensity')
    plt.ylabel('Count')
    plt.show()

def blend_images(base_image: np.ndarray, overlay_image: np.ndarray, alpha: float) -> np.ndarray:
    """
    :param base_image: базовое изображение
    :param overlay_image: наложенное изображение
    :param alpha: коэффициент прозрачности (от 0.0 до 1.0)
    :return: смешанное изображение
    """
    overlay_image = cv2.resize(overlay_image, (base_image.shape[1], base_image.shape[0]))
    blended = cv2.addWeighted(base_image, 1 - alpha, overlay_image, alpha, 0)
    return blended

def main(base_image_path: str, overlay_image_path: str, output_path: str, alpha: float) -> None:
    base_image = load_image(base_image_path)
    overlay_image = load_image(overlay_image_path)

    display_image_size(base_image, "Base Image")
    display_image_size(overlay_image, "Overlay Image")

    plot_histogram(base_image, "Histogram of Base Image")
    plot_histogram(overlay_image, "Histogram of Overlay Image")

    blended_image = blend_images(base_image, overlay_image, alpha)

    plt.figure(figsize=(10, 5))
    plt.subplot(1, 3, 1)
    plt.title('Base Image')
    plt.imshow(cv2.cvtColor(base_image, cv2.COLOR_BGR2RGB))
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.title('Overlay Image')
    plt.imshow(cv2.cvtColor(overlay_image, cv2.COLOR_BGR2RGB))
    plt.axis('off')

    plt.subplot(1, 3, 3)
    plt.title('Blended Image')
    plt.imshow(cv2.cvtColor(blended_image, cv2.COLOR_BGR2RGB))
    plt.axis('off')

    plt.show()

    cv2.imwrite(output_path, blended_image)
    print(f"Blended image saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=' blend two images with alpha value.')
    parser.add_argument('base_image_path', type=str, help=' path to the base image')
    parser.add_argument('overlay_image_path', type=str, help='path to the overlay image')
    parser.add_argument('output_path', type=str, help='path to save the blended image')
    parser.add_argument('alpha', type=float, help='alpha value (0.0 to 1.0)')

    args = parser.parse_args()

    main(args.base_image_path, args.overlay_image_path, args.output_path, args.alpha)



